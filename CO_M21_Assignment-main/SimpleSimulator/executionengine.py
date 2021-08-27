class executionengine():
    def __init__(self, mem_, regfile):
        self.mem = mem_.mem
        self.reg = regfile.reg_file

    def binaryToDecimal(self, binary):
        binary = int(binary)
        decimal, i, n = 0, 0, 0
        while (binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        return decimal

    def decimaltobinary(self, no):
        y = bin(no).replace("0b", "")
        z = ""
        if len(y) <= 16:
            for i in range(16 - len(y)):
                z = z + "0"
            z = z + y
        else:
            z = y
        return z

    def reg_check(self, reg):
        if reg == "000":
            return 0
        elif reg == "001":
            return 1
        elif reg == "010":
            return 2
        elif reg == "011":
            return 3
        elif reg == "100":
            return 4
        elif reg == "101":
            return 5
        elif reg == "110":
            return 6
        elif reg == "111":
            return 7

    def add(self, reg1, reg2, reg3):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        ind3 = executionengine.reg_check(self, reg3)
        self.reg[ind1] = executionengine.decimaltobinary(
            self, (executionengine.binaryToDecimal(self, self.reg[ind2]) +
                   executionengine.binaryToDecimal(self, self.reg[ind3])))
        if len(self.reg[ind1]) > 16:
            length_reg = len(self.reg[ind1])
            self.reg[ind1] = self.reg[ind1][len(self.reg[ind1])-16:length_reg]
            self.reg[7] = self.reg[7][:12] + "1" + self.reg[7][13:16]

    def sub(self, reg1, reg2, reg3):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        ind3 = executionengine.reg_check(self, reg3)
        if executionengine.binaryToDecimal(
                self, self.reg[ind3]) > executionengine.binaryToDecimal(
                    self, self.reg[ind2]):
            self.reg[ind1] = executionengine.decimaltobinary(self, 0)
            self.reg[7] = self.reg[7][:12] + "1" + self.reg[7][13:16]
        else:
            self.reg[ind1] = executionengine.decimaltobinary(
                self, (executionengine.binaryToDecimal(self, self.reg[ind2]) -
                       executionengine.binaryToDecimal(self, self.reg[ind3])))

    def movimm(self, reg1, imm):
        ind1 = executionengine.reg_check(self, reg1)
        self.reg[ind1] = "00000000" + imm

    def movreg(self, reg1, reg2):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        self.reg[ind1] = self.reg[ind2]

    def movflag(self, reg1):
        ind1 = executionengine.reg_check(self, reg1)
        self.reg[ind1] = self.reg[7]
        if self.reg[7][12:13] == "1":
            self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
        if self.reg[7][13:14] == "1":
            self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
        if self.reg[7][14:15] == "1":
            self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
        if self.reg[7][15:16] == "1":
            self.reg[7] = self.reg[7][0:15] + "0"

    def load(self, reg1, var_pos):
        ind1 = executionengine.reg_check(self, reg1)
        var_pos_int = executionengine.binaryToDecimal(self, var_pos)
        self.reg[ind1] = self.mem[var_pos_int]

    def store(self, reg1, var_pos):
        ind1 = executionengine.reg_check(self, reg1)
        var_pos_int = executionengine.binaryToDecimal(self, var_pos)
        self.mem[var_pos_int] = self.reg[ind1]

    def mul(self, reg1, reg2, reg3):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        ind3 = executionengine.reg_check(self, reg3)
        self.reg[ind1] = executionengine.decimaltobinary(
            self, (executionengine.binaryToDecimal(self, self.reg[ind2]) *
                   executionengine.binaryToDecimal(self, self.reg[ind3])))
        if len(self.reg[ind1]) > 16:
            length_reg = len(self.reg[ind1])
            self.reg[ind1] = self.reg[ind1][len(self.reg[ind1]) - 16:length_reg]
            self.reg[7] = self.reg[7][:12] + "1" + self.reg[7][13:16]

    def div(self, reg1, reg2):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        self.reg[0] = executionengine.decimaltobinary(self,int(executionengine.binaryToDecimal(self,self.reg[ind1]) / executionengine.binaryToDecimal(self,self.reg[ind2])))
        self.reg[1] = executionengine.decimaltobinary(self,executionengine.binaryToDecimal(self,self.reg[ind1]) % executionengine.binaryToDecimal(self,self.reg[ind2]))


    def rightshift(self, reg1, imm):
        ind1 = executionengine.reg_check(self, reg1)
        reg_int = executionengine.binaryToDecimal(self, self.reg[ind1])
        imm_int = executionengine.binaryToDecimal(self, imm)
        shift_right = reg_int >> imm_int
        self.reg[ind1] = executionengine.decimaltobinary(self, shift_right)

    def leftshift(self, reg1, imm):
        ind1 = executionengine.reg_check(self, reg1)
        reg_int = executionengine.binaryToDecimal(self, self.reg[ind1])
        imm_int = executionengine.binaryToDecimal(self, imm)
        shift_left = reg_int << imm_int
        self.reg[ind1] = executionengine.decimaltobinary(self, shift_left)

    def xoro(self, reg1, reg2, reg3):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        ind3 = executionengine.reg_check(self, reg3)
        reg_int1 = executionengine.binaryToDecimal(self, self.reg[ind1])
        reg_int2 = executionengine.binaryToDecimal(self, self.reg[ind2])
        reg_int3 = executionengine.binaryToDecimal(self, self.reg[ind3])
        xor_op = reg_int2 ^ reg_int3
        self.reg[ind1] = executionengine.decimaltobinary(self, xor_op)

    def oro(self, reg1, reg2, reg3):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        ind3 = executionengine.reg_check(self, reg3)
        reg_int1 = executionengine.binaryToDecimal(self, self.reg[ind1])
        reg_int2 = executionengine.binaryToDecimal(self, self.reg[ind2])
        reg_int3 = executionengine.binaryToDecimal(self, self.reg[ind3])
        or_op = reg_int2 | reg_int3
        self.reg[ind1] = executionengine.decimaltobinary(self, or_op)

    def ando(self, reg1, reg2, reg3):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        ind3 = executionengine.reg_check(self, reg3)
        reg_int1 = executionengine.binaryToDecimal(self, self.reg[ind1])
        reg_int2 = executionengine.binaryToDecimal(self, self.reg[ind2])
        reg_int3 = executionengine.binaryToDecimal(self, self.reg[ind3])
        and_op = reg_int2 & reg_int3
        self.reg[ind1] = executionengine.decimaltobinary(self, and_op)

    def inverto(self, reg1, reg2):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        number = self.reg[ind2]
        inverse = number.replace('1', '2')
        inverse = inverse.replace('0', '1')
        inverse = inverse.replace('2', '0')
        self.reg[ind1] = inverse

    def comparo(self, reg1, reg2):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        reg_int1 = executionengine.binaryToDecimal(self, self.reg[ind1])
        reg_int2 = executionengine.binaryToDecimal(self, self.reg[ind2])
        if reg_int1 == reg_int2:
            self.reg[7] = self.reg[7][:15] + "1" + self.reg[7][16:16]
        elif reg_int1 > reg_int2:
            self.reg[7] = self.reg[7][:14] + "1" + self.reg[7][15:16]
        else:
            self.reg[7] = self.reg[7][:13] + "1" + self.reg[7][14:16]

    def jmp(self):
        return True

    def jlt(self):
        if self.reg[7][13:14] == "1":
            return True
        else:
            return False

    def jgt(self):
        if self.reg[7][14:15] == "1":
            return True
        else:
            return False

    def je(self):
        if self.reg[7][15:16] == "1":
            return True
        else:
            return False

    def execute(self, inst, cycle, PC):
        opcode = inst[0:5]
        PC_int = executionengine.binaryToDecimal(self, PC)
        if opcode == "00000":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.add(self, inst[7:10], inst[10:13], inst[13:16])
            return False, PC_int + 1

        if opcode == "00001":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.sub(self, inst[7:10], inst[10:13], inst[13:16])
            return False, PC_int + 1

        if opcode == "00010":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.movimm(self, inst[5:8], inst[8:16])
            return False, PC_int + 1

        if opcode == "00011":
            if inst[13:16] == "111":
                executionengine.movflag(self, inst[10:13])
                if self.reg[7][12:13] == "1":
                    self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
                if self.reg[7][13:14] == "1":
                    self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
                if self.reg[7][14:15] == "1":
                    self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
                if self.reg[7][15:16] == "1":
                    self.reg[7] = self.reg[7][0:15] + "0"
                return False, PC_int + 1
            else:
                executionengine.movreg(self, inst[10:13], inst[13:16])
                if self.reg[7][12:13] == "1":
                    self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
                if self.reg[7][13:14] == "1":
                    self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
                if self.reg[7][14:15] == "1":
                    self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
                if self.reg[7][15:16] == "1":
                    self.reg[7] = self.reg[7][0:15] + "0"
                return False, PC_int + 1

        if opcode == "00100":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.load(self, inst[5:8], inst[8:16])
            return False, PC_int + 1

        if opcode == "00101":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.store(self, inst[5:8], inst[8:16])
            return False, PC_int + 1

        if opcode == "00110":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.mul(self, inst[7:10], inst[10:13], inst[13:16])
            return False, PC_int + 1

        if opcode == "00111":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.div(self, inst[10:13], inst[13:16])
            return False, PC_int + 1

        if opcode == "01000":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.rightshift(self, inst[5:8], inst[8:16])
            return False, PC_int + 1

        if opcode == "01001":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.leftshift(self, inst[5:8], inst[8:16])
            return False, PC_int + 1

        if opcode == "01010":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.xoro(self, inst[7:10], inst[10:13], inst[13:16])
            return False, PC_int + 1

        if opcode == "01011":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.oro(self, inst[7:10], inst[10:13], inst[13:16])
            return False, PC_int + 1

        if opcode == "01100":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.ando(self, inst[7:10], inst[10:13], inst[13:16])
            return False, PC_int + 1

        if opcode == "01101":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.inverto(self, inst[10:13], inst[13:16])
            return False, PC_int + 1
        if opcode == "01110":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            executionengine.comparo(self, inst[10:13], inst[13:16])
            return False, PC_int + 1

        if opcode == "01111":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            check = executionengine.jmp(self)
            if check:
                convert_decimal = executionengine.binaryToDecimal(self, inst[8:16])
                return False, convert_decimal

        if opcode == "10000":
            check_flag_lt = executionengine.jlt(self)
            if check_flag_lt:
                convert_decimal = executionengine.binaryToDecimal(
                    self, inst[8:16])
                if self.reg[7][12:13] == "1":
                    self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
                if self.reg[7][13:14] == "1":
                    self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
                if self.reg[7][14:15] == "1":
                    self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
                if self.reg[7][15:16] == "1":
                    self.reg[7] = self.reg[7][0:15] + "0"
                return False, convert_decimal
            else:
                if self.reg[7][12:13] == "1":
                    self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
                if self.reg[7][13:14] == "1":
                    self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
                if self.reg[7][14:15] == "1":
                    self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
                if self.reg[7][15:16] == "1":
                    self.reg[7] = self.reg[7][0:15] + "0"
                return False, PC_int + 1

        if opcode == "10001":
            check_flag_gt = executionengine.jgt(self)
            if check_flag_gt:
                convert_decimal = executionengine.binaryToDecimal(
                    self, inst[8:16])
                if self.reg[7][12:13] == "1":
                    self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
                if self.reg[7][13:14] == "1":
                    self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
                if self.reg[7][14:15] == "1":
                    self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
                if self.reg[7][15:16] == "1":
                    self.reg[7] = self.reg[7][0:15] + "0"
                return False, convert_decimal
            else:
                if self.reg[7][12:13] == "1":
                    self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
                if self.reg[7][13:14] == "1":
                    self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
                if self.reg[7][14:15] == "1":
                    self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
                if self.reg[7][15:16] == "1":
                    self.reg[7] = self.reg[7][0:15] + "0"
                return False, PC_int + 1

        if opcode == "10010":
            check_flag_eq = executionengine.je(self)
            if check_flag_eq:
                convert_decimal = executionengine.binaryToDecimal(
                    self, inst[8:16])
                if self.reg[7][12:13] == "1":
                    self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
                if self.reg[7][13:14] == "1":
                    self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
                if self.reg[7][14:15] == "1":
                    self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
                if self.reg[7][15:16] == "1":
                    self.reg[7] = self.reg[7][0:15] + "0"
                return False, convert_decimal
            else:
                if self.reg[7][12:13] == "1":
                    self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
                if self.reg[7][13:14] == "1":
                    self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
                if self.reg[7][14:15] == "1":
                    self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
                if self.reg[7][15:16] == "1":
                    self.reg[7] = self.reg[7][0:15] + "0"
                return False, PC_int + 1

        if opcode == "10011":
            if self.reg[7][12:13] == "1":
                self.reg[7] = self.reg[7][0:12] + "0" + self.reg[7][13:16]
            if self.reg[7][13:14] == "1":
                self.reg[7] = self.reg[7][0:13] + "0" + self.reg[7][14:16]
            if self.reg[7][14:15] == "1":
                self.reg[7] = self.reg[7][0:14] + "0" + self.reg[7][15:16]
            if self.reg[7][15:16] == "1":
                self.reg[7] = self.reg[7][0:15] + "0"
            return True, PC_int
