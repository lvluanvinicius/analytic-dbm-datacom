with open("test", "r") as file: 
    for line in file.readlines():
        if "Rx Optical Power [dBm]" in line:
            if "N/A" in line.split(":")[1].strip(): 
                break