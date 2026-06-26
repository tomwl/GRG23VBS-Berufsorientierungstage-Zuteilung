# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:16:22 2026

@author: tom
"""

import pandas as pd
import re
from pathlib import Path

class FileIO:
    def __init__(self, pFile, wFile, sFout, wFout):
        self.prefencesFileIn = pFile
        self.workshopsFileIn = wFile
        self.studentsFileOut = sFout
        self.workshopsFileOut = wFout


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
        for w in preferences:  # ← Changed: was `ws` (the module), should be `preferences`
            n = re.sub(r"[\(\[].*?[\)\]]", "", w).strip()  # ← Raw string: r"..."
            n = n.strip("...")
            studentPreferences.append(n) 
        
        firstName = row.iloc[nameIndex].split(" ")[0]
        lastName = row.iloc[nameIndex].split(" ")[1]
        year = row.iloc[yearIndex]  # ← Fixed: was `year = lastName = ...` (overwrote lastName)
        
        students.append([firstName, lastName, year] + studentPreferences)  # ← Use studentPreferences, not preferences
        
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
        fileInputPath=Path("test_data/MS Forms/users.xlsx"),
        fileOutputPath=Path("output/user_test_data_output.xlsx"),
        nameIndex=4,
        yearIndex=8,
        preferencesIndex=11
    )
            
if __name__ == '__main__':
    main()