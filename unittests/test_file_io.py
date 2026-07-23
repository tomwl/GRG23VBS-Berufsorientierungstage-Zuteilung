# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:49:49 2026

@author: chatGPT

exceute in the root directory of the project in a command window with:
    python -m pytest unittests/test_file_io.py -v
"""

import pandas as pd
import pytest

from FileIO import (
    FileIO,
    processMSFormsData,
    findMissingStudents,
)
import workshop as ws


# ============================================================
# Tests for processMSFormsData
# ============================================================

def test_process_ms_forms_data_basic(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    input_df = pd.DataFrame({
        "Name": ["Alice Smith"],
        "Klasse": ["7A"],
        "Preferences": ["Drama; Football; Art"],
    })

    input_df.to_excel(input_file, index=False)

    processMSFormsData(
        fileInputPath=input_file,
        fileOutputPath=output_file,
        nameIndex=0,
        formIndex=1,
        preferencesIndex=2,
    )

    result = pd.read_excel(output_file, keep_default_na=False)

    expected = pd.DataFrame({
        "Name": ["alice smith"],
        "Klasse": ["7A"],
        "Wunsch 1": ["Drama"],
        "Wunsch 2": ["Football"],
        "Wunsch 3": ["Art"],
    })

    pd.testing.assert_frame_equal(result, expected)


def test_process_ms_forms_data_names_are_lowercase(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    input_df = pd.DataFrame({
        "Name": ["ALICE SMITH"],
        "Klasse": ["7A"],
        "Preferences": ["Drama"],
    })

    input_df.to_excel(input_file, index=False)

    processMSFormsData(
        input_file,
        output_file,
        nameIndex=0,
        formIndex=1,
        preferencesIndex=2,
    )

    result = pd.read_excel(output_file, keep_default_na=False)

    assert result.iloc[0]["Name"] == "alice smith"


def test_process_ms_forms_data_normalises_whitespace(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    input_df = pd.DataFrame({
        "Name": ["Alice"],
        "Klasse": ["7A"],
        "Preferences": ["   Drama    Club   ;   Football   "],
    })

    input_df.to_excel(input_file, index=False)

    processMSFormsData(
        input_file,
        output_file,
        nameIndex=0,
        formIndex=1,
        preferencesIndex=2,
    )

    result = pd.read_excel(output_file, keep_default_na=False)

    assert result.iloc[0]["Wunsch 1"] == "Drama Club"
    assert result.iloc[0]["Wunsch 2"] == "Football"


def test_process_ms_forms_data_removes_empty_preferences(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    input_df = pd.DataFrame({
        "Name": ["Alice"],
        "Klasse": ["7A"],
        "Preferences": ["Drama;;Football;"],
    })

    input_df.to_excel(input_file, index=False)

    processMSFormsData(
        input_file,
        output_file,
        nameIndex=0,
        formIndex=1,
        preferencesIndex=2,
    )

    result = pd.read_excel(output_file, keep_default_na=False)

    assert result.iloc[0]["Wunsch 1"] == "Drama"
    assert result.iloc[0]["Wunsch 2"] == "Football"


def test_process_ms_forms_data_duplicate_names_keep_last(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    input_df = pd.DataFrame({
        "Name": ["Alice", "Alice"],
        "Klasse": ["7A", "7B"],
        "Preferences": ["Drama", "Football"],
    })

    input_df.to_excel(input_file, index=False)

    processMSFormsData(
        input_file,
        output_file,
        nameIndex=0,
        formIndex=1,
        preferencesIndex=2,
    )

    result = pd.read_excel(output_file, keep_default_na=False)

    assert len(result) == 1
    assert result.iloc[0]["Klasse"] == "7B"
    assert result.iloc[0]["Wunsch 1"] == "Football"


def test_process_ms_forms_data_empty_input(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    input_df = pd.DataFrame({
        "Name": [],
        "Klasse": [],
        "Preferences": [],
    })

    input_df.to_excel(input_file, index=False)

    processMSFormsData(
        input_file,
        output_file,
        nameIndex=0,
        formIndex=1,
        preferencesIndex=2,
    )

    result = pd.read_excel(output_file, keep_default_na=False)

    assert list(result.columns) == ["Name", "Klasse"]
    assert len(result) == 0


# ============================================================
# Tests for findMissingStudents
# ============================================================

def test_find_missing_students_finds_unassigned_student(tmp_path):
    actual_file = tmp_path / "actual.xlsx"
    assigned_file = tmp_path / "assigned.xlsx"

    actual_df = pd.DataFrame({
        "foreName": ["Alice", "Bob", "Charlie"],
        "longName": ["Smith", "Jones", "Brown"],
        "klasse": ["7A", "7A", "7A"],
    })

    assigned_df = pd.DataFrame({
        "Name": ["Alice Smith", "Bob Jones"],
    })

    actual_df.to_excel(actual_file, index=False)
    assigned_df.to_excel(assigned_file, index=False)

    result = findMissingStudents(
        actual_file,
        assigned_file,
        ("7"),
    )

    print("ASDFASDFASDFASDF")
    print(result)
    assert result == ["charliebrown"]


def test_find_missing_students_returns_all_actual_students_when_none_are_assigned(tmp_path):
    actual_file = tmp_path / "actual.xlsx"
    assigned_file = tmp_path / "assigned.xlsx"
    
    expected = ["alicesmith", "bobjones", "charliebrown"]
    
    actual_df = pd.DataFrame({
        "foreName": ["Alice", "Bob", "Charlie"],
        "longName": ["Smith", "Jones", "Brown"],
        "klasse": ["7A", "7B", "7C"],
    })

    assigned_df = pd.DataFrame({
        "Name": [],
    })

    actual_df.to_excel(actual_file, index=False)
    assigned_df.to_excel(assigned_file, index=False)
    
    result = findMissingStudents(
        actual_file,
        assigned_file,
        ("7"),
    )
    
    assert set(result) == set(expected)
    
    
def test_find_missing_students_filters_by_class(tmp_path):
    actual_file = tmp_path / "actual.xlsx"
    assigned_file = tmp_path / "assigned.xlsx"
    
    expected = ["alicesmith", "bobjones"]
    
    actual_df = pd.DataFrame({
        "foreName": ["Alice", "Bob", "Charlie"],
        "longName": ["Smith", "Jones", "Brown"],
        "klasse": ["7A", "8B", "9C"],
    })

    assigned_df = pd.DataFrame({
        "Name": [],
    })

    actual_df.to_excel(actual_file, index=False)
    assigned_df.to_excel(assigned_file, index=False)
    
    result = findMissingStudents(
        actual_file,
        assigned_file,
        ("7", "8"),
    )
    
    assert set(result) == set(expected)


def test_find_missing_students_ignores_whitespace_differences(tmp_path):
    actual_file = tmp_path / "actual.xlsx"
    assigned_file = tmp_path / "assigned.xlsx"

    actual_df = pd.DataFrame({
        "foreName": ["Anna Maria"],
        "longName": ["Smith"],
        "klasse": ["7A"],
    })

    assigned_df = pd.DataFrame({
        "Name": ["AnnaMariaSmith"],
    })

    actual_df.to_excel(actual_file, index=False)
    assigned_df.to_excel(assigned_file, index=False)

    result = findMissingStudents(
        actual_file,
        assigned_file,
        ("7"),
    )

    assert result == []


def test_find_missing_students_similar_name_is_assigned(tmp_path):
    actual_file = tmp_path / "actual.xlsx"
    assigned_file = tmp_path / "assigned.xlsx"

    actual_df = pd.DataFrame({
        "foreName": ["Alice"],
        "longName": ["Smith"],
        "klasse": ["7A"],
    })

    assigned_df = pd.DataFrame({
        "Name": ["AliceeSmith"],
    })

    actual_df.to_excel(actual_file, index=False)
    assigned_df.to_excel(assigned_file, index=False)

    result = findMissingStudents(
        actual_file,
        assigned_file,
        ("7"),
    )

    assert result == []


# ============================================================
# Tests for FileIO.initialiseWorkshops
# ============================================================

def test_initialise_workshops(tmp_path):
    workshops_file = tmp_path / "workshops.xlsx"

    workshops_df = pd.DataFrame({
        "Name": ["Drama", "Football"],
        "Capacity": [20, 15],
    })

    workshops_df.to_excel(workshops_file, index=False)

    file_io = FileIO(
        pFile=None,
        wFile=workshops_file,
        sFout=None,
        wFout=None,
    )

    workshops = file_io.initialiseWorkshops(n_slots=3)

    assert len(workshops) == 2

    assert workshops[0].name == "Drama"
    assert workshops[0].capacity == 20

    assert workshops[1].name == "Football"
    assert workshops[1].capacity == 15


# ============================================================
# Tests for FileIO.initialisePreferences
# ============================================================

def test_initialise_preferences(tmp_path):
    preferences_file = tmp_path / "preferences.xlsx"

    preferences_df = pd.DataFrame({
        "Name": ["Alice"],
        "Klasse": ["7A"],
        "Wunsch 1": ["Drama"],
        "Wunsch 2": ["Football"],
        "Wunsch 3": ["Art"],
        "Wunsch 4": ["Music"],
        "Wunsch 5": ["Science"],
        "Wunsch 6": ["Maths"],
        "Wunsch 7": ["History"],
        "Wunsch 8": ["English"],
        "Wunsch 9": ["French"],
        "Wunsch 10": ["Geography"],
    })

    preferences_df.to_excel(preferences_file, index=False)

    workshops = [
        ws.Workshop("Drama", 20, 3),
        ws.Workshop("Football", 20, 3),
        ws.Workshop("Art", 20, 3),
        ws.Workshop("Music", 20, 3),
        ws.Workshop("Science", 20, 3),
        ws.Workshop("Maths", 20, 3),
        ws.Workshop("History", 20, 3),
        ws.Workshop("English", 20, 3),
        ws.Workshop("French", 20, 3),
        ws.Workshop("Geography", 20, 3),
    ]

    file_io = FileIO(
        pFile=preferences_file,
        wFile=None,
        sFout=None,
        wFout=None,
    )

    students = file_io.initialisePreferences(
        workshops,
        n_slots=3,
    )

    assert len(students) == 1
    assert students[0].getName() == "Alice"
    assert students[0].form == "7A"


def test_initialise_preferences_missing_form_raises_error(tmp_path):
    preferences_file = tmp_path / "preferences.xlsx"

    preferences_df = pd.DataFrame({
        "Name": ["Alice"],
        "Klasse": [""],
        "Wunsch 1": ["Drama"],
        "Wunsch 2": ["Football"],
        "Wunsch 3": ["Art"],
        "Wunsch 4": ["Music"],
        "Wunsch 5": ["Science"],
        "Wunsch 6": ["Maths"],
        "Wunsch 7": ["History"],
        "Wunsch 8": ["English"],
        "Wunsch 9": ["French"],
        "Wunsch 10": ["Geography"],
    })

    preferences_df.to_excel(preferences_file, index=False)

    workshops = []

    file_io = FileIO(
        pFile=preferences_file,
        wFile=None,
        sFout=None,
        wFout=None,
    )

    with pytest.raises(Exception, match="Student has no form"):
        file_io.initialisePreferences(
            workshops,
            n_slots=3,
        )


def test_initialise_preferences_unknown_workshop_raises_error(tmp_path):
    preferences_file = tmp_path / "preferences.xlsx"

    preferences_df = pd.DataFrame({
        "Name": ["Alice"],
        "Klasse": ["7A"],
        "Wunsch 1": ["Unknown Workshop"],
        "Wunsch 2": ["Football"],
        "Wunsch 3": ["Art"],
        "Wunsch 4": ["Music"],
        "Wunsch 5": ["Science"],
        "Wunsch 6": ["Maths"],
        "Wunsch 7": ["History"],
        "Wunsch 8": ["English"],
        "Wunsch 9": ["French"],
        "Wunsch 10": ["Geography"],
    })

    preferences_df.to_excel(preferences_file, index=False)

    workshops = []

    file_io = FileIO(
        pFile=preferences_file,
        wFile=None,
        sFout=None,
        wFout=None,
    )

    with pytest.raises(
        Exception,
        match="Workshop not found for student in initialisation",
    ):
        file_io.initialisePreferences(
            workshops,
            n_slots=3,
        )


# ============================================================
# Tests for FileIO.writeStudents
# ============================================================

class FakeStudent:

    def __init__(self, name, form, workshops):
        self.name = name
        self.form = form
        self.workshops = workshops

    def getName(self):
        return self.name

    def getWorkshopNames(self):
        return self.workshops


def test_write_students(tmp_path):
    output_file = tmp_path / "students.xlsx"

    file_io = FileIO(
        pFile=None,
        wFile=None,
        sFout=output_file,
        wFout=None,
    )

    students = [
        FakeStudent(
            "Alice",
            "7A",
            ["Drama", "Football", "Art"],
        )
    ]

    file_io.writeStudents(students)

    result = pd.read_excel(output_file)

    assert list(result.columns) == [
        "Student Name",
        "Class",
        "Slot 1",
        "Slot 2",
        "Slot 3",
    ]

    assert result.iloc[0]["Student Name"] == "Alice"
    assert result.iloc[0]["Class"] == "7A"
    assert result.iloc[0]["Slot 1"] == "Drama"
    assert result.iloc[0]["Slot 2"] == "Football"
    assert result.iloc[0]["Slot 3"] == "Art"


# ============================================================
# Tests for FileIO.writeWorkshops
# ============================================================

class FakeWorkshop:

    def __init__(self, name, students_by_slot):
        self.name = name
        self.students_by_slot = students_by_slot

    def getStudentsInSlot(self, slot):
        return self.students_by_slot.get(slot, [])


def test_write_workshops(tmp_path):
    output_file = tmp_path / "workshops.xlsx"

    file_io = FileIO(
        pFile=None,
        wFile=None,
        sFout=None,
        wFout=output_file,
    )

    workshop = FakeWorkshop(
        "Drama",
        {
            0: [
                FakeStudent(
                    "Alice",
                    "7A",
                    [],
                )
            ],
            1: [],
            2: [],
        },
    )

    file_io.writeWorkshops(
        workshops=[workshop],
        slots=3,
    )

    result_slot_0 = pd.read_excel(
        output_file,
        sheet_name="0",
    )

    result_slot_1 = pd.read_excel(
        output_file,
        sheet_name="1",
    )

    assert list(result_slot_0.columns) == [
        "Workshop",
        "Student Name",
        "Class",
    ]

    assert result_slot_0.iloc[0]["Workshop"] == "Drama"
    assert result_slot_0.iloc[0]["Student Name"] == "Alice"
    assert result_slot_0.iloc[0]["Class"] == "7A"

    assert len(result_slot_1) == 0