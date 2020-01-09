###### tags: `git project`

# Branch-prediction
* 高等計算機結構 Project1
* 說明
    * 至少要做一種預測器。output為預測結果與misprediction統計數量
    * 基礎要求：2bit counter, input為Taken/Not Taken序列 (predictor的entry數量為無限大)
    * 高分要求：2bit history, input為一個序列的PC與instruction 同時可以設定predictor的entry數量
* HackMD 連結: https://hackmd.io/@EzhUyvwWT32Gy69CeyFNyA/SyUUyBNyL

# 目錄
[TOC]

## 程式執行方法
```=
python main.py [mode] [case] [entry_count]  

執行範例:
python main.py 0 base_case.txt  
python main.py 1 inst_case1.txt 4
```
* [mode]
    * mode 0 : TNTNTNTN
    * mode 1 : instruction 
* [case]
    * i.e. base_case.txt
* [entry_count]
    * entry 的個數有幾個

## Branch-prediction Alogrithm
### 2bit history prediction

## 測資
### base_case
```=  
TNTNTNTTTTTT
```
### inst_case1
```=
0x110 li R1, 0
0x114 li R2, 2
Loop:
0x118 beq R1, R2, End
0x11C subi R2, R2, 1
0x120 j Loop
End:
```

## 執行結果
### base_case
```=  
|       state        | predict  | outcome  | correct  |
|(0, SN, SN, SN, SN) |    N     |    T     |    X     |
|(1, WN, SN, SN, SN) |    N     |    N     |    O     |
|(0, WN, SN, SN, SN) |    N     |    T     |    X     |
|(1, WT, SN, SN, SN) |    N     |    N     |    O     |
|(0, WT, SN, SN, SN) |    T     |    T     |    O     |
|(1, ST, SN, SN, SN) |    N     |    N     |    O     |
|(0, ST, SN, SN, SN) |    T     |    T     |    O     |
|(1, ST, SN, SN, SN) |    N     |    T     |    X     |
|(2, ST, WN, SN, SN) |    N     |    T     |    X     |
|(3, ST, WN, WN, SN) |    N     |    T     |    X     |
|(3, ST, WN, WN, WN) |    N     |    T     |    X     |
|(3, ST, WN, WN, WT) |    T     |    T     |    O     |
# Misprediction : 6
```
### inst_case1
```=
|  entry   |   inst   |       state        | predict  | outcome  | correct  |
|    0     |  0x110   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    1     |  0x114   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    2     |  0x118   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    3     |  0x11C   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    0     |  0x120   |(0, SN, SN, SN, SN) |    N     |    T     |    X     |
|    2     |  0x118   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    3     |  0x11C   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    0     |  0x120   |(1, WN, SN, SN, SN) |    N     |    T     |    X     |
|    2     |  0x118   |(0, SN, SN, SN, SN) |    N     |    T     |    X     |
# Total Misprediction : 3

|  entry   |   inst   |       state        | predict  | outcome  | correct  |
|    0     |  0x110   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    0     |  0x120   |(0, SN, SN, SN, SN) |    N     |    T     |    X     |
|    0     |  0x120   |(1, WN, SN, SN, SN) |    N     |    T     |    X     |
# Entry0 Misprediction : 2

|  entry   |   inst   |       state        | predict  | outcome  | correct  |
|    1     |  0x114   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
# Entry1 Misprediction : 0

|  entry   |   inst   |       state        | predict  | outcome  | correct  |
|    2     |  0x118   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    2     |  0x118   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    2     |  0x118   |(0, SN, SN, SN, SN) |    N     |    T     |    X     |
# Entry2 Misprediction : 1

|  entry   |   inst   |       state        | predict  | outcome  | correct  |
|    3     |  0x11C   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
|    3     |  0x11C   |(0, SN, SN, SN, SN) |    N     |    N     |    O     |
# Entry3 Misprediction : 0
```

## 系統流程
1. 執行 main()
2. 看是 mode0/mode1
3. 讀取 input
4. 建立 Machine_Code
5. 建立 Predictor
6. 當 PC 還沒大於 指令的長度，不斷的 Machine_Code.exe()



## Function 說明
### class Predictor
* __init__(self, entry_count):
    * 初始化參數
    * 使用 create_entry()
* create_entry(self):
    * 創建空白的 entry
* predict(self, pc):
    * 預測是否 taken/not taken
* update(self, pc, predict, outcome):
    * 預測完後更新值
* get_his(self, pc, i):
    * 0:SN
    * 1:WN
    * 2:WT
    * 3:ST
* get_state(self, pc):
    * 回傳目前 state 狀態


### class Machine_Code
*  __init__(self, lines):
    *  初始化 class 參數
*  parse(self, lines):
    *  讀取 machine code
*  init_reg(self):
    *  定義 R0 的值是 0
*  exe(self):
    *  執行一次 prediction

### others
* main()
    * 讀取程式參數
* mode0(case_dir):
    * input 是 TNTN...
* mode1(case_dir):
    * input 是 machine code
    * 執行 Machine_Code.exe() 多次，直到結束