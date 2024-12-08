import re
import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
#import numpy as np

#modelName = 'ecg_small'
modelName = 'mobilebert'

logFilePathBase = 'log'
logFileName = ''
logFilePath = ''

if modelName == 'ecg_small':
    logFileName = 'ecg_small_fp32_default'
elif modelName == 'mobilebert':
    logFileName = 'mobilebert'

logFilePath = f'{logFilePathBase}/{logFileName}.txt'

funcCallSeq = []
funcID = 0
funcTbl = {}

def createFuncTable(funcSeq):
    global funcID
    for funcName in funcSeq:
        if funcName not in funcTbl:
            funcTbl[funcName] = funcID
            funcID += 1
    for funcName, idx in funcTbl.items():
        print(f'{idx:3} {funcName}')
    print(f'--> Total {funcID} items')
    return funcID

print(matplotlib.get_backend())
logFile = open(logFilePath, 'r', encoding='utf-8')
print(f'file {logFilePath} is successfully opened')

lines = logFile.readlines()
logFile.close()

pattern = r'main_\S*'
for line in lines:
    matches = re.findall(pattern, line)
    funcCallSeq.append(matches[0])

funcTblLen = createFuncTable(funcCallSeq)
funcSeqTbl = [ [] for _ in range(funcTblLen) ]
funcSeqList = []

for ln, funcName in enumerate(funcCallSeq):
    funcSeqTbl[funcTbl[funcName]].append(ln)
    funcSeqList.append(funcTbl[funcName])
    # print(f'[{ln}] {funcName} --> {funcTbl[funcName]}')

totalCalls = 0
for idx, e in enumerate(funcSeqTbl):
    # print(f'{idx:3}: {e} --> total {len(e)} calls')
    totalCalls += len(e)

print(f'==> total {totalCalls} dispatch region calls')

# x = np.linspce(0, len(funcCallSeq)-1, len(funcCallSeq))
x = range(0, len(funcCallSeq))
y = funcSeqList

fig, ax = plt.subplots()
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.scatter(x, y, color='blue', s=1)
ax.grid(True)

plt.show()