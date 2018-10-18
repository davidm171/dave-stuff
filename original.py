# coding="utf-8"
# Create directory of all system parameter htms by parsing relevant pages

def create_parameter_files(lang, build_path):
    # open the file-----------------------------------------------------------------------------------------------------------------------------------------------------------
    def open_file(file_name):
        f1 = open(file_name, "r")
        fileText = f1.read()
        f1.close()
        return fileText
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Write and close file ----------------------------------------------------------------------------------------------------------------------------------------------------
    def writefile(file,fileText):
        print "++The file being written is:" , file
        try: 
            f = open(file, "w")
            f.write(fileText)
            f.close()
        except IOError:
            print "Can't write file: ", file
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Function to extract system parameter name from h6----------------------------------------------------------------------------------------------------------------------
    def processHeading(name):
        # name = re.sub(r"\n", "", name)              ### This removes carriage returns which appear in h6s for no known reason
        
        nameP = name.replace(" ", "")                                # Removes spaces so no issue with spaces before colon
        colonPosition = string.find(nameP, ":")
        if colonPosition != -1:
            parameterText = nameP[:colonPosition]
        else:
            parameterText = nameP
        
        parameterText = parameterText.strip()
        return parameterText
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Function to find all htms under path ------------------------------------------------------------------------------------------------------------------------------------
    def findHtm(path):
        htmfiles = [os.path.join(root, name)
                    for root, dirs, files in os.walk(path)
                    for name in files
                    if name.endswith(".htm")]
        return htmfiles
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def filePaths(path,systemParameterFileList):
        systemParameterFilePaths = []
        for htmPath in path:
            if os.path.split(htmPath)[1] in systemParameterFileList:
                systemParameterFilePaths.append(htmPath)

        return systemParameterFilePaths
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    # Function to find system parameters in file list -------------------------------------------------------------------------------------------------------------------------
    def getSystemParameters(systemParameterFilePaths):
        sysParamList = []
        sysParamDict = {}
        lastParameterInFile = []
        for file in systemParameterFilePaths:
            fileText = open_file(file)
            root = ET.fromstring(fileText)
            # print "The root tag is: ", root
            
            # for h6 in root.findall("body/h6"):
                # h6.text.encode('utf8')
                # yield h6.text
            
            # gen = (h6.text for h6 in root.findall("body/h6") if h6,text is not None)
            
            # for s in gen:
                # print s.encode('utf8'), type(s)

            # for h6 in root.findall("body/h6"):
                # print file
                # print type(h6)
                # try:
                    # if h6.text is not None:
                        # print h6.text.encode('utf8')
                    # else:
                        # print "None Found"
                # except (TypeError, ValueError) as error:
                    # print "TypeError", error
            # print(ET.tostring(root, encoding='utf8').decode('utf8'))
            # h6_list = [elem for elem in root.iter() if elem.tag == "h6"]
            # print h6_list
            
            rawHeading = re.findall(r"<h6.+?</h6>", fileText)
            print rawHeading
            
            
            # for h6 in root.iterfind('body/h6'):
                # if h6.text is not None:
                    # name = h6.text
                    # print "Name is--", name, "---"
                    # print "Parameter is--", processHeading(name).encode('utf-8'), "---"
                    # print "The filepath is: ", file
                # else:
                    # print "There is a bookmark here"
                    # print "The tag is ", 
                    # bookmark = h6.find('a')                                            #Finds the child a (bookmark) of an h6
                    # print "The bookmark is: ", bookmark.attrib
                    # print "The parameter is: ", h6[0].tail                        #Finds the h6 if there is a bookmark
                    # name = h6[0].tail
                
                # parameterText = processHeading(name)
                # sysParamList.append(parameterText)
                # sysParamDict[parameterText] = file
                
            # lastParameter = processHeading(name)
            # lastParameterInFile.append(lastParameter)                                    # Keep a record of the last parameter in each file    
        # print "The last parameters are: ", lastParameterInFile, "\n\n" 
                        
        # return sysParamList, sysParamDict, lastParameterInFile 

    # Create an htm file for all the parameters in the list ----------------------------------------------------------------------------------------------------------
    def createHtmlFiles(sysParamList, sysParamDict, lastParameterInFile):
        for param in sysParamList:
            index = sysParamList.index(param)
            if param not in lastParameterInFile:
                nextIndex = index +1
                print "Hurray! ", param, " is in main list at position ", index, "Next entry is: ", sysParamList[nextIndex] ###  This doesn't check for the end of the file
                nextParam = sysParamList[nextIndex]
                endString = "<h6>" + nextParam
            else:
                print "The parameter is the last in the topic"
                endString = "<p class=\"hide\">"
                
            if sysParamDict.has_key(param):
                print "\n\nThe parameter ", param, " is in ", sysParamDict[param]
                filePath = sysParamDict[param]
                fileText = open_file(filePath).decode('utf-8')        ### change this to remove any a tags
                fileText = re.sub(r"<a name=(.*?)<\/a>", "",fileText)  ### this line removes all the a tags in the string
                startString = "<h6>" + param
                # print "THE FILE IS: /n", fileText
                startIndex = fileText.find(startString)
                tempText = fileText[startIndex:]
                endIndex = tempText.find(endString)
                print "\n @@@The tempText is: ", tempText.encode('utf-8')
                parameterText = tempText[:endIndex]
                parameterText = re.sub(r"<a.*?>", "<i>",parameterText)                 # Two lines remove cross references in sys param text
                parameterText = re.sub(r"</a>", "</i>",parameterText)
                print "\n @@@The parameterText is: ", parameterText.encode('utf-8')
                createParameterFile(parameterText, param, writeDestination)
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    def createParameterFile(parameterText, param, writeDestination):
        startHtml = """<!DOCTYPE html>
    <html xmlns:MadCap="http://www.madcapsoftware.com/Schemas/MadCap.xsd" lang="en-gb" xml:lang="en-gb" data-mc-search-type="Stem" data-mc-help-system-file-name="SystemParameterPopupHelp.xml" data-mc-path-to-help-system="../../" data-mc-target-type="WebHelp2" data-mc-runtime-file-type="Topic" data-mc-preload-images="false" data-mc-in-preview-mode="false" data-mc-toc-path="">
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <meta charset="utf-8" />
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title></title>
            <link href="../../Skins/Default/Stylesheets/Slideshow.css" rel="stylesheet" data-mc-generated="True" />
            <link href="../../Skins/Default/Stylesheets/TextEffects.css" rel="stylesheet" data-mc-generated="True" />
            <link href="../../Skins/Default/Stylesheets/Topic.css" rel="stylesheet" data-mc-generated="True" />
            <link href="../../Skins/Default/Stylesheets/Components/Styles.css" rel="stylesheet" data-mc-generated="True" />
            <link href="../../Skins/Default/Stylesheets/Components/Tablet.css" rel="stylesheet" data-mc-generated="True" />
            <link href="../../Skins/Default/Stylesheets/Components/Mobile.css" rel="stylesheet" data-mc-generated="True" />
            <link href="../resources/tablestyles/note.css" rel="stylesheet" />
            <link href="../resources/tablestyles/globalbasictable8ptshort.css" rel="stylesheet" />
            <link href="../resources/tablestyles/globalbasictable8pt.css" rel="stylesheet" />
            <link href="../resources/tablestyles/globalbasictable10ptshort.css" rel="stylesheet" />
            <link href="../resources/tablestyles/globalbasictable10pt.css" rel="stylesheet" />
            <link href="../resources/stylesheets/advantage_02.css" rel="stylesheet" />
            <script src="../../Resources/Scripts/custom.modernizr.js">
            </script>
            <script src="../../Resources/Scripts/jquery.min.js">
            </script>
            <script src="../../Resources/Scripts/require.min.js">
            </script>
            <script src="../../Resources/Scripts/require.config.js">
            </script>
            <script src="../../Resources/Scripts/foundation.min.js">
            </script>
            <script src="../../Resources/Scripts/plugins.min.js">
            </script>
            <script src="../../Resources/Scripts/MadCapAll.js">
            </script>
        </head>
        <body>"""
        endHtml = """ <p class="hide"><a href="../resources/stylesheets/fonts/geinspirasans.woff" class="MCXref xref">(linked document is not in XML format)</a>
            </p>
        </body>
    </html>"""
        fileWriteText = (startHtml + parameterText + endHtml).encode('utf-8')
        
        if not os.path.exists(writeDestination):        # Should delete this first?
            os.makedirs(writeDestination)
            
        htmFileName = param + ".htm"
        file = os.path.join(writeDestination, htmFileName)
        # Check if file exists before writing it
        if not os.path.exists(file):
            writefile(file,fileWriteText)
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    import codecs, os, string, re, shutil, sys
    codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
    import xml.etree.ElementTree as ET
    
    reload(sys)  
    sys.setdefaultencoding('utf8')

    # Add the file name here of files that contain system parameter descriptions in h6 format ----------------------------------------------------------------------------------
    # systemParameterFileList = ["a_system_parameter_list.htm", "b_system_parameter_list.htm", "c_system_parameters_list.htm", "d_system_parameters_list.htm","e_system_parameters_list.htm",
                # "f_system_parameters_list.htm", "g_system_parameters_list.htm", "h_system_parameters_list.htm", "i_system_parameters_list.htm", "j_system_parameters_list.htm", 
                # "l_system_parameters_list.htm", "m_system_parameters_list.htm", "n_system_parameters_list.htm", "o_system_parameters_list.htm", "p_system_parameters_list.htm",
                # "r_system_parameters_list.htm", "s_system_parameters_list.htm", "t_system_parameters_list.htm", "u_system_parameters_list.htm", "w_system_parameters_list.htm", 
                # "y_system_parameters_list.htm", "z_system_parameters_list.htm" , "oms_system_parameters.htm", "mobile_system_parameters.htm", "power_analysis_system_parameters_list.htm",
                # "nmi_system_parameters.htm", "ivvc_system_parameters.htm", "iccp_system_parameters.htm", "geoview_system_parameters.htm", "network_model_exporter_system_parameters.htm", 
                # "nmi_system_parameters.htm", "sld_system_parameters_hidden.htm", "printing.htm", "application_window_size.htm", "spacing_and_feature_distance.htm", "location_points.htm", 
                # "background_foreground_colours.htm", "normally_open_points.htm", "looped_nops.htm", "circuit_breakers.htm", "spurs.htm", "cable_ratings.htm", "location_category.htm",
                # "scada_analogues.htm"] # earth_fault_indicators.htm and dressing_symbols.htm missing - it's a duplicate, text.htm is not unique
                
                
    systemParameterFileList = ["iccp_system_parameters.htm"]
    # op_dir = os.path.join(build_path,lang)
    
    # Find the poa main and subsystems directory
    
    for root, dirnames, filenames in os.walk(build_path):
        if "poa_main.htm" in filenames:
            print "Hurray, found poa_main.htm ", root
            poa_main_content_dir = os.path.join(root, "content")
            subsystemsDir = os.path.join(root, "Subsystems")
        
    writeDestination = os.path.join(poa_main_content_dir, "system_parameters")      # Should make the second directory here a variable so it can be changed
    print "The writedestination is", writeDestination
    
    try:
        shutil.rmtree(writeDestination)
    except WindowsError:
        print "Folder ", writeDestination, " is open!!"
        pass

    allHtmPaths = findHtm(subsystemsDir)
    systemParameterFilePaths = filePaths(allHtmPaths, systemParameterFileList)
    sysParamList, sysParamDict, lastParameterInFile = getSystemParameters(systemParameterFilePaths)
    # createHtmlFiles(sysParamList, sysParamDict, lastParameterInFile)

if __name__ == '__main__':
    lang = 'us'
    build_path = r"C:\test_project"
    create_parameter_files(lang, build_path)


