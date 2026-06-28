# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:52:50 2026

@author: tom
"""

import workshop as ws

class Student:
    WEIGHT_MAP = {
        0: 0,  1: 1,  2: 2,      # Small values
        3: 4,  4: 8,  5: 12, 6: 16, # Moderately large values
        7: 25, 8: 40, 9: 80     # Heavily weighted values
    }
    
    def __init__(self, firstname: str, lastname: str, year: int, nslots: int):
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
        # the final workshops they will visit, these are ordered by slot
        # e.g. workshops[0] will be in the first slot etc.
        self.workshops: list[ws.Workshop] = []
        for _ in range(nslots):
            self.workshops.append(None)
        self.year = year
        # the workshops they want to visit
        # these should be ordered as first one is fav.
        self.preferences: list[ws.Workshop] = []
        
    def __str__(self):
        return "{0} {1} in year {2}".format(
            self.firstname, self.lastname, self.year)
    
    def getName(self):
        return "{0} {1}".format(self.firstname, self.lastname) 
    
    def resetWorkshops(self):
        for i in range(len(self.workshops)):
            self.workshops[i] = None
    
    def assignPreference(self, preference):
        if not preference is None:
            self.preferences.append(preference)
    
    def assignWorkshop(self, workshop, slot):
        if workshop not in self.workshops:
            self.workshops[slot] = workshop
            workshop.addStudentToSlot(self, slot)
        else:
            # should throw some kind of error here
            raise Exception("Error: student already has this workshop: {0}"
                            .format(workshop.name))
            
    def removeWorkshop(self, workshop, slot):
        ws = next((item for item in self.workshops if item == workshop), None)
        if ws is None:
            raise Exception("Error: trying to remove workshop from student that doesn't have it")
        ws.removeStudentFromSlot(self, slot)
        self.workshops[slot] = None
        
    def getWorkshopNames(self):
        return [ws.name if not ws is None else "" for ws in self.workshops]
    
    def getWorkshops(self):
        return self.workshops
    
    def unhappiness_score(self, workshops=None):
        """
        This uses the weight map at the top of the class to rank 
        a student's unhappiness with their workshop assignments

        Parameters
        ----------
        workshops : List of Workshop, optional
            The default is None.

        Returns
        -------
        score : float
            An unhappiness score.

        """
        score = 0
        if workshops is None:
            workshops = self.workshops
        for workshop in workshops:
            rank = self.WEIGHT_MAP[self.preferences.index(workshop)]
            score += rank
        return score
    
    def getLowestPreferenceWorkshop(self):
        return max(self.workshops, key=self.preferences.index, default = None)