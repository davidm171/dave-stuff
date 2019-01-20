# coding="utf-8"


# def add_parameter_references(lang, build_path, htm_params_list):
    
    # import string, os, re
    # import codecs, sys
    # codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
    # sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)                                        # Gets rid of coding errors when print to screen

    # reload(sys)  
    # sys.setdefaultencoding('utf8')

# open the file-----------------------------------------------------------------------------------------------------------------------------------------------------------
def open_file(file_name):
    f1 = open(file_name, "r")
    fileText = f1.read()
    f1.close()
    return fileText
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Write and close file ----------------------------------------------------------------------------------------------------------------------------------------------------
def writefile(file,fileText):
    f = open(file, "w")
    f.write(fileText)
    f.close()
# -----------------------------------------------------------------------------------------------------------------------------------
# Create a popup href for the system parameter ----------------------------------------------------------------------------------------------------------------------------                
def constructHref(entry, file):
    ellipsis = relPath(file)
    print "Ellipsis: ", ellipsis
    href = "<a href=\"" +  ellipsis + "content/system_parameters/" + entry + ".htm\" " + "class=\"MCTopicPopup MCTopicPopupHotSpot a aPopup\" data-mc-width=\"auto\" data-mc-height=\"auto\">" + entry + "</a>"
    print "The href is: ", href
    return href
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to find the depth of ellipisis in relative path -------------------------------------------------------------------------
def relPath(file):
    path = os.path.normpath(file)
    path_list = path.split(os.sep)
    print path_list
    absoluteFileDepth = len(path_list)
    depthCount = absoluteFileDepth
    
    file_path_html = "AdvantageHTML5_" + lang  #.upper()
    while path_list[depthCount-1] != file_path_html:            # This should be constructed for all languages
        depthCount -= 1
        print "depthCount is: ", depthCount
    
    depth = absoluteFileDepth - depthCount - 1        
    print "Depth is: ", absoluteFileDepth - depthCount - 1
    relPath = ""
    for i in range(0, depth):
        relPath = relPath + "../"
        print "relPath: ", relPath
    
    # ellipsis = os.path.normpath(relPath)                            This changes it to a dos path?
    print "The ELLIPSIS is: ", relPath
    return relPath
    # ---------------------------------------------------------------------------------------------------------------------------------
# Find the system parameters and replace the text with hyperlinks ---------------------------------------------------------------------------------------------------------
def replaceLinks(path, sysParamList):
    # htmList = findHtm(path)
    excludeStrings = ['CDADA', 'DXF', 'CHA', 'CHE', 'XML', 'DOCTYPE', 'ICCP', 'FEP', 'RTU']
    SysParamFoundList = []
    for object in HtmInfo.htm_params_list:
        fileText = open_file(object.htm_path)                        # Does this need to be opened here
        # Get prospective hits from object
        prospective = object.prospective_sys_param_list
        print "prospective", prospective
        print "dibble"
        print "Processing ", object.htm_path, " for system parameters..."
        
        parameters_found_in_file = []
        for pros in prospective:
            if pros in sysParamList:
                parameters_found_in_file.append(pros)
        print "PArameters found in file: ", parameters_found_in_file
        if len(parameters_found_in_file) != 0:
        
            for hit in parameters_found_in_file:                # this will only find it once in each para, but that's fine?
                # paraHits = re.findall(r"((?:<p|<li).+?[^>#=\"\/]\b[^_]{0}[^_=]\b)".format(hit),fileText)              #Could check here for \ or .htm to stop links being processed.
                paraHits = re.findall(r"((?:<p|<li).+?[^#='\"\/]\b{0}\b[^='])".format(hit),fileText)  
                print "paraHits", paraHits
                if len(paraHits) != 0:
                    print "---The sentence is             :   ", paraHits[0]
                    print "---The prospective parameter is:   ", hit
                    
                    if hit in sysParamList:
                        print "---                            :   ", hit, " is a system parameter"
                        paraHit = paraHits[0]
                        print ">>", paraHit
                        href = constructHref(hit, object.htm_path)
                        newPara = paraHit.replace(hit, href)
                        print "---The new sentence is         :   ", newPara, "\n\n"
                        newFileText = fileText.replace(paraHit, newPara)
                        fileText = newFileText
                        # writefile(file, fileText)
                                            
                
            writefile(object.htm_path, fileText)
        print "dibble 2"
                            
    # Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():

    # Get a list of the system parameter files, could check body is not empty?-----------------------------------------------------------------------------------------------

    op_dir = build_path + "\Output\AdvantageHTML5_" + lang + "\content\system_parameters"
    
    if os.path.exists(op_dir):                        # This makes sure the system_parameter directory exists
        print "op_dir is: ", op_dir
        
        filenames = next(os.walk(op_dir))[2]
        sysParamList = []
        for file in filenames:
            sysParamList.append(file[:-4])
            print file

        path = build_path +"\Output" + "\AdvantageHTML5_" + lang + "\Subsystems"

        # Find the system parameters and replace the text with hyperlinks --------------------------------------------------------------------------------------------------------
        SysParamFoundList = replaceLinks(path, sysParamList)

if __name__ == '__main__':
    import os, re
    lang = 'us'
    build_path = r"C:\test_project"
    op_dir = build_path + "\Output\AdvantageHTML5_" + lang + "\content\system_parameters"
    from find_htm import process
    from htm_object import HtmInfo
    process()
    main()
