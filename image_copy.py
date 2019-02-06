def update_image_link(param_text, image_list):
    import re, string
    param_image_list = re.findall(r"<img src=\"(.*?).png",param_text)		# If there are any, copy image files over
    if len(param_image_list) != 0:
        for image_path_in_file in param_image_list:
            file_split = image_path_in_file.split("/")
            index = len(image_path_in_file.split("/"))
            image_directory = file_split[index - 2]
            image_file = file_split[index - 1] + ".png"
            for image_path in image_list:
                if (image_directory in image_path) and (image_file in image_path):
                    part2 = image_path.rpartition("Subsystems")[2]
                    new_str = string.replace(part2, '\\', '/')
                    new_image_link = "../../Subsystems" + new_str
                    original_image = image_path_in_file + ".png"
                    param_text = param_text.replace(original_image,new_image_link)
    return param_text
