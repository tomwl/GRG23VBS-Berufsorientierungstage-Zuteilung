# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:08:37 2026

@author: tom
"""

class Workshop:
    def __init__(self, name: str, capacity: int):
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
        self.students = []
        self.capacity = capacity
        
    @property
    def name(self):
        return str(self._name)
    
    def resetStudents(self):
        self.students = []
        
    def getStudents(self):
        return self.students
        
    def isFull(self):
        return len(self.students) >= self.capacity