# coding="utf-8"

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
    href = "<a href=\"" +  ellipsis + "content/system_parameters/" + entry + ".htm\" " + "class=\"MCTopicPopup MCTopicPopupHotSpot a aPopup\" data-mc-width=\"auto\" data-mc-height=\"auto\">" + entry + "</a>"
    print "The href is: ", href
    return href
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to find the depth of ellipisis in relative path -------------------------------------------------------------------------
def relPath(file):
    import os
    import config
    lang = config.language
    path = os.path.normpath(file)
    path_list = path.split(os.sep)
    print path_list
    absoluteFileDepth = len(path_list)
    depthCount = absoluteFileDepth
    
    file_path_html = "AdvantageHTML5_" + lang  #.upper()
    while path_list[depthCount-1] != file_path_html:            # This should be constructed for all languages
        depthCount -= 1
    
    depth = absoluteFileDepth - depthCount - 1
    relPath = ""
    for i in range(0, depth):
        relPath = relPath + "../"
        # print "relPath: ", relPath
    
    return relPath
    # ---------------------------------------------------------------------------------------------------------------------------------
# Find the system parameters and replace the text with hyperlinks ---------------------------------------------------------------------------------------------------------
def replaceLinks(fileText, object, parameters_found_in_file):
    import re
    from htm_object import HtmInfo  # Shouldn't have to declare this twice
    
    for hit in parameters_found_in_file:                # this will only find it once in each para, but that's fine?
        # paraHits = re.findall(r"((?:<p|<li).+?[^>#=\"\/]\b[^_]{0}[^_=]\b)".format(hit),fileText)              #Could check here for \ or .htm to stop links being processed.
        paraHits = re.findall(r"((?:<p|<li).+?[^#='\"\/]\b{0}\b[^='])".format(hit),fileText)  
        print "paraHits", paraHits
        if len(paraHits) != 0:
            print "---The prospective parameter is:   ", hit
            
            if hit in parameters_found_in_file:
                paraHit = paraHits[0]
                href = constructHref(hit, object.htm_path)
                newPara = paraHit.replace(hit, href)
                newFileText = fileText.replace(paraHit, newPara)
                fileText = newFileText

    return fileText
                            
    # Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def main():

    # Get a list of the system parameter files, could check body is not empty?-----------------------------------------------------------------------------------------------

    # import config
    # from htm_object import HtmInfo
    
    # op_dir = config.flare_content_path + "\system_parameters"
    
    # if os.path.exists(op_dir):                        # This makes sure the system_parameter directory exists - is this required?
        # print "op_dir is: ", op_dir
        # sysParamList = HtmInfo.system_parameters_list

        # Find the system parameters and replace the text with hyperlinks --------------------------------------------------------------------------------------------------------
        # SysParamFoundList = replaceLinks(op_dir, sysParamList)

if __name__ == '__main__':
    import os, re
    lang = 'us'
    build_path = r"C:\test_project"
    # op_dir = build_path + "\Output\AdvantageHTML5_" + lang + "\content\system_parameters"
    from find_htm import process
    process()
    # main()
