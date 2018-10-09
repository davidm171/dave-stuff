class HtmInfo:
    htm_object_list = []

    def __init__(self, htm_name, htm_path, htm_h1):
        self.htm_name = htm_name
        self.htm_path = htm_path
        self.htm_h1 = htm_h1
        # HtmInfo.htm_object_list.append(self)

    def __str__(self):
        return "\n\n\nFile: " + self.htm_name + "\n" + "Path: " + self.htm_path + "\n" + \
               "Heading 1: " + self.htm_h1 + "\n\n"
    
    # @classmethod
    def add(self):
        HtmInfo.htm_object_list.append(self)

class HtmItalics(HtmInfo):
    htm_italics_list = []

    def __init__(self, htm_name, htm_path, htm_h1, italics_list):
        self.italics_list = italics_list
        HtmInfo.__init__(self,  htm_name, htm_path, htm_h1)
        HtmItalics.htm_italics_list.append(self)

    def __str__(self):
        return "\n\n\nFile: " + self.htm_name + "\n" + "Path: " + self.htm_path + "\n" + \
               "Heading 1: " + self.htm_h1 + "\n" + \
               "Italics: " + self.italics_list[0]

    def print_italics(self):
        for entry in self.italics_list:
            print entry

class HtmProspectSysParms(HtmInfo):
    htm_params_list = []

    def __init__(self, htm_name, htm_path, htm_h1, prospective_sys_param_list):
        self.prospective_sys_param_list = prospective_sys_param_list
        HtmInfo.__init__(self, htm_name, htm_path, htm_h1)
        HtmProspectSysParms.htm_params_list.append(self)

    def __str__(self):
        return "\n\n\nFile: " + self.htm_name + "\n" + "Path: " + self.htm_path + "\n" + \
               "Heading 1: " + self.htm_h1 + "\n" + \
               "Params?: " + self.prospective_sys_param_list[0]
               
if __name__ == '__main__':
    for x in range(10):
        htm_file_object = HtmInfo("", str(x), "")
        print htm_file_object
    print "#############################################\n\n"
    print HtmInfo.htm_object_list
    for object in HtmInfo.htm_object_list:
        print object