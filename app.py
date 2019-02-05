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

srt_file = open("Sukiyaki Western Django (2007).srt", "r").read()
modified_srt_file = open("modified srt.srt", "w")

lines = srt_file.split("\n\n")
"""
current = {
    "hr": 0,
    "min": 55,
    "sec": 50,
    "ms": 990
}
"""
shift = {
    "hr": 0,
    "min": 0,
    "sec": 1,
    "ms": 1
}


numbers = []
timestamps = []
content = []

try:
    for line in lines:
        numbers.append(line.split("\n")[0])
        timestamps.append(line.split("\n")[1])
        content.append(line.split("\n")[2:])
except IndexError:
    pass

try:
    for i in range(len(numbers)):
        print(numbers[i])
        print(timestamps[i])
        print(content[i])
        print("\n", end="")

except IndexError:
    pass

separate_timestamps = []
for timestamp in timestamps:
    before = timestamp.split(" -")[0]
    after = timestamp.split("> ")[1]

    separate_timestamps.append(before)
    separate_timestamps.append(after)

print(separate_timestamps)

dict_timestamps = []

for stamp in separate_timestamps:
    dictionary = {
        "hr": int(stamp.split(":")[0]),
        "min": int(stamp.split(":")[1]),
        "sec": int(stamp.split(":")[2].split(",")[0]),
        "ms": int(stamp.split(":")[2].split(",")[1])
    }

    dict_timestamps.append(dictionary)

#print(split_timestamps)

shifted_timestamps = []

for split_timestamp in dict_timestamps:
    modified_stamp = sub_modifier(split_timestamp, shift)
    shifted_timestamps.append(modified_stamp)

starter_timestamp_lines = []
ender_timestamp_lines = []
def timestamp_formatter(shifted_timestamps):
    for mod_stamp in shifted_timestamps:
        if shifted_timestamps.index(mod_stamp) % 2 == 0:
            mod_lin = (mod_stamp["hr"] + ":" + mod_stamp["min"] + ":" + mod_stamp["sec"] + "," + mod_stamp["ms"] + " --> ")
            starter_timestamp_lines.append(mod_lin)
        else:
            mod_lin = (mod_stamp["hr"] + ":" + mod_stamp["min"] + ":" + mod_stamp["sec"] + "," + mod_stamp["ms"] +"\n")
            ender_timestamp_lines.append(mod_lin)
    return (starter_timestamp_lines, ender_timestamp_lines)

timestamp_formatter(shifted_timestamps)
print(ender_timestamp_lines)

try:
    for i in range(len(lines)):
            modified_srt_file.write(lines[i].split("\n")[0] + "\n")
            modified_srt_file.write(starter_timestamp_lines[i])
            modified_srt_file.write(ender_timestamp_lines[i])
            for sub_line in content[i]:
                modified_srt_file.write(sub_line)
                modified_srt_file.write("\n")
            modified_srt_file.write("\n")
except IndexError:
    pass