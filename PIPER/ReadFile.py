line = file.readline().rstrip().decode("utf-8")
            line_float = [float(x) for x in line.split(",")]
            file_content = line
            numberOfLine = 1
            while (line):
                line = file.readline().rstrip().decode("utf-8")
                line_float = []
                for x in line.split(","):
                    if (x.isdecimal()):
                        line_float += [float(x)]
                    else:
                        break
                file_content += ("\r\n")
                file_content += line
                numberOfLine += 1