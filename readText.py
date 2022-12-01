# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 13:40:33 2022

@author: zxie
"""
def readTest(textFromPDF):
    textFromPDF = textFromPDF.replace("\n\n", "\n")
    lines = textFromPDF.split("\n")
    for row in range(len(lines)):
        
        try:
            if "Ohms" in lines[row]:
                flhr = lines[row+1].split(" ")
                wdg_tr = flhr[3]
                brg_tr = flhr[5]
                
            if "STATOR I2R LOSS" in lines[row]:
                pri = lines[row+1].split(" ")[2]
                core = lines[row+2].split(" ")[2]
                sec = lines[row+3].split(" ")[5]
                wf = lines[row+4].split(" ")[1]
            
            if "STRAY-LOAD LOSS" in lines[row]:
                line = lines[row].replace(" | ", " ")
                stray = line.split(" ")[4]
        except:
            wdg_tr = 0
            brg_tr = 0
            pri = 0
            core = 0
            sec = 0
            wf = 0
            stray = 0
    
    testData = {}
    testData["wdg temp rise"] = wdg_tr
    testData["brg temp rise"] = brg_tr
    testData["primary"] = pri
    testData["secondary"] = sec
    testData["core"] = core
    testData["Windage and Friction"] = wf
    testData["stray"] = stray
    
    return testData

