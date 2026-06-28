# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:05:26 2026

@author: tom
"""

import os
import random
import FileIO

NUM_SLOTS = 3 # how many workshops should each student visit
UNHAPPINESS_TARGET_SCORE = 500 # if you get below this score, well done
NUM_OPTIMISATIONS = 10000 # how many iterations to do when optimising allocation

# ToDo: May have to add code to assign less popular workshops first

def printNumberOfPeopleInWorkshops(workshops):
    for w in workshops:
        print(w.name)
        for slot in range(NUM_SLOTS):
            print(len(w.getStudentsInSlot(slot)))

def assignYearGroup(students, unassigned):
    for s in students:
        # loop through and try brute force assignment of workshops to students 
        slot_counter = 0
        for p in s.preferences:
            if all(x is not None for x in s.workshops):
                break
            if not p.isSlotFull(slot_counter):
                s.assignWorkshop(p, slot_counter)
                slot_counter += 1
        if any(x is None for x in s.workshops):
            # we have a problem, they have empty slots
            print("Error, student missing workshop")
            unassigned.append(s)

def assignWorkshops(workshops, students):
    """
    Main function for workshop assignment
    Goal: Let's assign students to workshops they want to visit.
    First brute force and then try an optimisation routine

    Returns
    -------
    None.

    """
    unassignedStudents = []
    for w in workshops:
        w.resetStudents()
    for s in students:
        s.resetWorkshops()
    # get the 8th year students first
    target_students = [x for x in students if x.year == 8]
    assignYearGroup(target_students, unassignedStudents)
    
    target_students = [x for x in students if x.year == 7] # now do 7th year
    
    # initial assignment is pretty simple, just brute force assign
    assignYearGroup(target_students, unassignedStudents)
    
    printNumberOfPeopleInWorkshops(workshops)
    
    #calculate total unhappiness before optimisation
    unhappiness = sum(s.unhappiness_score() for s in students)
    print(unhappiness)
    
    # try to do some swapping to make people a bit happier
    counter = 0
    improvements_counter = 0
    while counter <= NUM_OPTIMISATIONS and unhappiness > UNHAPPINESS_TARGET_SCORE:
        counter += 1
        # total unhappiness
        unhappiness = sum(s.unhappiness_score() for s in students)
        # randomly select from unhappy students, weighted by unhappiness
        weights = [s.unhappiness_score() for s in students]

        unhappiest = random.choices(
            students,
            weights=weights,
            k=1
        )[0]
        
        # get lowest preference workshop for unhappiest person
        workshop_to_swap = unhappiest.getLowestPreferenceWorkshop()
        if workshop_to_swap is None:
            continue
        workshop_to_swap_idx = unhappiest.workshops.index(workshop_to_swap)
        # now find best student to swap workshops with
        best_student = None
        current_best_score = 0
        for s in students:
            if s == unhappiest:
                continue
            if workshop_to_swap in s.workshops:
                continue
            # restrict to same time slot
            trade_workshop = s.workshops[workshop_to_swap_idx] 
            if trade_workshop in unhappiest.workshops:
                continue
            
            old_score = unhappiest.unhappiness_score() + s.unhappiness_score()
            
            unhappiest_test_workshops = [x for x in unhappiest.workshops if x != workshop_to_swap]
            unhappiest_test_workshops.append(trade_workshop)
            
            s_test_workshops = [x for x in s.workshops if x != trade_workshop]
            s_test_workshops.append(workshop_to_swap)
            
            new_score = (unhappiest.unhappiness_score(unhappiest_test_workshops) +
                         s.unhappiness_score(s_test_workshops))
            
            if old_score - new_score >= current_best_score:
                best_student = s
            
        if best_student is not None:
            # swap unhappiest's worst workshop with their best match's workshop
            unhappiest.removeWorkshop(workshop_to_swap, workshop_to_swap_idx)  
            trade_workshop = best_student.workshops[workshop_to_swap_idx]
            best_student.removeWorkshop(trade_workshop, workshop_to_swap_idx)
            unhappiest.assignWorkshop(trade_workshop, workshop_to_swap_idx)   
            best_student.assignWorkshop(workshop_to_swap, workshop_to_swap_idx) 
            improvements_counter += 1
            
    #calculate total unhappiness, hopefully better now
    print(sum(s.unhappiness_score() for s in students), improvements_counter)
    
    # print the results for the unhappiest student                
    unhappiest = max(students, key=lambda s: s.unhappiness_score())     
    print(unhappiest.getWorkshopNames())
    for p in unhappiest.preferences:
        print(p.name)
    

def main():
    data_dir = os.path.join(os.getcwd(), 'test_data')
    preferenceFile = os.path.join(data_dir, 'Workshop_Wuensche_160_Personen.xlsx')
    workshopsFile = os.path.join(data_dir, 'workshop_data.xlsx')
    studentFileOut = os.path.join(data_dir, 'test_students_1.xlsx')
    workshopsFileOut = os.path.join(data_dir, 'test_workshops_1.xlsx')
    
    fileIO = FileIO.FileIO(
        preferenceFile, workshopsFile, studentFileOut, workshopsFileOut)
    
    # read in the student preferences and workshop names
    workshops = fileIO.initialiseWorkshops(NUM_SLOTS)
    students = fileIO.initialisePreferences(workshops, NUM_SLOTS)
    
    # this is where the magic happens
    assignWorkshops(workshops, students)
    
    # output data
    fileIO.writeWorkshops(workshops, NUM_SLOTS)
    fileIO.writeStudents(students)
    
if __name__ == '__main__':
    main()