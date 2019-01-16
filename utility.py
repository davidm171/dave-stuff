import os, fnmatch, io
import re

subsystemsDir = r"C:\test_project\output\AdvantageHTML5_us\content\system_parameters"
filepat = "*.htm"
allHtmPaths = [os.path.join(path,name) for path, dirlist, filelist in os.walk(subsystemsDir)
            for name in fnmatch.filter(filelist,filepat)]
            
# print allHtmPaths

for file in allHtmPaths:
    # fileText = open_file(file)
    with io.open(file,'r',encoding='utf8') as f:
        fileText = f.read()

    h6all= re.findall(r"<h6.+?</h6>", fileText)
    if len(h6all) > 1:
        print file