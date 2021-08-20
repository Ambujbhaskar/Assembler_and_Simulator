class executionengine():
    def __init__(self,mem_,regfile):
        self.mem = mem_.mem
        self.reg = regfile.reg_file

    def binaryToDecimal(self,binary):
        binary = int(binary)
        decimal, i, n = 0, 0, 0
        while (binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        return decimal

    def decimaltobinary(self,no):
        y = bin(no).replace("0b", "")
        z = ""
        if len(y)<=16:
            for i in range(16 - len(y)):
                z = z + "0"
            z = z + y
        else:
            z = y
        return z

    def reg_check(self,reg):
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

    def add(self,reg1, reg2, reg3):
        ind1 = executionengine.reg_check(self,reg1)
        ind2 = executionengine.reg_check(self,reg2)
        ind3 = executionengine.reg_check(self,reg3)
        self.reg[ind1] = executionengine.decimaltobinary(self,(executionengine.binaryToDecimal(self,self.reg[ind2]) + executionengine.binaryToDecimal(self,self.reg[ind3])))
        if len(self.reg[ind1]) > 16:
            self.reg[7] = self.reg[7][:12] + "1" + self.reg[7][13:16]

    def sub(self,reg1, reg2, reg3):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        ind3 = executionengine.reg_check(self, reg3)
        if executionengine.binaryToDecimal(self,self.reg[ind3]) > executionengine.binaryToDecimal(self,self.reg[ind2]):
            self.reg[ind1] = executionengine.decimaltobinary(self,0)
        else:
            self.reg[ind1] = executionengine.decimaltobinary(self, (executionengine.binaryToDecimal(self, self.reg[ind2]) - executionengine.binaryToDecimal(self,self.reg[ind3])))

    def movimm(self,reg1,imm):
        ind1 = executionengine.reg_check(self, reg1)
        self.reg[ind1] = "00000000" + imm

    def movreg(self,reg1,reg2):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        self.reg[ind1] = self.reg[ind2]

    def store(self,reg1,mem_add):
        ind1 = executionengine.reg_check(self, reg1)
        for x in range(0,256):
            if self.mem[x] == "0000000000000000":
                self.mem[x] = self.reg[ind1]
                break

    def mul(self, reg1,reg2,reg3):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        ind3 = executionengine.reg_check(self, reg3)
        self.reg[ind1] = executionengine.decimaltobinary(self, (executionengine.binaryToDecimal(self, self.reg[ind2]) * executionengine.binaryToDecimal(self,self.reg[ind3])))
        if len(self.reg[ind1]) > 16:
            self.reg[7] = self.reg[7][:12] + "1" + self.reg[7][13:16]

    def div(self,reg1,reg2):
        ind1 = executionengine.reg_check(self, reg1)
        ind2 = executionengine.reg_check(self, reg2)
        self.reg[0] = self.reg[ind1] / self.reg[ind2]
        self.reg[1] = self.reg[ind1] % self.reg[ind2]

    def rightshift(self,reg1, imm):
        ind1 = executionengine.reg_check(self, reg1)
        reg_int = executionengine.binaryToDecimal(self,self.reg[ind1])
        imm_int = executionengine.binaryToDecimal(self,imm)
        shift_right = reg_int >> imm_int
        self.reg[ind1] = executionengine.decimaltobinary(self,shift_right)
        
    def leftshift(self,reg1, imm):
        ind1 = executionengine.reg_check(self, reg1)
        reg_int = executionengine.binaryToDecimal(self, self.reg[ind1])
        imm_int = executionengine.binaryToDecimal(self, imm)
        shift_left = reg_int << imm_int
        self.reg[ind1] = executionengine.decimaltobinary(self, shift_left)

    def execute(self,inst,cycle):
        opcode = inst[0:5]
        if opcode == "00000":
            executionengine.add(self,inst[7:10], inst[10:13], inst[13:16])
            return False, 1

        if opcode == "00001":
            executionengine.sub(self, inst[7:10], inst[10:13], inst[13:16])
            return False, 1

        if opcode == "00010":
            executionengine.movimm(self,inst[5:8],inst[8:16])
            return False, 1

        if opcode == "00011":
            executionengine.movreg(self,inst[10:13], inst[13:16])
            return False, 1

        if opcode == "00101":
            executionengine.store(self,inst[5:8],inst[8:16])
            return False, 1

        if opcode == "00110":
            executionengine.mul(self,inst[7:10], inst[10:13], inst[13:16])
            return False, 1

        if opcode == "00111":
            executionengine.div(self,inst[10:13], inst[13:16])
            return False, 1

        if opcode == "01000":
            executionengine.rightshift(self,inst[5:8],inst[8:16])
            return False, 1

        if opcode == "01001":
            executionengine.leftshift(self,inst[5:8],inst[8:16])
            return False, 1

        if opcode == "10011":
            return True, 0


