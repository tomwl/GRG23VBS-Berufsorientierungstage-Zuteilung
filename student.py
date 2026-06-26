# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:52:50 2026

@author: tom
"""

import Workshop as ws

class Student:
    def __init__(self, firstname: str, lastname: str, year: int):
        """Constructor for Student

        Parameters
        ----------
        firstname : str
            student's first name.
        lastname : str
            student's last name.
        year : int
            the year they are in e.g. 7 or 8

        Returns
        -------
        None.

        """
        self.firstname = firstname
        self.lastname = lastname
        self.workshops = []
        self.year = year
        self.preferences: list[ws.Workshop] = []
        
    def __str__(self):
        return "{0} {1} in year {2}".format(
            self.firstname, self.lastname, self.year)
    
    def getName(self):
        return "{0} {1}".format(self.firstname, self.lastname)  
    
    def assignPreference(self, preference):
        if not preference is None:
            self.preferences.append(preference)
    
    def assignWorkshop(self, workshop):
        if workshop not in self.workshops:
            self.workshops.append(workshop)
        else:
            # should throw some kind of error here
            pass
        
    def getWorkshopNames(self):
        return [ws.name if not ws is None else "" for ws in self.workshops.values()]
    
    def getWorkshops(self):
        return self.workshops