import subprocess

def readInputFileWithSpace(filePath):
    data = []
    
    file = open(filePath, "r")
    line = file.readline()
    separator = " "
    lineData = [float(x.strip()) for x in line.split(separator) if x != '']
    sizeOfLineData = len(lineData)

    for i in range(sizeOfLineData):
        data = data + [[lineData[i]]]

    while(line):
        line = file.readline()
        stringlineData = [x.strip() for x in line.split(separator) if x != '']
        if(sizeOfLineData != len(stringlineData)):
            break
        lineData = [float(x) for x in stringlineData]

        for i in range(sizeOfLineData):
            data[i] = data[i] + [lineData[i]]

    return data

def readOutputVar(process):
    output = process.stdout.readline()
    varStr = output.strip().decode("utf-8")
    return [float(x) for x in varStr.split(' ')]

auxFilePath = "D:\\MicroService\\Test1\\uploads\\DAT_IN\\AUXDATA.dat"
fldFilePath = "D:\\MicroService\\Test1\\uploads\\DAT_IN\\FLDDATA.dat"

auxData = readInputFileWithSpace(auxFilePath)
fldData = readInputFileWithSpace(fldFilePath)

depth = auxData[0]
restInit = auxData[1]
measurement = fldData[1:len(fldData)]

exeFullPath = "D:\\src\\fe_ans\\Techlog\\TFSRepo\\HFE-Algo-PixelInversion_changed\\PIPER\\x64\\Release\\PiperEXE.exe"

depthArg = " ".join([str(x) for x in depth])
restInitArg = " ".join([str(x) for x in restInit])


process = subprocess.Popen(exeFullPath, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

process.stdin.write(bytes(str(len(depth))+' ', "utf-8"))
process.stdin.write(bytes(depthArg       , "utf-8"))
process.stdin.write(bytes(restInitArg    , "utf-8"))

for mea in measurement:
    meaArg = " ".join([str(x) for x in mea])
    process.stdin.write(bytes(meaArg, "utf-8"))

process.stdin.close()

RH60   = readOutputVar(process)
RH80   = readOutputVar(process)
RV60   = readOutputVar(process)
RV80   = readOutputVar(process)
DPAP60 = readOutputVar(process)
DPAP80 = readOutputVar(process)
DPAA60 = readOutputVar(process)
DPAA80 = readOutputVar(process)
DPTR60 = readOutputVar(process)
DPTR80 = readOutputVar(process)
DPAZ60 = readOutputVar(process)
DPAZ80 = readOutputVar(process)
MF60   = readOutputVar(process)
MF80   = readOutputVar(process)

print(RH60  )
print(RH80  )
print(RV60  )
print(RV80  )
print(DPAP60)
print(DPAP80)
print(DPAA60)
print(DPAA80)
print(DPTR60)
print(DPTR80)
print(DPAZ60)
print(DPAZ80)
print(MF60  )
print(MF80  )


