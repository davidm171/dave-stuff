# coding="utf-8"

import os
import fnmatch
import sys
import re
from htm_object import HtmInfo
from time_it import timer
from createSysParamFiles import create_parameter_files


def writefile(file, fileText):
    f = open(file, "w")
    f.write(fileText)
    f.close()

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
            
@timer
def process():

    import config
    
    filepat = "*.htm"

    # Defines the generator ------------------------------------------------------------------------------

    gen_find = (os.path.join(path,name) for path, dirlist, filelist in os.walk(config.build_path)
                                        for name in fnmatch.filter(filelist,filepat))
    file_text_strings = open_file_y(gen_find)
    h1s = h1_print(file_text_strings)

    # Runs the generator ---------------------------------------------------------------------------------

    for h in h1s:
        filename = os.path.split(path_transfer)[1]
        if config.poa_filename == filename:
            HtmInfo.flare_main_path = os.path.split(path_transfer)[0]
            print "Hurray, found poa_main.htm ", path_transfer
            # HtmInfo.poa_filename = path_transfer
            config.flare_content_path = os.path.join(HtmInfo.flare_main_path, "content")
            config.subsystemsDir = os.path.join(HtmInfo.flare_main_path, "Subsystems")
        htm_file_object = HtmInfo(filename, path_transfer, h[1], h[2], h[3])
        htm_file_object.add()
        italics_list = h[2]
        if italics_list:
            htm_file_object.add_italics()
            
        prospective_sys_param_list = h[3]
        if prospective_sys_param_list:
            htm_file_object.add_params()

    # ----------------------------------------------------------------------------------------------------

    print "Total number of files           : ", len(HtmInfo.htm_object_list)
    print "Files with italics              : ", len(HtmInfo.htm_italics_list)
    print "Files with system params (maybe): ", len(HtmInfo.htm_params_list)

    htms = [h.htm_path for h in HtmInfo.htm_object_list]
    itals = [x.htm_path for x in HtmInfo.htm_italics_list]
    params = [p.htm_path for p in HtmInfo.htm_params_list]
    itals_params = list(set(itals) & set(params))
    countb = len(itals_params)
    print "files with both                 : ", countb
    union = list(set(itals) | set(params))
    countu = len(union)
    print "union of both                   : ", countu
    
    
    # Add system parameters sub folder-------------------------------------------------------------------
    lang = config.language
    
    allHtmPaths = [file for file in htms if "Subsystems" in str(file)]
    from createSysParamFiles import create_parameter_files
    
    create_parameter_files(lang, config.build_path, allHtmPaths)

    # Start pricessing -----------------------------------------------------------------------------------
    from add_cross_refs import crossRefs
    from excel_import import import_map

    guideToDirMap = {}
    guideToDirMap = import_map(lang)
    from param_insert import replaceLinks
    
    obj_union = set(HtmInfo.htm_italics_list) | set(HtmInfo.htm_params_list)
    
    for obj in obj_union:
        fileText = open_file(obj.htm_path)
        print "The file to be processed has the path: ", obj.htm_path
        fileText = open_file(obj.htm_path)
        if obj.htm_italics_list:
            fileText = crossRefs(obj, fileText, guideToDirMap)
        
        if obj.htm_params_list:
            prospective = obj.prospective_sys_param_list
            parameters_found_in_file = list(set(prospective) & set(HtmInfo.system_parameters_list))
            if parameters_found_in_file:
                fileText = replaceLinks(fileText, obj, parameters_found_in_file)
                
        print "File processed."
        writefile(obj.htm_path, fileText)

    print "POA file path is:       ", config.poa_filename
    print "Content directory is:   ", config.flare_content_path
    print "Subsystem directory is  ", config.subsystemsDir
    
if __name__ == "__main__":
    process()
