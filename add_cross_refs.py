# encoding: utf-8

# Issues
# Searching for Introduction in guide only references does find all 1st chapters, and it isn't translatable can it look in TOC?
# In guideToDir make function to process href, or for both for loops?
# Search for strings in directory a structure,  instead of another directory structure?
# Can reference to spread sheet be changed per language?
# Get a log list of the references that aren't substituted
# It substitutes the same text back in, for example a reference to Work Package Manager instead of Order Manager


def crossRefs(lang, build_path, obj, fileText, guideToDirMap):


    # guideToDirMap = {"PowerOn Configuration Reference Guide" : "Subsystems\\core_config\\content\\00-poweron_configuration_reference", "Generic Functionality Guide" : \
    # "Subsystems\\core\\content\\00-generic_functionality", "Alarm Configuration Guide" : "Subsystems\\core_config\\content\\02-alarm_configuration", "Generic Functionality User Guide" : \
    # "02-user\\00-core\\Content\\00-generic_functionality", "Operators and Privileges Configuration Guide" : "OperatorsandPrivilegesConfigurationHelp",\
    # "Work Package Manager Configuration Guide" : "Subsystems\\nms_config\\content\\01-wpm_configuration", "PowerOn Configuration Guide" : \
    # "Subsystems\\core_config\\content\\01-poweron_configuration", "Order Manager Configuration Guide" : "WorkPackageManagerConfigurationHelp", \
    # "Work Package Manager User Guide" : "Subsystems\\nms\content\\01-order_manager", "Order Manager User Guide" : "Subsystems\\nms\content\\01-order_managerr"}

    import os, re, sys, textwrap

    # Open file ----------------------------------------------------------------------------------------------------------------------
    def openFile(file):
        f = open(file, 'r')
        fileText = f.read()
        f.close()
        return (fileText)

    # --------------------------------------------------------------------------------------------------------------------------------

    # Write and close file -----------------------------------------------------------------------------------------------------------
    def writefile(file, fileText):
        f = open(file, "w")
        f.write(fileText)
        f.close()

    # --------------------------------------------------------------------------------------------------------------------------------

    # Function to find the depth of ellipisis in relative path -------------------------------------------------------------------------
    def relPath(file):
        path = os.path.normpath(file)
        path_list = path.split(os.sep)
        absoluteFileDepth = len(path_list)
        depthCount = absoluteFileDepth

        while path_list[depthCount - 1] != "Subsystems":
            depthCount -= 1

        depth = absoluteFileDepth - depthCount - 1
        relPath = ""
        for i in range(0, depth):
            relPath = relPath + "..\\"

        ellipsis = os.path.normpath(relPath)
        return ellipsis

    # ---------------------------------------------------------------------------------------------------------------------------------

    # Function to return reference guide name, and section if it has one --------------------------------------------------------------
    def processItalics(findItalics):
        fullRef = hit[3:-4]
        mDash = '—'
        reference = []
        if mDash in fullRef:
            reference.append(fullRef.split(mDash)[0])
            reference.append(fullRef.split(mDash)[1])
        else:
            reference.append(fullRef)
        return reference

    # Function to find mapping from guide reference to director address ---------------------------------------------------------------
    def guideToDir(ref):
        guideName = ref[0]
        linkInfo = ["Link not found!", "No section text in link!"]
        if guideName in guideToDirMap:

            guideDirectory = guideToDirMap[guideName]
            if len(ref) == 1:
                section = "Introduction"
                linkInfo = firstPageCrossRef(guideDirectory, section, linkInfo)

            elif len(ref) == 2:
                section = ref[1]
                linkInfo = constructCrossRef(guideDirectory, section,  linkInfo)

        return linkInfo

    # ---------------------------------------------------------------------------------------------------------------------------------
    # Search for cross ref guide directory address in all address, and section, and construct cross ref -------------------------------
    # This searches for introduction in the filename rather than in the heading so no need to translate -------------------------------
    def firstPageCrossRef(guideDirectory, section, linkInfo):

        for htm_object in htm_object_list:
            if (str(guideDirectory).lower() in str(htm_object.htm_path).lower()) and (
                    str(section).lower() in str(htm_object.htm_path).lower()):

                htmRef = re.findall(r'Subsystems\\(.+?\.htm)', htm_object.htm_path)
                relativeRef = str(htmRef[0])
                href = relPath(htm_object.htm_path) + "\\" + relativeRef  # Why need the to add \\?????
                linkInfo[0] = href
                linkInfo.append(section)

        return linkInfo

    # ---------------------------------------------------------------------------------------------------------------------------------
    # Search for cross ref guide directory address in all address, and section, and construct cross ref -------------------------------
    def constructCrossRef(guideDirectory, section, linkInfo):

        for htm_object in htm_object_list:
            if (str(guideDirectory).lower() in str(htm_object.htm_path).lower()) and (section == htm_object.htm_h1):
 
                htmRef = re.findall(r'Subsystems\\(.+?\.htm)', htm_object.htm_path)
                relativeRef = str(htmRef[0])

                href = relPath(htm_object.htm_path) + "\\" + relativeRef  # Why need the to add \\?????

                linkInfo[0] = href
                linkInfo.append(section)

        return linkInfo

    # ---------------------------------------------------------------------------------------------------------------------------------
    # Main ----------------------------------------------------------------------------------------------------------------------------

    # path = "C:\\builds\\us"														# CHANGE THIS TO POINT TO ANY DIRECTORY AS LONG AS TRANSLATION IN SPREADSHEET
    
    htm_object_list = obj.htm_object_list
    
    findItalics = obj.italics_list
    if "system_parameters" not in str(obj.htm_path):  # Don't process the system parameters directory

        for hit in findItalics:
            ref = processItalics(findItalics)
            refInfo = guideToDir(ref)

            if refInfo[0] != "Link not found!":
                hit = hit[3:-4]  # Remove italics here from text
                aTag = "<a href=" + "\"" + refInfo[0] + "\"" + " class=\"MCXref xref\"" + ">" + hit + "</a>"
                aTag = aTag.replace("\\", "/")
                hit = "<i>" + hit + "</i>"  # Substitute italics out, there must be an easier way?
                fileText = fileText.replace(hit, aTag)
                
    return fileText
