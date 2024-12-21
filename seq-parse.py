import re
import matplotlib
#matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import argparse

parser = argparse.ArgumentParser()

#modelName = 'ecg_small'
modelName = 'mobilebert'
parser.add_argument('--model-name', '-m', action='store', default=modelName)
args = parser.parse_args()

modelName = args.model_name

logFilePathBase = 'log'
logFileName = ''
logFilePath = ''

if modelName == 'ecg_small':
    logFileName = 'ecg_small_fp32_default'
elif modelName == 'mobilenet_v1':
    logFileName = 'mobilenet_v1'
elif modelName == 'mobilebert':
    logFileName = 'mobilebert'

logFilePath = f'{logFilePathBase}/{logFileName}.txt'

funcCallSeq = []
funcID = 0
funcTbl = {} # 함수 이름으로 인덱싱되는 딕셔너리

def createFuncTable(funcSeq):
    global funcID
    for funcName in funcSeq:
        if funcName not in funcTbl:
            funcTbl[funcName] = funcID
            funcID += 1
    print('idx name')
    for funcName, idx in funcTbl.items():
        print(f'{idx:3} {funcName}')
    # print(f'--> Total {funcID} items')
    print(f'--> Total {len(funcTbl)} items')
    #return funcID

print(matplotlib.get_backend())
logFile = open(logFilePath, 'r', encoding='utf-8')
print(f'file {logFilePath} is successfully opened')

lines = logFile.readlines()
logFile.close()

# dispatch region 함수 이름 추출 -> 리스트 funcCallSeq에 저장
pattern = r'main_\S*'
for line in lines:
    matches = re.findall(pattern, line)
    funcCallSeq.append(matches[0])

# funcCallSeq를 이용하여 funcTbl 생성
createFuncTable(funcCallSeq)

funcAccTbl = [ [] for _ in range(len(funcTbl)) ] # 각 dispatch region의 호출 지점들을 저장
funcSeqList = []                                 # dispatch region 호출 시퀀스를 저장

for ln, funcName in enumerate(funcCallSeq):
    funcAccTbl[funcTbl[funcName]].append(ln)
    funcSeqList.append(funcTbl[funcName])
    # print(f'[{ln}] {funcName} --> {funcTbl[funcName]}')

## funcAccTbl 동작 확인
# totalCalls = 0
# for idx, e in enumerate(funcAccTbl):
#     print(f'{idx:3}: {e} --> total {len(e)} calls')
#     #totalCalls += len(e)

totalCalls = len(funcSeqList)
print(f'==> total {totalCalls} dispatch region calls')

prevIdx = 0
prevFuncIdx = 0
sepList = []
print('sepList: [ ', end='')
for idx, funcIdx in enumerate(funcSeqList):
    if modelName == 'mobilebert' and prevFuncIdx == 25 and funcIdx == 5:
        print(f'{idx}(+{idx - prevIdx}) ', end='')
        sepList.append(idx)
        prevIdx = idx
    prevFuncIdx = funcIdx
print(f'] --> total {len(sepList)} items')

# x = np.linspce(0, len(funcCallSeq)-1, len(funcCallSeq))
x = range(0, len(funcCallSeq))
y = funcSeqList

fig, ax = plt.subplots()
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.scatter(x, y, color='blue', s=3)
ax.grid(True)

for sepx in sepList:
    ax.axvline(x=sepx, color='#aa0000', linestyle='--', linewidth=1)

plt.show()
