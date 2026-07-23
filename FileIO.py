# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:16:22 2026

@author: tom
"""

import pandas as pd
import re
from pathlib import Path
from difflib import SequenceMatcher
import workshop as ws
import student

class FileIO:
    def __init__(self, pFile, wFile, sFout, wFout):
        self.prefencesFileIn = pFile
        self.workshopsFileIn = wFile
        self.studentsFileOut = sFout
        self.workshopsFileOut = wFout
        
    def initialiseWorkshops(self, n_slots):
        workshops = pd.read_excel(self.workshopsFileIn, keep_default_na=False)
        result = []
        for index, row in workshops.iterrows():  
            result.append(ws.Workshop(row["Name"], 
                                      int(row["Capacity"]),
                                      n_slots))
        return result
    
    def initialisePreferences(self, workshops, n_slots):
        preferences = pd.read_excel(self.prefencesFileIn, keep_default_na=False)
        students = []
        for index, row in preferences.iterrows():
            name = row["Name"]
            form = row["Klasse"]
            if not form:
                raise Exception("Student has no form")
            s = student.Student(name, form, n_slots)
            # find and allocate preferences from workshop list
            for i in range(1, 11):
                preference_i = row["Wunsch " + str(i)]
                ws = [x for x in workshops if x.name == preference_i]
                if ws:
                    for result in ws:
                        s.assignPreference(result)
                else:
                    raise Exception("Workshop not found for student in initialisation")
            students.append(s)
        return students
    
    def writeWorkshops(self, workshops, slots):
        """Given a list of workshops with students assigned, write this information
        to a file

        Parameters
        ----------
        workshops : list of Workshop
            The list of workshops with students assigned to them.

        Returns
        -------
        None.

        """
        df = []
        for i in range(slots):
            df.append(None)
        for i in range(slots):
            data = []
            for w in workshops:
                wname = w.name
                students = w.getStudentsInSlot(i)
                for s in students:
                    data.append([wname, s.getName(), s.form])
            df[i] = pd.DataFrame(data, columns=['Workshop', 'Student Name', 'Class'])
        
        with pd.ExcelWriter(self.workshopsFileOut) as writer:
            for i in range(slots):
                df[i].to_excel(writer, sheet_name=str(i), index=False)
            
    def writeStudents(self, students):
        """Given a list of forms, containing students to whom workshops have
        been assigned, write this information to file

        Parameters
        ----------
        forms : list of Form
            The forms containing the students and their assigned workshops.

        Returns
        -------
        None.

        """
        data = []
        for s in students:
            data.append([s.getName(), s.form] + s.getWorkshopNames())
        df = pd.DataFrame(data, 
                          columns=['Student Name', 'Class', 'Slot 1', 'Slot 2', 'Slot 3'])
        with pd.ExcelWriter(self.studentsFileOut) as writer:  
            df.to_excel(writer, index=False)
        


def processMSFormsData(
        fileInputPath: Path, 
        fileOutputPath:Path, 
        nameIndex: int, 
        formIndex: int, 
        preferencesIndex: int ):
    
    data = pd.read_excel(fileInputPath, keep_default_na=False)
    data = data.drop_duplicates(subset=[data.columns[nameIndex]], keep='last')
    
    students = list()
    for index, row in data.iterrows():
        preferences = row.iloc[preferencesIndex].split(";")
        preferences = list(filter(None, preferences))
        
        studentPreferences = list()
        for w in preferences:  
            n = " ".join(w.split())
            studentPreferences.append(n) 
        
        name = row.iloc[nameIndex].lower()
        form = row.iloc[formIndex]  
        
        students.append([name, form] + studentPreferences)  
        
    max_cols = max(len(student) for student in students) if students else 2
    num_preferences = max_cols - 2 

    columns = ['Name', 'Klasse'] + [f'Wunsch {i+1}' for i in range(num_preferences)]

    try:
        df = pd.DataFrame(students, columns=columns)
        with pd.ExcelWriter(fileOutputPath) as writer:
            df.to_excel(writer, index=False)
    except ValueError as e:
        print(f"ValueError: writing failed! {e}")

def findMissingStudents(
        fname_actual: str, 
        fname_assigned: str, 
        classes: tuple):
    """
    Go through a file with a list of all students, filter out all students
    not in the desired year groups (classes)

    Parameters
    ----------
    fname_actual : str
        the nameof the file containing a list of all students in the school.
    fname_assigned : str
        the name of the file containing the assigned students.
    classes: tuple
        the desired year groups you want, example ('7', '8')

    Returns
    -------
    unassignedStudents : list
        A list containing the names of the unassigned students.

    """
    actualStudents = pd.read_excel(fname_actual, keep_default_na=False)  
    # filter to students in the above classes
    actualStudents = (
        actualStudents[actualStudents.klasse.astype(str).str.startswith(classes)]
    )
        
    # set with the (full) names of all actualStudents with no whitespace
    actualStudentSet = set()
    for row in actualStudents[["foreName", "longName"]].itertuples(index=False):
        firstName = re.sub(r"\s+", "", row.foreName.lower())
        lastName = re.sub(r"\s+", "", row.longName.lower())
        combinedName = firstName + lastName
        actualStudentSet.add(combinedName)
        
    # get students we already assigned
    assignedStudents = pd.read_excel(fname_assigned, keep_default_na=False)
    
    # organise them into a set that contains names with no whitespace
    assignedStudentsNoSpaces = {
        re.sub(r"\s+", "", str(name).lower())
        for name in set(list(assignedStudents["Name"]))
    }
    # if the assigned file has no entries return all students
    if not assignedStudentsNoSpaces: 
        return list(actualStudentSet)
    
    # find the unassigned students
    unassignedStudents = []
    for person in actualStudentSet:
        maxMatch = max(
            (
                SequenceMatcher(a=person, b=s).ratio()
                for s in assignedStudentsNoSpaces
            ),
            default=0
        )
        if not maxMatch > 0.9:
            unassignedStudents.append(person)
    
    # return the list of students that are in the system but weren't assigned
    return unassignedStudents
        
        
def main():      
    data_dir = Path.cwd() / "test_data"
    processMSFormsData(
        fileInputPath=data_dir / "MS Forms" / "Berufsorientierung-3.xlsx",
        fileOutputPath=data_dir / "user_test_data_output.xlsx",
        nameIndex=4,
        formIndex=6,
        preferencesIndex=7
    )
    #findMissingStudents(
    #    r"C:\Users\tom\Downloads\all_students_2026.xls", 
    #    data_dir / "user_test_data_output.xlsx",
    #    ('7', '8')
    #)
            
if __name__ == '__main__':
    main()