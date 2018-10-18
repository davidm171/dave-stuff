# coding="utf-8"
# Create directory of all system parameter htms by parsing relevant pages


# open the file-----------------------------------------------------------------------------------------------------------------------------------------------------------
def open_file(file_name, encoding='utf8'):
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

        
        rawHeading = re.findall(r"<h6.+?</h6>", fileText)
        print rawHeading
        
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
lang = 'us'
build_path = r"C:\test_project"
import codecs, os, string, re, shutil, sys
# codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
import xml.etree.ElementTree as ET

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

writeDestination = os.path.join(poa_main_content_dir, "system_parameters")
if not os.path.exists(writeDestination):        # Should delete this first?
    os.makedirs(writeDestination)

from write_decorator import message

for file in systemParameterFilePaths:
    fileText = open_file(file).decode('utf8')
    
    # rawHeading = re.finsystemParameterFilePaths:
    h6all= re.findall(r"<h6.+?</h6>", fileText)
    # print h6all
    
    # gen = (h6.text for h6 in root.findall("body/h6") if h6.text is not None)
    
    h6_list = iter(h6all)
    i = next(h6_list)
    start_string = str(i)
    for h6 in h6_list:
        end_string = str(h6)
        print processHeading(start_string)
        print start_string.encode('utf8'), " -----> ", end_string.encode('utf8')
        startIndex = fileText.find(start_string)
        endIndex = fileText.find(end_string)
        param_text = fileText[startIndex - 4:endIndex - 4]
        print "\n", param_text.encode('utf8'), "\n\n"

        param_file_name = processHeading(start_string)[4:] + ".htm"
        param_file_path = os.path.join(writeDestination, param_file_name)
        print "@@@File path: ",  param_file_path
        message(param_file_path, param_text)
        start_string = end_string


        
    # for d in duds:
        # print d

    # print "The last parameter in the file was: ", end_string  #Need to sort out last parameters in file problem


