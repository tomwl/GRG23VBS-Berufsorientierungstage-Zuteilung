# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:16:22 2026

@author: tom
"""

import pandas as pd
import re
from pathlib import Path
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
            firstname = row["Vorname"]
            lastname = row["Nachname"]
            year = row["Klasse"]
            if not year:
                raise Exception("Student has no year")
            s = student.Student(firstname, lastname, year, n_slots)
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
                    data.append([wname, s.getName(), str(s.year)])
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
            data.append([s.getName(), str(s.year)] + s.getWorkshopNames())
        df = pd.DataFrame(data, 
                          columns=['Student Name', 'Class', 'Slot 1', 'Slot 2', 'Slot 3'])
        with pd.ExcelWriter(self.studentsFileOut) as writer:  
            df.to_excel(writer, index=False)
        


def processMSFormsData(
        fileInputPath: Path, 
        fileOutputPath:Path, 
        nameIndex: int, 
        yearIndex: int, 
        preferencesIndex: int ):
    
    data = pd.read_excel(fileInputPath, keep_default_na=False)
    data = data.drop_duplicates(subset=[data.columns[nameIndex]], keep='last')
    
    students = list()
    for index, row in data.iterrows():
        preferences = row.iloc[preferencesIndex].split(";")
        preferences = list(filter(None, preferences))
        
        studentPreferences = list()
        for w in preferences:  
            n = re.sub(r"[\(\[].*?[\)\]]", "", w).strip()  # ← Raw string: r"..."
            n = n.strip("...")
            studentPreferences.append(n) 
        
        firstName = row.iloc[nameIndex].split(" ")[0]
        lastName = row.iloc[nameIndex].split(" ")[1]
        year = row.iloc[yearIndex]  
        
        students.append([firstName, lastName, year] + studentPreferences)  
        
    max_cols = max(len(student) for student in students) if students else 3
    num_preferences = max_cols - 3 

    columns = ['Vorname', 'Nachname', 'Klasse'] + [f'Wunsch {i+1}' for i in range(num_preferences)]

    try:
        df = pd.DataFrame(students, columns=columns)
        with pd.ExcelWriter(fileOutputPath) as writer:
            df.to_excel(writer, index=False)
    except ValueError as e:
        print(f"ValueError: writing failed! {e}")
        
        
def main():      
    processMSFormsData(
        fileInputPath=Path("test_data/MS Forms/Berufsorientierungs.xlsx"),
        fileOutputPath=Path("test-data/user_test_data_output.xlsx"),
        nameIndex=4,
        yearIndex=6,
        preferencesIndex=7
    )
            
if __name__ == '__main__':
    main()