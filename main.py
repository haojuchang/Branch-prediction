import sys
import re


class Predictor:
    def __init__(self, entry_count):
        self.entry_count = entry_count
        self.entrys = self.create_entry()

    def create_entry(self):
        entrys = []
        for i in range(0, self.entry_count):
            e = {
                "his": 0,   # on which bc
                "bc": [0, 0, 0, 0],  # [bc0, bc1, bc2, bc3] 01:N, 23:T
                "mis": 0  # misprediction count
            }
            entrys.append(e)
        return entrys

    def predict(self, pc):
        his = self.entrys[pc]["his"]
        if self.entrys[pc]["bc"][his] == 0 or self.entrys[pc]["bc"][his] == 1:
            return "N"
        else:  # 2 and 3
            return "T"

    def update(self, pc, predict, outcome):
        his = self.entrys[pc]["his"]

        if outcome == "T":
            if self.entrys[pc]["bc"][his] != 3:
                self.entrys[pc]["bc"][his] += 1
            if self.entrys[pc]["his"] != 3:
                self.entrys[pc]["his"] += 1
        elif outcome == "N":
            if self.entrys[pc]["bc"][his] != 0:
                self.entrys[pc]["bc"][his] -= 1
            if self.entrys[pc]["his"] != 0:
                self.entrys[pc]["his"] -= 1

        if predict != outcome:
            self.entrys[pc]["mis"] += 1
            return "X"
        else:
            return "O"

    def get_his(self, pc, i):
        bc = ""
        if self.entrys[pc]["bc"][i] == 0:
            bc = "SN"
        elif self.entrys[pc]["bc"][i] == 1:
            bc = "WN"
        elif self.entrys[pc]["bc"][i] == 2:
            bc = "WT"
        elif self.entrys[pc]["bc"][i] == 3:
            bc = "ST"
        return bc

    def get_state(self, pc):
        his = str(self.entrys[pc]["his"])
        s = "({his}, {bc0}, {bc1}, {bc2}, {bc3})".format(his=his,
                                                         bc0=self.get_his(
                                                             pc, 0),
                                                         bc1=self.get_his(
                                                             pc, 1),
                                                         bc2=self.get_his(
                                                             pc, 2),
                                                         bc3=self.get_his(pc, 3))
        return s


class Machine_Code:
    def __init__(self, lines):
        self.pc = 0
        self.insts = []
        self.reg = {}  # store register num
        self.tag = {}  # stroe tag's pc
        self.parse(lines)
        self.init_reg()

    def parse(self, lines):  # store tag and remove tag from lines and split
        num = 0
        for line in lines:
            split = re.split(r'[;,\s]\s*', line)
            if len(split) == 1:  # represent the tag
                self.tag[split[0][:-1]] = num
            else:
                self.insts.append(split)
                num += 1

    def init_reg(self):
        self.reg["R0"] = 0

    def exe(self):
        cur_inst = self.insts[self.pc]
        # def : li, sub, subi, add, addi, and, andi, beq, bne, j,
        if cur_inst[1] == "li":  # 0x110 li R1, 0
            self.reg[cur_inst[2]] = int(cur_inst[3])
            self.pc += 1
            return "N"
        elif cur_inst[1] == "sub":  # 0x11C subi R2, R2, R3
            self.reg[cur_inst[2]] = self.reg[cur_inst[3]] - \
                self.reg[cur_inst[4]]
            self.pc += 1
            return "N"
        elif cur_inst[1] == "subi":  # 0x11C subi R2, R2, 1
            self.reg[cur_inst[2]] = self.reg[cur_inst[3]] - int(cur_inst[4])
            self.pc += 1
            return "N"
        elif cur_inst[1] == "add":  # 0x11C add R6, R5, R4
            self.reg[cur_inst[2]] = self.reg[cur_inst[3]] + \
                self.reg[cur_inst[4]]
            self.pc += 1
            return "N"
        elif cur_inst[1] == "addi":  # 0x11C addi R5, R5, 1
            self.reg[cur_inst[2]] = self.reg[cur_inst[3]] + int(cur_inst[4])
            self.pc += 1
            return "N"
        elif cur_inst[1] == "and":  # 0x11C andi R6, R6, R7
            self.reg[cur_inst[2]] = self.reg[cur_inst[3]
                                             ] & self.reg[cur_inst[4]]
            self.pc += 1
            return "N"
        elif cur_inst[1] == "andi":  # 0x11C andi R6, R6, 1
            self.reg[cur_inst[2]] = self.reg[cur_inst[3]] & int(cur_inst[4])
            self.pc += 1
            return "N"
        elif cur_inst[1] == "beq":  # 0x118 beq R1, R2, End
            if self.reg[cur_inst[2]] == self.reg[cur_inst[3]]:
                self.pc = self.tag[cur_inst[4]]
                return "T"
            else:
                self.pc += 1
                return "N"
        elif cur_inst[1] == "bne":  # 0x118 bne R6, R0, Endif
            if self.reg[cur_inst[2]] != self.reg[cur_inst[3]]:
                self.pc = self.tag[cur_inst[4]]
                return "T"
            else:
                self.pc += 1
                return "N"
        elif cur_inst[1] == "j":  # 0x120 j Loop
            self.pc = self.tag[cur_inst[2]]
            return "T"


def mode1(case_dir):
    f = open(case_dir, 'r')
    data = f.read()
    lines = data.splitlines()
    mc = Machine_Code(lines)
    fp = open("ans.txt", "w")

    entry_count = int(sys.argv[3])
    pred = Predictor(entry_count=entry_count)

    head = "|" + "entry".center(10) + "|" + "inst".center(10) + "|" + "state".center(20) + "|" + "predict".center(10) \
        + "|" + "outcome".center(10) + "|" + "correct".center(10) + "|\n"
    entry_ans = [head] * entry_count
    total_ans = head

    while True:
        if mc.pc >= len(mc.insts):  # end the machine code
            break
        # print(mc.insts[mc.pc])
        en = mc.pc % entry_count
        inst = mc.insts[mc.pc][0]
        state = pred.get_state(en)
        predict = pred.predict(en)
        outcome = mc.exe()
        correct = pred.update(en, predict, outcome)
        #print(type(en), type(inst), type(state), type(predict), type(outcome), type(correct))
        s = "|" + str(en).center(10) + "|" + inst.center(10) + "|" + state.center(20) + "|" + predict.center(10) \
            + "|" + outcome.center(10) + "|" + correct.center(10) + "|\n"
        entry_ans[en] += s
        total_ans += s
    fp.write(total_ans)
    total_mis = 0
    for i in range(0, entry_count):
        total_mis += pred.entrys[i]["mis"]
    fp.write("# Total Misprediction : " + str(total_mis) + "\n\n")

    for i in range(0, entry_count):
        fp.write(entry_ans[i])
        fp.write("# Entry" + str(i) + " Misprediction : " +
                 str(pred.entrys[i]["mis"]) + "\n\n")


def mode0(case_dir):
    f = open(case_dir, 'r')
    data = f.read()
    fp = open("ans.txt", "w")

    pred = Predictor(entry_count=1)
    en = 0

    fp.write("|" + "state".center(20) + "|" + "predict".center(10) +
             "|" + "outcome".center(10) + "|" + "correct".center(10) + "|\n")
    for outcome in data:
        state = pred.get_state(en)
        predict = pred.predict(en)
        correct = pred.update(en, predict, outcome)
        fp.write("|" + state.center(20) + "|" + predict.center(10) +
                 "|" + outcome.center(10) + "|" + correct.center(10) + "|\n")

    misprediction = str(pred.entrys[en]["mis"])
    fp.write("# Misprediction : " + misprediction)


# -------------------------- main --------------------------
mode = sys.argv[1]
case_dir = sys.argv[2]

if mode == "0":
    mode0(case_dir)
elif mode == "1":
    mode1(case_dir)
