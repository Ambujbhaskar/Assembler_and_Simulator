class programcounter():
    def __init__(self, n):
        y = bin(n).replace("0b", "")
        z = ""
        for i in range(8 - len(y)):
            z = z + "0"
        z = z + y
        self.PCdecimal = n  # for plot
        self.PC = z

    def decimaltobinary(self, no):
        y = bin(no).replace("0b", "")
        z = ""
        for i in range(8 - len(y)):
            z = z + "0"
        z = z + y
        return z

    def getPCdec(self):
        return self.PCdecimal

    def getVal(self):
        return self.PC

    def dump(self):
        return self.PC

    def update(self, next):
        self.PC = programcounter.decimaltobinary(self, next)
        self.PCdecimal = next
