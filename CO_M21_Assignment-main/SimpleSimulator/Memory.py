
class Memory:
    def __init__(self):
        y = bin(0).replace("0b", "")
        z = ""
        for i in range(16 - len(y)):
            z = z + "0"
        z = z + y
        self.mem = [z] * 256
        try:
            for x in range(0, 256):
                inp = input()
                if inp == "":
                    break
                else:
                    self.mem[x] = inp
        except EOFError:
            pass

    def binaryToDecimal(self,binary):
        binary = int(binary)
        decimal, i, n = 0, 0, 0
        while (binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        return decimal

    def dump(self):
        for x in range(0,256):
            print(self.mem[x])

    def fetch(self, PC_value, cycle):
        return self.mem[Memory.binaryToDecimal(self,PC_value)]
