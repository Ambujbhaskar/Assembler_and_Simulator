class registerfile():
    def __init__(self):
        y = bin(0).replace("0b", "")
        z = ""
        for i in range(16 - len(y)):
            z = z + "0"
        z = z +y
        self.reg_file = [z]*8

    def dump(self):
        return self.reg_file[0] + " " + self.reg_file[1] + " " + self.reg_file[2] + " " + self.reg_file[3]+" " + self.reg_file[4] + " " + self.reg_file[5] + " " + self.reg_file[6] + " " + self.reg_file[7]