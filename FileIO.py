# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:16:22 2026

@author: tom
"""

import pandas as pd
import workshop as ws
import student

class FileIO:
    def __init__(self, pFile, wFile, sFout, wFout):
        self.prefencesFileIn = pFile
        self.workshopsFileIn = wFile
        self.studentsFileOut = sFout
        self.workshopsFileOut = wFout
        