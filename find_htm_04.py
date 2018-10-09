# coding="utf-8"

import os
import fnmatch
import sys
import re
from htm_objects import HtmInfo
from htm_objects import HtmItalics
from htm_objects import HtmProspectSysParms

def open_file(file):
    with open(file, 'r') as f:
        return f.read()

def open_file_y(file_paths):
    global path_transfer
    for file in file_paths:
        path_transfer = file
        yield open_file(file)
            
def h1_print(file_texts):
    excludeStrings = {'ACTION', 'ALIAS', 'APRS', 'PATH', 'CDATA', 'DATA', 'DXF', 'CHA', 'CHE', 'XML', 'DOCTYPE', 'ICCP', 'FEP', 'RTU', 'SCADA', 'FUNCTION', 'CONTROL'
                      , 'BAD', 'QUALITY', 'ENMAC', 'LIMITBAND', 'NMS', 'OMS', 'ATTRIBUTE', 'PSTN', 'STATUS', 'REPLY', 'VALUE', 'COMPONENT'}
    for text in file_texts:
        temp_text = text.replace('\n', '').replace('\r', '')  # Remove carriage returns and line feeds
        rawHeading = re.findall(r"<h1.+?</h1>", temp_text)  # Remove all other tags
        if rawHeading != []:
            raw = rawHeading[0]
            Heading = re.sub(r"<.*?>", "", raw)
        else:
            Heading = "null"

        find_italics = re.findall(r"<i>.+?</i>", text)
        find_prospective_sys_params_temp = re.findall(r'\b[A-Z,_]{3,60}\b', text)
        find_prospective_sys_params = list(set(find_prospective_sys_params_temp) - excludeStrings)
        
        yield path_transfer, Heading, find_italics, find_prospective_sys_params
            
top = r"C:\test_project"
filepat = "*.htm"
            
gen_find = (os.path.join(path,name) for path, dirlist, filelist in os.walk(top)
                                    for name in fnmatch.filter(filelist,filepat))
file_text_strings = open_file_y(gen_find)
h1s = h1_print(file_text_strings)

count = 0
for h in h1s:
    # print h
    # count += 1

# print count
    


    filename = path_transfer.split("\\")[-1:]
    htm_file_object = HtmInfo(filename[0], path_transfer, h[1])
    # print "Object: ", htm_file_object
    htm_file_object.add()
    italics_list = h[2]
    if italics_list:
        htm_italics_object = HtmItalics(filename[0], path_transfer, h[1], italics_list)
        
    prospective_sys_param_list = h[3]
    if prospective_sys_param_list:
        # print "uuuuu   ", path_transfer
        htm_sys_params_object = HtmProspectSysParms(filename[0], path_transfer, h[1], prospective_sys_param_list)
        # print "IIIIII   ", htm_sys_params_object
    
# print HtmInfo.count
print "#############################################################################\n\n"

file_count = 0
italics_file_count = 0
prosp_sys_param_file_count = 0

for entry in HtmInfo.htm_object_list:
    # print "Path: ", entry.htm_path
    # print "Name: ", entry.htm_name
    # print "Heading: ", entry.htm_h1
    # print "\n\n"
    file_count +=1
    
for entry in HtmItalics.htm_italics_list:
    # print "Path: ", entry.htm_path
    # print "Name: ", entry.htm_name
    # print "Heading: ", entry.htm_h1
    # print "Italics: ", entry.italics_list
    # print "\n\n"
    italics_file_count += 1

for entry in HtmProspectSysParms.htm_params_list:
    # print "Path: ", entry.htm_path
    # print "Name: ", entry.htm_name
    # print "Heading: ", entry.htm_h1
    # print "Params: ", entry.prospective_sys_param_list
    # print "\n\n"
    prosp_sys_param_file_count += 1
    
print "Total number of files           : ", file_count, len(HtmInfo.htm_object_list)
print "Files with italics              : ", italics_file_count, len(HtmItalics.htm_italics_list)
print "Files with system params (maybe): ", prosp_sys_param_file_count, len(HtmProspectSysParms.htm_params_list)


itals = [x.htm_path for x in HtmItalics.htm_italics_list]
params = [p.htm_path for p in HtmProspectSysParms.htm_params_list]

# print itals
# print params

itals_params = list(set(itals) & set(params))
countb = 0
# print itals_params
for d in itals_params:
    # print d
    countb += 1
 
print "files with both                 : ", countb

union = list(set(itals) | set(params))

countu = 0
for u in union:
    # print d
    countu += 1

print "union of both                   : ", countu