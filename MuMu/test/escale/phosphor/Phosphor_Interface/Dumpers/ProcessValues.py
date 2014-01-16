'''
Macro to read in text file from dumper and create LaTeX tables for photon resolution and scaling
Valere Lambert, 27 August 2013
'''

import os
import socket
import ROOT
from ROOT import *
import JPsi.MuMu.common.roofit as roo

ROOT.gSystem.Load('libJPsiMuMu')

def main():
    #file from output of JPsi/MuMu/test/escale/phosphor/Phosphor_Interface/Modified_phosphorDumper.py
    read_file('out.txt')
# end main    
    
## -------------------------------------------------------------------
def read_file (infile):
    text = open(infile, 'r')

    DataEntry = []
    for line in text:
        # Remove commented lines
        tag = line[0:1]
        if tag != "#":
            # Fill arrays      0: pile up  ,  1: data    ,  2: detector   , 3: R9      ,  4: Pt       , 5: Correction    ,6 : value     
            DataEntry.append([int(line[0:1]),int(line[2:3]),int(line[4:5]),int(line[6:7]),int(line[8:9]),int(line[10:11]),float(line[12:17])])

    # Arrays to form pile up and r9 pairs        
    HighPU = []
    LowPU  = []
    AllPUHR = []
    AllPULR = []
    for i in range(len(DataEntry)):
        # All Pile Up: High R9
        if DataEntry[i][0] == 2 and DataEntry[i][3] == 0:
            AllPUHR.append(DataEntry[i])
            for k in range(len(DataEntry)):
                # Choose matching Low R9
                if DataEntry[k][3] == 1 and DataEntry[k][0:3] == DataEntry[i][0:3] and DataEntry[k][4:6] == DataEntry[i][4:6]:
                   AllPULR.append(DataEntry[k]) 
        # Determine High Pile Up sets
        elif DataEntry[i][0] == 0:
            HighPU.append(DataEntry[i])
            for j in range(len(DataEntry)):
                # Choose matching Low Pile Up
                if DataEntry[j][0] == 1 and DataEntry[j][1:6] == DataEntry[i][1:6]:
                    LowPU.append(DataEntry[j])

    # Event Arrays                
    MC_High_EB_res   = []
    MC_Low_EB_res    = []
    MC_High_EE_res   = []
    MC_Low_EE_res    = []
    Data_High_EB_res = []
    Data_Low_EB_res  = []
    Data_High_EE_res = []
    Data_Low_EE_res  = []

    MC_High_EB_scale   = []
    MC_Low_EB_scale    = []
    MC_High_EE_scale   = []
    MC_Low_EE_scale    = []
    Data_High_EB_scale = []
    Data_Low_EB_scale  = []
    Data_High_EE_scale = []
    Data_Low_EE_scale  = []

    MC_All_EB_res = []
    MC_All_EE_res = []
    Data_All_EB_res = []
    Data_All_EE_res = []

    MC_All_EB_scale = []
    MC_All_EE_scale = []
    Data_All_EB_scale = []
    Data_All_EE_scale = []

    MC_EB_scale = []
    MC_EB_res = []
    Data_EB_scale = []
    Data_EB_res = []
    MC_EE_scale = []
    MC_EE_res = []
    Data_EE_scale = []
    Data_EE_res = []

    
    '''
    Fill all pile up arrays :  ( pT bin ,  High R9  ,  Low R9 )
    '''
    for element in range(len(AllPUHR)):
        # Monte Carlo
        if AllPUHR[element][1] == 0:
            # Barrel
            if AllPUHR[element][2] == 0:
                #Scale
                if AllPUHR[element][5] == 0:   
                    MC_EB_scale.append([AllPUHR[element][4],AllPUHR[element][6],AllPULR[element][6]])
                #Reolution
                if AllPUHR[element][5] == 1:
                    MC_EB_res.append([AllPUHR[element][4],AllPUHR[element][6],AllPULR[element][6]])
            # End Caps        
            if AllPUHR[element][2] == 1:
                #Scale
                if AllPUHR[element][5] == 0:
                    MC_EE_scale.append([AllPUHR[element][4],AllPUHR[element][6],AllPULR[element][6]])
                #Resolution    
                if AllPUHR[element][5] == 1:
                    MC_EE_res.append([AllPUHR[element][4],AllPUHR[element][6],AllPULR[element][6]])
        # Data            
        elif AllPUHR[element][1] == 1:
            #Barrel
            if AllPUHR[element][2] == 0:
                #Scale
                if AllPUHR[element][5] == 0:
                    Data_EB_scale.append([AllPUHR[element][4],AllPUHR[element][6],AllPULR[element][6]])
                #Resolution
                if AllPUHR[element][5] == 1:
                    Data_EB_res.append([AllPUHR[element][4],AllPUHR[element][6],AllPULR[element][6]])
            #End Caps
            if AllPUHR[element][2] == 1:
                #Scale
                if AllPUHR[element][5] == 0:
                    Data_EE_scale.append([AllPUHR[element][4],AllPUHR[element][6],AllPULR[element][6]])
                #Resolution
                if AllPUHR[element][5] == 1:
                    Data_EE_res.append([AllPUHR[element][4],AllPUHR[element][6],AllPULR[element][6]])
                    
    '''
    Fill high/low pile up arrays :  ( pT bin ,  High PU  ,  Low PU )
    '''
    for l in range(len(HighPU)):
        # Monte Carlo
        if HighPU[l][1] == 0:
            #Barrel
            if HighPU[l][2] == 0:
                #High R9
                if HighPU[l][3] == 0:
                    #Scale
                    if HighPU[l][5] == 0:
                        MC_High_EB_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        MC_High_EB_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                #Low R9
                if HighPU[l][3] == 1:
                    #Scale
                    if HighPU[l][5] == 0:
                        MC_Low_EB_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resoluton
                    if HighPU[l][5] == 1:
                        MC_Low_EB_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                #All R9
                if HighPU[l][3] == 2:
                    #Scale
                    if HighPU[l][5] == 0:
                        MC_All_EB_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution    
                    if HighPU[l][5] == 1:
                        MC_All_EB_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
            #End Caps            
            if HighPU[l][2] == 1:
                #High R9
                if HighPU[l][3] == 0:
                    #Scale
                    if HighPU[l][5] == 0:
                        MC_High_EE_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        MC_High_EE_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                #Low R9
                if HighPU[l][3] == 1:
                    #Scale
                    if HighPU[l][5] == 0:
                        MC_Low_EE_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        MC_Low_EE_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                #All R9
                if HighPU[l][3] == 2:
                    #Scale
                    if HighPU[l][5] == 0:
                        MC_All_EE_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        MC_All_EE_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
        #Data
        if HighPU[l][1] == 1:
            #Barrel
            if HighPU[l][2] == 0:
                #High R9
                if HighPU[l][3] == 0:
                    #Scale
                    if HighPU[l][5] == 0:
                        Data_High_EB_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        Data_High_EB_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                #Low R9
                if HighPU[l][3] == 1:
                    #Scale
                    if HighPU[l][5] == 0:
                        Data_Low_EB_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        Data_Low_EB_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                #All R9
                if HighPU[l][3] == 2:
                    #Scale
                    if HighPU[l][5] == 0:
                        Data_All_EB_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        Data_All_EB_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
            #End Caps
            if HighPU[l][2] == 1:
                #High R9
                if HighPU[l][3] == 0:
                    #Scale
                    if HighPU[l][5] == 0:
                        Data_High_EE_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        Data_High_EE_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                #Low R9
                if HighPU[l][3] == 1:
                    #Scale
                    if HighPU[l][5] == 0:
                        Data_Low_EE_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        Data_Low_EE_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                #All R9
                if HighPU[l][3] == 2:
                    #Scale
                    if HighPU[l][5] == 0:
                        Data_All_EE_scale.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])
                    #Resolution
                    if HighPU[l][5] == 1:
                        Data_All_EE_res.append([HighPU[l][4],HighPU[l][6],LowPU[l][6]])


#=========================================================================================================#
#                                          Print out LaTeX Tables                                         #
#=========================================================================================================#
    get_pt_label = {
        0 : '10 to 12',
        1 : '12 to 15',
        2 : '15 to 20',
        3 : '20 to 25',
        4 : '25 to 35',
        5 : '35 to 999',
        6 : '20 to 999',
        }

    # Table for High and Low Pile UP
    #Data Resolutions
    print "\\begin{multicols}{2}"
    print "\\begin{center}"
    print "\\begin{tabular}{|c|c|c|} \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Data Resolution : High R9}} \\\\ \hline"
    print " Pt Bin  &  High Pile Up  &  Low Pile Up \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry1 in range(len(Data_High_EB_res)):
        print get_pt_label[Data_High_EB_res[entry1][0]],  " & ", Data_High_EB_res[entry1][1], " & ", Data_High_EB_res[entry1][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry2 in range(len(Data_High_EE_res)):
        print get_pt_label[Data_High_EE_res[entry2][0]],  " & ", Data_High_EE_res[entry2][1], " & ", Data_High_EE_res[entry2][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Data Resolution : Low R9}} \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry3 in range(len(Data_Low_EB_res)):
        print get_pt_label[Data_Low_EB_res[entry3][0]],  " & ", Data_Low_EB_res[entry3][1], " & ", Data_Low_EB_res[entry3][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry4 in range(len(Data_Low_EE_res)):
        print get_pt_label[Data_Low_EE_res[entry4][0]],  " & ", Data_Low_EE_res[entry4][1], " & ", Data_Low_EE_res[entry4][2], "\\\\ \hline"
    print "\end{tabular}"
    print "\end{center}"
    
    #Monte Carlo Resolutions
    print "\\begin{center}"
    print "\\begin{tabular}{|c|c|c|} \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Monte Carlo Resolution : High R9}} \\\\ \hline"
    print " Pt Bin  &  High Pile Up  &  Low Pile Up \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry5 in range(len(MC_High_EB_res)):
        print get_pt_label[MC_High_EB_res[entry5][0]],  " & ", MC_High_EB_res[entry5][1], " & ", MC_High_EB_res[entry5][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry6 in range(len(MC_High_EE_res)):
        print get_pt_label[MC_High_EE_res[entry6][0]],  " & ", MC_High_EE_res[entry6][1], " & ", MC_High_EE_res[entry6][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Monte Carlo Resolution : Low R9}} \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry7 in range(len(MC_Low_EB_res)):
        print get_pt_label[MC_Low_EB_res[entry7][0]],  " & ", MC_Low_EB_res[entry7][1], " & ", MC_Low_EB_res[entry7][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry8 in range(len(MC_Low_EE_res)):
        print get_pt_label[MC_Low_EE_res[entry8][0]],  " & ", MC_Low_EE_res[entry8][1], " & ", MC_Low_EE_res[entry8][2], "\\\\ \hline"
    print "\end{tabular}"
    print "\end{center}"
    print "\end{multicols}"

    #Data Scalings
    print "\clearpage"
    print "\\begin{multicols}{2}"
    print "\\begin{center}"
    print "\\begin{tabular}{|c|c|c|} \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Data Scale : High R9}} \\\\ \hline"
    print " Pt Bin  &  High Pile Up  &  Low Pile Up \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry1 in range(len(Data_High_EB_scale)):
        print get_pt_label[Data_High_EB_scale[entry1][0]],  " & ", Data_High_EB_scale[entry1][1], " & ", Data_High_EB_scale[entry1][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry2 in range(len(Data_High_EE_scale)):
        print get_pt_label[Data_High_EE_scale[entry2][0]],  " & ", Data_High_EE_scale[entry2][1], " & ", Data_High_EE_scale[entry2][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Data Scale : Low R9}} \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry3 in range(len(Data_Low_EB_scale)):
        print get_pt_label[Data_Low_EB_scale[entry3][0]],  " & ", Data_Low_EB_scale[entry3][1], " & ", Data_Low_EB_scale[entry3][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry4 in range(len(Data_Low_EE_scale)):
        print get_pt_label[Data_Low_EE_scale[entry4][0]],  " & ", Data_Low_EE_scale[entry4][1], " & ", Data_Low_EE_scale[entry4][2], "\\\\ \hline"
    print "\end{tabular}"
    print "\end{center}"
    print "\\begin{center}"

    #Monte Carlo Scalings
    print "\\begin{tabular}{|c|c|c|} \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Monte Carlo Scale : High R9}} \\\\ \hline"
    print " Pt Bin  &  High Pile Up  &  Low Pile Up \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry5 in range(len(MC_High_EB_scale)):
        print get_pt_label[MC_High_EB_scale[entry5][0]],  " & ", MC_High_EB_scale[entry5][1], " & ", MC_High_EB_scale[entry5][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry6 in range(len(MC_High_EE_scale)):
        print get_pt_label[MC_High_EE_scale[entry6][0]],  " & ", MC_High_EE_scale[entry6][1], " & ", MC_High_EE_scale[entry6][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Monte Carlo Scale : Low R9}} \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry7 in range(len(MC_Low_EB_scale)):
        print get_pt_label[MC_Low_EB_scale[entry7][0]],  " & ", MC_Low_EB_scale[entry7][1], " & ", MC_Low_EB_scale[entry7][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry8 in range(len(MC_Low_EE_scale)):
        print get_pt_label[MC_Low_EE_scale[entry8][0]],  " & ", MC_Low_EE_scale[entry8][1], " & ", MC_Low_EE_scale[entry8][2], "\\\\ \hline"
    print "\end{tabular}"
    print "\end{center}"
    print "\end{multicols}"


    # All R9 Tables
    #Resolutions
    print "\clearpage"
    print "\\begin{multicols}{2}"
    print "\\begin{center}"
    print "\\begin{tabular}{|c|c|c|} \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Monte Carlo Resolution : All R9}} \\\\ \hline"
    print " Pt Bin  &  High Pile Up  &  Low Pile Up \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry5 in range(len(MC_All_EB_res)):
        print get_pt_label[MC_All_EB_res[entry5][0]],  " & ", MC_All_EB_res[entry5][1], " & ", MC_All_EB_res[entry5][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry6 in range(len(MC_All_EE_res)):
        print get_pt_label[MC_All_EE_res[entry6][0]],  " & ", MC_All_EE_res[entry6][1], " & ", MC_All_EE_res[entry6][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Data Resolution : All R9}} \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry7 in range(len(Data_All_EB_res)):
        print get_pt_label[Data_All_EB_res[entry7][0]],  " & ", Data_All_EB_res[entry7][1], " & ", Data_All_EB_res[entry7][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry8 in range(len(Data_All_EE_res)):
        print get_pt_label[Data_All_EE_res[entry8][0]],  " & ", Data_All_EE_res[entry8][1], " & ", Data_All_EE_res[entry8][2], "\\\\ \hline"
    print "\end{tabular}"
    print "\end{center}"

    #Scalings
    print "\\begin{center}"
    print "\\begin{tabular}{|c|c|c|} \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Monte Carlo Scale : All R9}} \\\\ \hline"
    print " Pt Bin  &  High Pile Up  &  Low Pile Up \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry5 in range(len(MC_All_EB_scale)):
        print get_pt_label[MC_All_EB_scale[entry5][0]],  " & ", MC_All_EB_scale[entry5][1], " & ", MC_All_EB_scale[entry5][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry6 in range(len(MC_All_EE_scale)):
        print get_pt_label[MC_All_EE_scale[entry6][0]],  " & ", MC_All_EE_scale[entry6][1], " & ", MC_All_EE_scale[entry6][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Data Scale : All R9}} \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry7 in range(len(Data_All_EB_scale)):
        print get_pt_label[Data_All_EB_scale[entry7][0]],  " & ", Data_All_EB_scale[entry7][1], " & ", Data_All_EB_scale[entry7][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry8 in range(len(Data_All_EE_scale)):
        print get_pt_label[Data_All_EE_scale[entry8][0]],  " & ", Data_All_EE_scale[entry8][1], " & ", Data_All_EE_scale[entry8][2], "\\\\ \hline"
    print "\end{tabular}"
    print "\end{center}"
    print "\end{multicols}"


    # All Pile Up Tables
    #Resolutions
    print "\clearpage"
    print "\\begin{multicols}{2}"
    print "\\begin{center}"
    print "\\begin{tabular}{|c|c|c|} \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Monte Carlo Resolution}} \\\\ \hline"
    print " Pt Bin  &  High R9  &  Low R9 \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry5 in range(len(MC_EB_res)):
        print get_pt_label[MC_EB_res[entry5][0]],  " & ", MC_EB_res[entry5][1], " & ", MC_EB_res[entry5][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry6 in range(len(MC_EE_res)):
        print get_pt_label[MC_EE_res[entry6][0]],  " & ", MC_EE_res[entry6][1], " & ", MC_EE_res[entry6][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Data Resolution}} \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry7 in range(len(Data_EB_res)):
        print get_pt_label[Data_EB_res[entry7][0]],  " & ", Data_EB_res[entry7][1], " & ", Data_EB_res[entry7][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry8 in range(len(Data_EE_res)):
        print get_pt_label[Data_EE_res[entry8][0]],  " & ", Data_EE_res[entry8][1], " & ", Data_EE_res[entry8][2], "\\\\ \hline"
    print "\end{tabular}"
    print "\end{center}"

    #Scalings
    print "\\begin{center}"
    print "\\begin{tabular}{|c|c|c|} \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Monte Carlo Scale}} \\\\ \hline"
    print " Pt Bin  &  High R9  &  Low R9 \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry5 in range(len(MC_EB_scale)):
        print get_pt_label[MC_EB_scale[entry5][0]],  " & ", MC_EB_scale[entry5][1], " & ", MC_EB_scale[entry5][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry6 in range(len(MC_EE_scale)):
        print get_pt_label[MC_EE_scale[entry6][0]],  " & ", MC_EE_scale[entry6][1], " & ", MC_EE_scale[entry6][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{\\textbf{Data Scale}} \\\\ \hline"
    print "\multicolumn{3}{|c|}{Barrel} \\\\ \hline"
    for entry7 in range(len(Data_EB_scale)):
        print get_pt_label[Data_EB_scale[entry7][0]],  " & ", Data_EB_scale[entry7][1], " & ", Data_EB_scale[entry7][2], "\\\\ \hline"
    print "\multicolumn{3}{|c|}{End Caps} \\\\ \hline"
    for entry8 in range(len(Data_EE_scale)):
        print get_pt_label[Data_EE_scale[entry8][0]],  " & ", Data_EE_scale[entry8][1], " & ", Data_EE_scale[entry8][2], "\\\\ \hline"
    print "\end{tabular}"
    print "\end{center}"
    print "\end{multicols}"
                                                                        
##---------------------------------------------------------------------
if __name__ == '__main__':
    main()
    
