import math


numbers = []                    # Number of line in the original srt file
timestamps = []                 # Timestamps line in the original srt file
content = []                    # Subtitle content line in the original srt file
separate_timestamps = []        # Separated timestamps list
dict_timestamps = []            # Dictionary of original srt timestamps separated into "hr", "min", "sec", "ms"
shifted_timestamps = []         # Dictionary of shifted timestamps separated into "hr", "min", "sec", "ms"
starter_timestamp_lines = []    # List of all lines beginning timestamps
ender_timestamp_lines = []      # List of all lines ending timestamps

def srt_line_parser(lines):
    try:
        for i in range(len(lines)):
            if len(lines[i].split("\n")) >= 3:
                numbers.append(lines[i].split("\n")[0])
                timestamps.append(lines[i].split("\n")[1])
                content.append(lines[i].split("\n")[2:])
            else:
                content[content.index(content[i - 1])].append(lines[i].split("\n")[0])
    except IndexError:
        print("Error Happened Internally")

    try:
        for i in range(len(numbers)):
            print(numbers[i])
            print(timestamps[i])
            print(content[i])
            print("\n", end="")

    except IndexError:
        pass

def timestamp_separator(timestamps):
    for timestamp in timestamps:
        before = timestamp.split(" -")[0]
        after = timestamp.split("> ")[1]

        separate_timestamps.append(before)
        separate_timestamps.append(after)

def timestamp_dict_creator(separate_timestamps):
    for stamp in separate_timestamps:
        dictionary = {
            "hr": int(stamp.split(":")[0]),
            "min": int(stamp.split(":")[1]),
            "sec": int(stamp.split(":")[2].split(",")[0]),
            "ms": int(stamp.split(":")[2].split(",")[1])
        }

        dict_timestamps.append(dictionary)


def shift_creator(shift_direction, shift_value):
    hr = 0
    min = 0
    sec = 0
    ms = 0
    shift_dict = {
        "hr": 0,
        "min": 0,
        "sec": 0,
        "ms": 0
    }

    if shift_value < 0.999:
        ms = shift_value * 1000

    else:
        sec = int(math.modf(shift_value)[1])
        ms = int(math.ceil(1000 * math.modf(shift_value)[0]))

        if sec >= 60:
            min = int(sec / 60)
            sec = sec - (min * 60)

        if min >= 60:
            hr = int(min / 60)
            min = min - (hr * 60)

    if shift_direction == "B" or shift_direction == "b":
        shift_dict = {
            "hr": hr * -1,
            "min": min * -1,
            "sec": sec * -1,
            "ms": ms * -1
        }

    elif shift_direction == "F" or shift_direction == "f":
        shift_dict = {
            "hr": hr,
            "min": min,
            "sec": sec,
            "ms": ms
        }
    
    else:
        return "Invalid Input" 

    return shift_dict

def sub_modifier(current, shift):
    altered_hr = current["hr"] + shift["hr"]
    altered_min = current["min"] + shift["min"]
    altered_sec = current["sec"] + shift["sec"]
    altered_ms = current["ms"] + shift["ms"]

    if altered_ms > 999:
        altered_ms -= 1000
        altered_sec += 1
    elif altered_ms < 0:
        altered_ms += 1000
        altered_sec -= 1

    if altered_sec > 59:
        altered_sec -= 60
        altered_min += 1
    elif altered_sec < 0:
        altered_sec += 60
        altered_min -= 1

    if altered_min > 59:
        altered_min -= 60
        altered_hr += 1
    elif altered_min < 0:
        altered_min += 60
        altered_hr -= 1
    
    altered_timestamp = {
        "hr": "{:02d}".format(altered_hr),
        "min": "{:02d}".format(altered_min),
        "sec": "{:02d}".format(altered_sec),
        "ms": "{:03d}".format(altered_ms)
    }

    if altered_hr < 0 or altered_min < 0 or altered_sec < 0 or altered_ms < 0:
        return "Not Cool" 

    return altered_timestamp

def timestamp_formatter(shifted_timestamps):
    for mod_stamp in shifted_timestamps:
        if shifted_timestamps.index(mod_stamp) % 2 == 0:
            mod_lin = (mod_stamp["hr"] + ":" + mod_stamp["min"] + ":" + mod_stamp["sec"] + "," + mod_stamp["ms"] + " --> ")
            starter_timestamp_lines.append(mod_lin)
        else:
            mod_lin = (mod_stamp["hr"] + ":" + mod_stamp["min"] + ":" + mod_stamp["sec"] + "," + mod_stamp["ms"] +"\n")
            ender_timestamp_lines.append(mod_lin)
    return (starter_timestamp_lines, ender_timestamp_lines)

def output_srt_file_creator(lines):
    try:
        for i in range(len(lines)):
                modified_srt_file.write(numbers[i].split("\n")[0] + "\n")
                modified_srt_file.write(starter_timestamp_lines[i])
                modified_srt_file.write(ender_timestamp_lines[i])
                for sub_line in content[i]:
                    if type(sub_line) == str:
                        modified_srt_file.write(sub_line)
                        modified_srt_file.write("\n")
                    elif type(sub_line) == list:
                        for item in sub_line:
                            modified_srt_file.write(item)
                    modified_srt_file.write("\n")

    except IndexError:
        pass


# User Interface

file_name = input("Enter File Name: ")
shift_direction = input("Shift Direction (Enter \"F\" or \"f\" for forward shifting or enter \"B\" or \"b\" for backward shifting: ")
shift_value = float(input("Enter shift value in seconds.millisecions format: "))


try:
    if file_name[(len(file_name) - 3):] == "srt":
        srt_file = open(file_name, "r").read()
        modified_srt_file = open(file_name.split(".")[0] + " modified.srt", "w")
        lines = srt_file.split("\n\n")
        srt_line_parser(lines)
        timestamp_separator(timestamps)
        timestamp_dict_creator(separate_timestamps)
        shift = shift_creator(shift_direction, shift_value)


        for split_timestamp in dict_timestamps:
            modified_stamp = sub_modifier(split_timestamp, shift)
            shifted_timestamps.append(modified_stamp)

        timestamp_formatter(shifted_timestamps)
        output_srt_file_creator(lines)
        print(numbers)
    else:
        print("Format Doesn't Match .srt")
except FileNotFoundError:
    print("File Doesn't Exist")
except IndexError:
    print("Invalid Input")