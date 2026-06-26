# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:08:37 2026

@author: tom
"""

class Workshop:
    def __init__(self, name: str, capacity: int, num_slots: int):
        """Constructor for Workshop

        Parameters
        ----------
        name : str
            name of workshop.
        capacity : int
            how many students allowed per day.
            
        Returns
        -------
        None.

        """
        self._name = name
        self.students = {}
        self.capacity = capacity
        self.n_slots = num_slots
        
    def __str__(self):
        result = "Name: {0}, \n".format(
            self.name)
        for i in range(self.n_slots):
            tmp = "Slot {0}: {1} students\n".format(i, len(self.students[i]))
            for s in self.students[i]:
                tmp += "{}\n".format(s)
            result += tmp
        return result 
    
    @property
    def name(self):
        return str(self._name)
    
    def resetStudents(self):
        for i in range(self.n_slots):
            self.students[i] = []
        
    def getStudentsInSlot(self, slot):
        return self.students[slot]
        
    def isSlotFull(self, slot):
        return len(self.students[slot]) >= self.capacity
    
    def addStudent(self, student, slot):
        allStudents = [item for sublist in self.students.values() for item in sublist]
        if student not in allStudents:
            self.students[slot].append(student)
        else:
            # should throw some kind of error here
            raise Exception("Error: workshop already has this student: {0}"
                            .format(student.getName()))
            