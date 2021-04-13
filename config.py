#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 19:41:40 2021

@author: zhu
"""

import logging

FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
LOG_FILE = "exchange.log"

def getLogger(logger_name):
   
    logger = logging.getLogger(logger_name)
   
    if not logger.hasHandlers():
       file_handler = logging.FileHandler(LOG_FILE)
       file_handler.setFormatter(FORMATTER)
       logger.addHandler(file_handler)
       
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    print("Testing ")
   
    return logger