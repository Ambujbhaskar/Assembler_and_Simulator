class executionengine():
    def __init__(self,mem,regfile):
        self.mem = mem
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
        for i in range(16 - len(y)):
            z = z + "0"
        z = z + y
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

    def execute(self,inst,cycle):
        opcode = inst[0:5]
        if opcode == "00000":
            executionengine.add(self,inst[7:10], inst[10:13], inst[13:16])
            return False, 1
        if opcode == "10011":
            return True, 0


