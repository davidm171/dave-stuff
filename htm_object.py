class HtmInfo:
    htm_object_list = []
    htm_italics_list = []
    htm_params_list = []
    poa_main_content_dir = r"C:\test_project\output\AdvantageHTML5_us\content" # Note that this is hard coded for now!
    subsystemsDir = r"C:\test_project\output\AdvantageHTML5_us\Subsystems"

    def __init__(self, htm_name, htm_path, htm_h1, italics_list, 
                  prospective_sys_param_list):
        self.htm_name = htm_name
        self.htm_path = htm_path
        self.htm_h1 = htm_h1
        self.italics_list = italics_list
        self.prospective_sys_param_list = prospective_sys_param_list


    def __str__(self):
        return "\n\n\nFile: " + self.htm_name + "\n" + "Path: " + self.htm_path + "\n" + \
               "Heading 1: " + self.htm_h1 + "\n\n" + "Italics: " + self.italics_list[0] + \
                "Params?: " + self.prospective_sys_param_list[0]
    
    def add(self):
        HtmInfo.htm_object_list.append(self)
        
    def add_italics(self):
        HtmInfo.htm_italics_list.append(self)
        
    def add_params(self):
        HtmInfo.htm_params_list.append(self)
        
               
if __name__ == '__main__':
    for x in range(10):
        htm_file_object = HtmInfo("", str(x), "", ["S"], ["T"])
        print htm_file_object
    print "#############################################\n\n"
    print HtmInfo.htm_object_list
    for object in HtmInfo.htm_object_list:
        print object