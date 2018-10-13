# coding="utf-8"

import os
import fnmatch
import sys
import re
from htm_object import HtmInfo

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

# Defines the generator ------------------------------------------------------------------------------

gen_find = (os.path.join(path,name) for path, dirlist, filelist in os.walk(top)
                                    for name in fnmatch.filter(filelist,filepat))
file_text_strings = open_file_y(gen_find)
h1s = h1_print(file_text_strings)

# Runs the generator ---------------------------------------------------------------------------------

for h in h1s:
    filename = path_transfer.split("\\")[-1]
    htm_file_object = HtmInfo(filename, path_transfer, h[1], h[2], h[3])
    htm_file_object.add()
    italics_list = h[2]
    
    htm_file_object.add_italics() if italics_list
        
    prospective_sys_param_list = h[3]
    if prospective_sys_param_list:
        htm_file_object.add_params()




    
print "Total number of files           : ", len(HtmInfo.htm_object_list)
print "Files with italics              : ", len(HtmInfo.htm_italics_list)
print "Files with system params (maybe): ", len(HtmInfo.htm_params_list)

itals = [x.htm_path for x in HtmInfo.htm_italics_list]
params = [p.htm_path for p in HtmInfo.htm_params_list]

itals_params = list(set(itals) & set(params))

countb = len(itals_params)
 
print "files with both                 : ", countb

union = list(set(itals) | set(params))

countu = len(union)

print "union of both                   : ", countu