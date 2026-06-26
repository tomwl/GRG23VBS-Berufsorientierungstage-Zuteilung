# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:05:26 2026

@author: tom
"""

import FileIO
import student
import workshop

NUM_WORKSHOPS = 1 # how many workshops should each student visit

def assignYearGroup(students, unassigned):
    for s in students:
        # loop through and try brute force assignment of workshops to students 
        for p in s.preferences:
            if len(s.getWorkshops()) == NUM_WORKSHOPS:
                break
            if not p.isFull():
                s.assignWorkshop(p)
        if len(s.getWorkshops()) < NUM_WORKSHOPS:
            # we have a problem, they have less than 3 assigned
            print("Error, student missing workshop")
            unassigned.append(s)

def assignWorkshops(workshops, students):
    """
    Main function for workshop assignment

    Returns
    -------
    None.

    """
    unassignedStudents = []
    for w in workshops:
        w.resetStudents()
    # get the 8th year students first
    target_students = [x for x in students if x.year == 8]
    assignYearGroup(target_students, unassignedStudents)
    
    target_students = [x for x in students if x.year == 7] # now do 7th year
    assignYearGroup(target_students, unassignedStudents)
    

def main():
    # read in the student preferences and workshop names
    
    # this is where the magic happens
    assignWorkshops(workshops, students)
    
    # output data
    
if __name__ == '__main__':
    main()