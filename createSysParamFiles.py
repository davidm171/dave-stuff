# coding="utf-8"
# Create directory of all system parameter htms by parsing relevant pages

def create_parameter_files(lang, build_path, allHtmPaths):
    import config
    
    # open the file-----------------------------------------------------------------------------------------------------------------------------------------------------------
    def open_file(file_name, encoding='utf8'):
        f1 = open(file_name, "r")
        fileText = f1.read()
        f1.close()
        return fileText
        
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Function to extract system parameter name from h6----------------------------------------------------------------------------------------------------------------------
    def processHeading(name):
        name = re.sub(r"\n", "", name)              ### This removes carriage returns which appear in h6s for no known reason
        name = re.sub(r"<a name=(.*?)<\/a>", "",name)
        nameP = name.replace(" ", "")                                # Removes spaces so no issue with spaces before colon
        colonPosition = string.find(nameP, ":")
        if colonPosition != -1:
            parameterText = nameP[:colonPosition]
        else:
            parameterText = nameP

        parameterText = parameterText.strip('<h6>')
        parameterText = parameterText.strip('</h6>')
        parameterText = parameterText.strip()
        return parameterText
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def filePaths(path,systemParameterFileList):
        systemParameterFilePaths = []
        for htmPath in path:
            if os.path.split(htmPath)[1] in systemParameterFileList:
                systemParameterFilePaths.append(htmPath)

        return systemParameterFilePaths
        
    def find_png(path):                                 #Find a better way to do this
        pngfiles = [os.path.join(root, name)
        for root, dirs, files in os.walk(path)
            for name in files
                if name.endswith(".png")]
        return pngfiles
        
    # Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    import codecs, os, string, re, shutil, sys

    reload(sys)  
    sys.setdefaultencoding('utf8')

    # Add the file name here of files that contain system parameter descriptions in h6 format ----------------------------------------------------------------------------------
    systemParameterFileList = ["a_system_parameter_list.htm", "b_system_parameter_list.htm", "c_system_parameters_list.htm", "d_system_parameters_list.htm","e_system_parameters_list.htm",
                "f_system_parameters_list.htm", "g_system_parameters_list.htm", "h_system_parameters_list.htm", "i_system_parameters_list.htm", "j_system_parameters_list.htm", 
                "l_system_parameters_list.htm", "m_system_parameters_list.htm", "n_system_parameters_list.htm", "o_system_parameters_list.htm", "p_system_parameters_list.htm",
                "r_system_parameters_list.htm", "s_system_parameters_list.htm", "t_system_parameters_list.htm", "u_system_parameters_list.htm", "w_system_parameters_list.htm", 
                "y_system_parameters_list.htm", "z_system_parameters_list.htm" , "oms_system_parameters.htm", "mobile_system_parameters.htm", "power_analysis_system_parameters_list.htm",
                "nmi_system_parameters.htm", "ivvc_system_parameters.htm", "iccp_system_parameters.htm", "geoview_system_parameters.htm", "network_model_exporter_system_parameters.htm", 
                "nmi_system_parameters.htm", "sld_system_parameters_hidden.htm", "printing.htm", "application_window_size.htm", "spacing_and_feature_distance.htm", "location_points.htm", 
                "background_foreground_colours.htm", "normally_open_points.htm", "looped_nops.htm", "circuit_breakers.htm", "spurs.htm", "cable_ratings.htm", "location_category.htm",
                "scada_analogues.htm"] # earth_fault_indicators.htm and dressing_symbols.htm missing - it's a duplicate, text.htm is not unique
                
                
    # systemParameterFileList = ["a_system_parameter_list.htm"]
    # op_dir = os.path.join(build_path,lang)

    # Find the poa main and subsystems directory

    subsystemsDir =   config.subsystemsDir
    writeDestination = os.path.join(config.flare_content_path, "system_parameters")      # Should make the second directory here a variable so it can be changed
    print "The writedestination is", writeDestination

    try:
        shutil.rmtree(writeDestination)
    except WindowsError:
        print "Folder ", writeDestination, " is open!!"
        pass

    systemParameterFilePaths = filePaths(allHtmPaths, systemParameterFileList)

    # writeDestination = os.path.join(  config.flare_content_path, "system_parameters")
    if not os.path.exists(writeDestination):        # Should delete this first?
        os.makedirs(writeDestination)

    from htm_object import HtmInfo
    from write_decorator import message
    from image_copy import update_image_link
    
    image_list = []
    image_list = find_png(r"C:\test_project\output\AdvantageHTML5_us")
    
    for file in systemParameterFilePaths:
        fileText = open_file(file).decode('utf8')
        
        # rawHeading = re.finsystemParameterFilePaths:
        h6all= re.findall(r"<h6.+?</h6>", fileText)
        h6all.append("<p class=\"hide\">")                                    # Add for end of file    
        h6_list = iter(h6all)

        i = next(h6_list)
        start_string = str(i)
        for h6 in h6_list:
        
            end_string = str(h6)
            HtmInfo.system_parameters_list.append(processHeading(start_string))
            print "The proessed heading string is: ", processHeading(start_string)      #EXECUTING THIS TWICE!!!
            # print start_string.encode('utf8'), " -----> ", end_string.encode('utf8')
            startIndex = fileText.find(start_string)
            endIndex = fileText.find(end_string)
            param_text = fileText[startIndex:endIndex]
            # param_text = re.sub(r"<a.*?>", "<i>",param_text)                 # Two lines remove cross references in sys param text
            # param_text = re.sub(r"</a>", "</i>",param_text)                  # Example is earth trace scope, but what about figures? see ETS
            # print "\n", param_text.encode('utf8'), "\n\n"
            # print "The start string is: ", start_string
            param_file_name = processHeading(start_string) + ".htm"
            # print "The filenmae is: ", param_file_name
            param_file_path = os.path.join(writeDestination, param_file_name)
            print "Writing system parameter file: ",  param_file_path
            param_text = update_image_link(param_text, image_list)                          #Update any image lnks
            message(param_file_path, param_text)
            start_string = end_string

    print "\n\nThe system parameter files have been created."
    print "\nThe system parameters are\n\n", HtmInfo.system_parameters_list
# Function to find all htms under path ------------------------------------------------------------------------------------------------------------------------------------
def findHtm(path):
    htmfiles = [os.path.join(root, name)
                for root, dirs, files in os.walk(path)
                for name in files
                if name.endswith(".htm")]
    return htmfiles
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
if __name__ == '__main__':
    
    import config
        
    import os
    lang = config.language
    
    for root, dirnames, filenames in os.walk(config.build_path):
        if "poa_main.htm" in filenames:
            print "Hurray, found poa_main.htm ", root
            config.flare_main_path = root
            config.flare_content_path = os.path.join(root, "content")
            config.subsystemsDir = os.path.join(root, "Subsystems")
    
    print "The main path is: ",   config.flare_main_path
    print "The Content path is: ",   config.flare_content_path
    allHtmPaths = findHtm(  config.subsystemsDir) 
    create_parameter_files(lang, config.build_path, allHtmPaths)




