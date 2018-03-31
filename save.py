from os import path
import sys


my_path = str(path.abspath(sys.modules['__main__'].__file__)).replace("main.py", "")
save_file_path = my_path + "save.sav"

def read_save():

    try:
        settings = open(save_file_path, "r+")
    except FileNotFoundError:
        settings = open(save_file_path, "w")
        settings.write(
            "# This is the saving file for pyckage tracker\n# Each line represents one package\n\n# Format of "
            "each entry should be:\n# Name; Carrier; Tracking_number\n# Separate by semi-columns \";\"\n\n# "
            "Lines starts as # \\n \\t or \\r will be skipped\n")
        settings.close()

    setting_list = []

    for line in settings:

        escaped_list = "#\n\t\r"

        if line[0] not in escaped_list:
            setting = line.split(";")
            setting[1] = setting[1].replace(" ", "")
            setting[2] = setting[2].replace(" ", "").replace("\n", "")
            setting_list.append([setting[0], setting[1], setting[2]])

    settings.close()
    # ============ Returns: setting_list = [[name, carrier, number],] ============
    return setting_list


def write_save(save_list):

    settings = open(save_file_path, "w")
    settings.write(
        "# This is the saving file for pyckage tracker\n# Each line represents one package\n\n# Format of "
        "each entry should be:\n# Name; Carrier; Tracking_number\n# Separate by semi-columns \";\"\n\n# "
        "Lines starts as # \\n \\t or \\r will be skipped\n\n\n")

    settings.close()
