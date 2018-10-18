# open the file-----------------------------------------------------------------------------------------------------------------------------------------------------------
def open_file(file_name, encoding='utf8'):
    f1 = open(file_name, "r")
    fileText = f1.read()
    f1.close()
    return fileText
    
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Write and close file ----------------------------------------------------------------------------------------------------------------------------------------------------
def writefile(func):
    def wrapper(*args,**kargs):
        file = args[0]
        try: 
            f = open(file, "w")
            start = """<!DOCTYPE html>
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
            end = """" <p class="hide"><a href="../resources/stylesheets/fonts/geinspirasans.woff" class="MCXref xref">(linked document is not in XML format)</a>
            </p>
        </body>
    </html>"""

            text = args[1]
            write_text = start + text + end
            f.write(text_to_display.encode("utf8"))
            f.close()
        except IOError:
            print "Can't write file: ", file
    return wrapper
# -------------------------------------------------------------------------------------------------------------------------------

@writefile
def message(file, text_to_display):
    return text_to_display
file = "diddy.htm"

text_to_display = raw_input("Enter text for htm: ")
# text_to_display = "Hello there!"
message(file, text_to_display)
    