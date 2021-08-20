class programcounter():
    def __init__(self, n):
        y = bin(n).replace("0b", "")
        z = ""
        for i in range(8 - len(y)):
            z = z + "0"
        z = z + y
        self.PC = z

    def decimaltobinary(self, no):
        y = bin(no).replace("0b", "")
        z = ""
        for i in range(8 - len(y)):
            z = z + "0"
        z = z + y
        return z

    def getVal(self):
        return self.PC

    def dump(self):
        return self.PC

    def update(self, next):
        next_bin = bin(next).replace("0b", "")
        next_final = ""
        for i in range(8 - len(next_bin)):
            next_final = next_final + "0"
        next_final = next_final + next_bin
        self.PC = programcounter.decimaltobinary(self, (int(self.PC,2) + int(next_final,2)))
