# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 12:20:09 2026

@author: chatGPT

exceute in the root directory of the project in a command window with:
    python -m pytest unittests/test_workshop.py -v
"""

import pytest

from workshop import Workshop


# ============================================================
# Helper class
# ============================================================

class FakeStudent:

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        return self.name


# ============================================================
# Initialisation
# ============================================================

def test_workshop_initialises_correctly():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    assert workshop.name == "Drama"
    assert workshop.capacity == 20
    assert workshop.n_slots == 3
    assert workshop.students == {
        0: [],
        1: [],
        2: [],
    }


def test_workshop_name_is_converted_to_string():

    workshop = Workshop(
        name=123,
        capacity=20,
        num_slots=3,
    )

    assert workshop.name == "123"


# ============================================================
# String representation
# ============================================================

def test_workshop_string_representation_without_students():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=2,
    )

    result = str(workshop)

    assert "Name: Drama" in result
    assert "Slot 0: 0 students" in result
    assert "Slot 1: 0 students" in result


def test_workshop_string_representation_includes_students():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=1,
    )

    student = FakeStudent("Alice")

    workshop.addStudentToSlot(
        student,
        slot=0,
    )

    result = str(workshop)

    assert "Name: Drama" in result
    assert "Slot 0: 1 students" in result
    assert "Alice" in result


# ============================================================
# Resetting students
# ============================================================

def test_reset_students_creates_empty_list_for_each_slot():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    student = FakeStudent("Alice")

    workshop.addStudentToSlot(
        student,
        slot=0,
    )

    workshop.resetStudents()

    assert workshop.students == {
        0: [],
        1: [],
        2: [],
    }


def test_reset_students_removes_students_from_all_slots():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    alice = FakeStudent("Alice")
    bob = FakeStudent("Bob")

    workshop.addStudentToSlot(alice, 0)
    workshop.addStudentToSlot(bob, 1)

    workshop.resetStudents()

    for slot in range(3):
        assert workshop.getStudentsInSlot(slot) == []


# ============================================================
# Getting students
# ============================================================

def test_get_students_in_slot_returns_students():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=2,
    )

    student = FakeStudent("Alice")

    workshop.addStudentToSlot(
        student,
        slot=1,
    )

    assert workshop.getStudentsInSlot(1) == [student]


# ============================================================
# Capacity
# ============================================================

def test_empty_slot_is_not_full():

    workshop = Workshop(
        name="Drama",
        capacity=2,
        num_slots=1,
    )

    assert workshop.isSlotFull(0) is False


def test_slot_is_full_when_capacity_is_reached():

    workshop = Workshop(
        name="Drama",
        capacity=2,
        num_slots=1,
    )

    alice = FakeStudent("Alice")
    bob = FakeStudent("Bob")

    workshop.addStudentToSlot(alice, 0)
    workshop.addStudentToSlot(bob, 0)

    assert workshop.isSlotFull(0) is True


def test_cannot_add_student_when_slot_is_full():

    workshop = Workshop(
        name="Drama",
        capacity=2,
        num_slots=1,
    )

    alice = FakeStudent("Alice")
    bob = FakeStudent("Bob")
    charlie = FakeStudent("Charlie")

    workshop.addStudentToSlot(alice, slot=0)
    workshop.addStudentToSlot(bob, slot=0)

    with pytest.raises(
        Exception,
        match="workshop slot is full cannot add student",
    ):
        workshop.addStudentToSlot(charlie, slot=0)


# ============================================================
# Adding students
# ============================================================

def test_add_student_to_slot():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=2,
    )

    student = FakeStudent("Alice")

    workshop.addStudentToSlot(
        student,
        slot=1,
    )

    assert workshop.getStudentsInSlot(1) == [student]


def test_add_student_to_one_slot_does_not_add_them_to_other_slots():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    student = FakeStudent("Alice")

    workshop.addStudentToSlot(
        student,
        slot=1,
    )

    assert workshop.getStudentsInSlot(0) == []
    assert workshop.getStudentsInSlot(1) == [student]
    assert workshop.getStudentsInSlot(2) == []


def test_same_student_cannot_be_added_to_workshop_twice():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=2,
    )

    student = FakeStudent("Alice")

    workshop.addStudentToSlot(
        student,
        slot=0,
    )

    with pytest.raises(
        Exception,
        match="workshop already has this student",
    ):
        workshop.addStudentToSlot(
            student,
            slot=1,
        )


def test_same_student_cannot_be_added_twice_to_same_slot():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=1,
    )

    student = FakeStudent("Alice")

    workshop.addStudentToSlot(
        student,
        slot=0,
    )

    with pytest.raises(
        Exception,
        match="workshop already has this student",
    ):
        workshop.addStudentToSlot(
            student,
            slot=0,
        )


# ============================================================
# Removing students
# ============================================================

def test_remove_student_from_slot():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=1,
    )

    student = FakeStudent("Alice")

    workshop.addStudentToSlot(
        student,
        slot=0,
    )

    workshop.removeStudentFromSlot(
        student,
        slot=0,
    )

    assert workshop.getStudentsInSlot(0) == []


def test_remove_student_only_removes_student_from_specified_slot():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=2,
    )

    alice = FakeStudent("Alice")
    bob = FakeStudent("Bob")

    workshop.addStudentToSlot(alice, 0)
    workshop.addStudentToSlot(bob, 1)

    workshop.removeStudentFromSlot(
        alice,
        slot=0,
    )

    assert workshop.getStudentsInSlot(0) == []
    assert workshop.getStudentsInSlot(1) == [bob]


def test_remove_student_not_in_slot_raises_error():

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=1,
    )

    student = FakeStudent("Alice")

    with pytest.raises(
        Exception,
        match="student not in this workshop slot",
    ):
        workshop.removeStudentFromSlot(
            student,
            slot=0,
        )