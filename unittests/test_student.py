# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 11:52:55 2026

@author: chatGPT

exceute in the root directory of the project in a command window with:
    python -m pytest unittests/test_student.py -v
"""

import pytest

from student import Student
from workshop import Workshop


# ============================================================
# Constructor and basic properties
# ============================================================

def test_student_initialises_with_correct_properties():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    assert student.name == "Alice"
    assert student.form == "7A"
    assert student.year == 7
    assert len(student.workshops) == 3
    assert student.workshops == [None, None, None]
    assert student.preferences == []


def test_student_get_name():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    assert student.getName() == "Alice"


def test_student_string_representation():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    assert str(student) == "Alice in form 7A"


# ============================================================
# Preferences
# ============================================================

def test_assign_preference_adds_workshop():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    student.assignPreference(workshop)

    assert student.preferences == [workshop]


def test_assign_none_as_preference_does_nothing():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    student.assignPreference(None)

    assert student.preferences == []


def test_multiple_preferences_are_kept_in_order():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    drama = Workshop("Drama", 20, 3)
    football = Workshop("Football", 20, 3)
    art = Workshop("Art", 20, 3)

    student.assignPreference(drama)
    student.assignPreference(football)
    student.assignPreference(art)

    assert student.preferences == [
        drama,
        football,
        art,
    ]


# ============================================================
# Assigning workshops
# ============================================================

def test_assign_workshop_assigns_workshop_to_correct_slot():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    student.assignWorkshop(
        workshop,
        slot=1,
    )

    assert student.workshops == [
        None,
        workshop,
        None,
    ]


def test_assign_workshop_adds_student_to_workshop():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    student.assignWorkshop(
        workshop,
        slot=1,
    )

    assert student in workshop.getStudentsInSlot(1)


def test_assigning_same_workshop_twice_raises_error():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    student.assignWorkshop(
        workshop,
        slot=0,
    )

    with pytest.raises(
        Exception,
        match="student already has this workshop",
    ):
        student.assignWorkshop(
            workshop,
            slot=1,
        )


# ============================================================
# Removing workshops
# ============================================================

def test_remove_workshop_removes_workshop_from_student():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    student.assignWorkshop(
        workshop,
        slot=1,
    )

    student.removeWorkshop(
        workshop,
        slot=1,
    )

    assert student.workshops == [
        None,
        None,
        None,
    ]


def test_remove_workshop_removes_student_from_workshop():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    student.assignWorkshop(
        workshop,
        slot=1,
    )

    student.removeWorkshop(
        workshop,
        slot=1,
    )

    assert student not in workshop.getStudentsInSlot(1)


def test_remove_workshop_that_student_does_not_have_raises_error():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    workshop = Workshop(
        name="Drama",
        capacity=20,
        num_slots=3,
    )

    with pytest.raises(
        Exception,
        match="trying to remove workshop from student",
    ):
        student.removeWorkshop(
            workshop,
            slot=0,
        )


# ============================================================
# Resetting workshops
# ============================================================

def test_reset_workshops_removes_all_assignments():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    drama = Workshop("Drama", 20, 3)
    football = Workshop("Football", 20, 3)

    student.assignWorkshop(drama, 0)
    student.assignWorkshop(football, 1)

    student.resetWorkshops()

    assert student.workshops == [
        None,
        None,
        None,
    ]


# ============================================================
# Workshop names and objects
# ============================================================

def test_get_workshop_names_returns_names_in_slot_order():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    drama = Workshop("Drama", 20, 3)
    football = Workshop("Football", 20, 3)

    student.assignWorkshop(drama, 0)
    student.assignWorkshop(football, 2)

    assert student.getWorkshopNames() == [
        "Drama",
        "",
        "Football",
    ]


def test_get_workshops_returns_workshops_in_slot_order():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    drama = Workshop("Drama", 20, 3)

    student.assignWorkshop(drama, 1)

    assert student.getWorkshops() == [
        None,
        drama,
        None,
    ]


# ============================================================
# Unhappiness score
# ============================================================

def test_unhappiness_score_for_first_preference_is_zero():
    student = Student(
        name="Alice",
        form="7A",
        nslots=1,
    )

    drama = Workshop("Drama", 20, 1)

    student.assignPreference(drama)
    student.assignWorkshop(drama, 0)

    assert student.unhappiness_score() == 0


def test_unhappiness_score_uses_preference_rank():
    student = Student(
        name="Alice",
        form="7A",
        nslots=1,
    )

    drama = Workshop("Drama", 20, 1)
    football = Workshop("Football", 20, 1)
    art = Workshop("Art", 20, 1)

    student.assignPreference(drama)
    student.assignPreference(football)
    student.assignPreference(art)

    student.assignWorkshop(art, 0)

    # Art is preference index 2
    # WEIGHT_MAP[2] == 2
    assert student.unhappiness_score() == 2


def test_unhappiness_score_can_use_supplied_workshops():
    student = Student(
        name="Alice",
        form="7A",
        nslots=2,
    )

    drama = Workshop("Drama", 20, 2)
    football = Workshop("Football", 20, 2)

    student.assignPreference(drama)
    student.assignPreference(football)

    assert student.unhappiness_score(
        workshops=[football]
    ) == 1


# ============================================================
# Lowest preference
# ============================================================

def test_get_lowest_preference_workshop_returns_lowest_ranked_workshop():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    drama = Workshop("Drama", 20, 3)
    football = Workshop("Football", 20, 3)
    art = Workshop("Art", 20, 3)

    student.assignPreference(drama)
    student.assignPreference(football)
    student.assignPreference(art)

    student.assignWorkshop(drama, 0)
    student.assignWorkshop(art, 1)
    
    assert student.getLowestPreferenceWorkshop() == art


def test_get_lowest_preference_workshop_returns_none_when_no_workshops_assigned():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    assert student.getLowestPreferenceWorkshop() is None


# ============================================================
# Checking whether workshops are all different
# ============================================================

def test_check_workshops_all_different_returns_true():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    drama = Workshop("Drama", 20, 3)
    football = Workshop("Football", 20, 3)
    art = Workshop("Art", 20, 3)

    student.assignWorkshop(drama, 0)
    student.assignWorkshop(football, 1)
    student.assignWorkshop(art, 2)

    assert student.checkWorkshopsAllDifferent() is True


def test_check_workshops_all_different_returns_false_for_duplicate_workshop():
    student = Student(
        name="Alice",
        form="7A",
        nslots=3,
    )

    drama = Workshop("Drama", 20, 3)

    # Directly set up the invalid state because assignWorkshop()
    # correctly prevents duplicate workshops.
    student.workshops = [
        drama,
        drama,
        None,
    ]

    assert student.checkWorkshopsAllDifferent() is False