def num_to_8bit(integer):
    y = bin(integer).replace("0b", "")
    z = []
    for i in range(8 - len(y)):
        z.append("0")
    z.append(y)
    return "".join(z)


def reg_bin(num, inslst, erdic):
    instructions = inslst
    errors = erdic
    if num == "0":
        return "000"
    elif num == "1":
        return "001"
    elif num == "2":
        return "010"
    elif num == "3":
        return "011"
    elif num == "4":
        return "100"
    elif num == "5":
        return "101"
    elif num == "6":
        return "110"
    elif num == "FLAGS":
        return "111"


def opcode(line, inslst, erdic):
    fw = line[0]
    instructions = inslst
    errors = erdic
    if fw == "hlt":
        return "10011"
    elif fw == "jmp":
        return "01111"
    elif fw == "jlt":
        return "10000"
    elif fw == "jgt":
        return "10001"
    elif fw == "je":
        return "10010"
    elif fw == "ld":
        return "00100"
    elif fw == "st":
        return "00101"
    elif fw == "add":
        return "00000"
    elif fw == "sub":
        return "00001"
    elif fw == "mul":
        return "00110"
    elif fw == "div":
        return "00111"
    elif fw == "rs":
        return "01000"
    elif fw == "ls":
        return "01001"
    elif fw == "xor":
        return "01010"
    elif fw == "or":
        return "01011"
    elif fw == "and":
        return "01100"
    elif fw == "not":
        return "01101"
    elif fw == "cmp":
        return "01110"
    elif fw == "mov":
        tw = line[2]
        if tw[0] == "$":
            return "00010"
        elif tw[0] == "R":
            return "00011"
        elif tw == "FLAGS":
            return "00011"
    else:
        # no type (error gen)
        errors[0][0] = True


def instruction_flow(ins_line, inslst, erdic, varlst, labeldic, countpar):
    # print(labeldic)
    labels = labeldic
    count = countpar
    variables = varlst
    instructions = inslst
    errors = erdic
    first_instruction = ins_line[0]
    ret = []
    for i in range(len(instructions)):
        if first_instruction == instructions[i]:
            if i == 1 or i == 2 or i == 6 or i == 10 or i == 11 or i == 12:
                # type A
                if len(ins_line) != 4:
                    errors[9][0] = True
                else:
                    ret.append(opcode(ins_line, instructions, errors))
                    ret.append("00")
                    if ins_line[1][0] == "R" and ins_line[2][0] == "R" and ins_line[3][0] == "R":
                        if 0 <= int(ins_line[1][-1]) <= 6:
                            ret.append(reg_bin(ins_line[1][-1], instructions, errors))
                            ret.append(reg_bin(ins_line[2][-1], instructions, errors))
                            ret.append(reg_bin(ins_line[3][-1], instructions, errors))
                        else:
                            errors[0][0] = True
                    else:
                        errors[0][0] = True
                return "".join(ret)
            elif i == 8 or i == 9:
                # type B
                ret.append(opcode(ins_line, instructions, errors))
                if ins_line[1][0] == "R":
                    if 0 <= int(ins_line[1][-1]) <= 6:
                        ret.append(reg_bin(ins_line[1][-1], instructions, errors))
                        if ins_line[2][0] == "$" and not ins_line[2][1:].isalpha() and 0 <= int(ins_line[2][1:]) <= 255:
                            ret.append(num_to_8bit(int(ins_line[2][1:])))
                        else:
                            errors[4][0] = True
                    else:
                        errors[0][0] = True
                else:
                    errors[0][0] = True
                return "".join(ret)
            elif i == 3:
                # mov instr (type B and C)
                ret.append(opcode(ins_line, instructions, errors))
                if ins_line[2][0] == "$":
                    if 0 <= int(ins_line[1][-1]) <= 6:
                        ret.append(reg_bin(ins_line[1][-1], instructions, errors))
                        if ins_line[2][0] == "$" and not ins_line[2][1:].isalpha() and 0 <= int(ins_line[2][1:]) <= 255:
                            ret.append(num_to_8bit(int(ins_line[2][1:])))
                        else:
                            errors[4][0] = True
                    else:
                        errors[0][0] = True
                elif ins_line[2][0] == "R":
                    ret.append("00000")
                    if 0 <= int(ins_line[1][-1]) <= 6:
                        ret.append(reg_bin(ins_line[1][-1], instructions, errors))
                        if 0 <= int(ins_line[2][-1]) <= 6:
                            ret.append(reg_bin(ins_line[2][-1], instructions, errors))
                        else:
                            errors[0][0] = True
                    else:
                        errors[0][0] = True
                elif ins_line[2] == "FLAGS":
                    ret.append("00000")
                    # print(ret)
                    if 0 <= int(ins_line[1][-1]) <= 6:
                        ret.append(reg_bin(ins_line[1][-1], instructions, errors))
                        if ins_line[2] == "FLAGS":
                            ret.append(reg_bin(ins_line[2], instructions, errors))

                        else:
                            errors[0][0] = True
                        # print(ret)
                    else:
                        errors[0][0] = True
                    # print(ret)
                else:
                    errors[9][0] = True
                # print(ret)
                return "".join(ret)
            elif i == 7 or i == 13 or i == 14:
                # type C (except mul)
                ret.append(opcode(ins_line, instructions, errors))
                ret.append("00000")
                if ins_line[2][0] == "R":
                    ret.append("00000")
                    if 0 <= int(ins_line[1][-1]) <= 6:
                        ret.append(reg_bin(ins_line[1][-1], instructions, errors))
                        if 0 <= int(ins_line[2][-1]) <= 6:
                            ret.append(reg_bin(ins_line[2][-1], instructions, errors))
                        else:
                            errors[0][0] = True
                    else:
                        errors[0][0] = True
                else:
                    errors[9][0] = True
                return "".join(ret)
            elif i == 4 or i == 5:
                # type D
                ret.append(opcode(ins_line, instructions, errors))
                if ins_line[1][0] == "R":
                    if 0 <= int(ins_line[1][-1]) <= 6:
                        ret.append(reg_bin(ins_line[1][-1], instructions, errors))
                        if len(ins_line) == 3 and ins_line[2] in variables:
                            flag1 = True
                            for j in range(len(variables)):
                                if variables[j] == ins_line[2]:
                                    ret.append(num_to_8bit(j + count))
                                    flag1 = False
                            if flag1:
                                errors[2] = True
                        else:
                            errors[9][0] = True
                    else:
                        errors[0][0] = True
                else:
                    errors[0][0] = True
                return "".join(ret)
            elif i == 15 or i == 16 or i == 17 or i == 18:
                # type E
                ret.append(opcode(ins_line, instructions, errors))
                ret.append("000")
                if len(ins_line) == 2:
                    flag2 = True
                    for x in labels:
                        if x[0] == ins_line[1]:
                            ret.append(num_to_8bit(x[1]))
                            flag2 = False
                    if flag2:
                        errors[2][0] = True
                else:
                    errors[9][0] = True
                return "".join(ret)
            elif i == 0:
                # type F
                ret.append(opcode(ins_line, instructions, errors))
                ret.append("00000000000")
                return "".join(ret)
    # no type (error gen)
    errors[-1][0] = True
    return "".join(ret)


def main():
    memory_array = []
    labels = []
    variables = []
    instructions = ["hlt", "add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp",
                    "jmp", "jlt", "jgt", "je"]
    errors = [[False, "Error: Typos in instruction name or register name"],  # A -0
              [False, "Error: Use of undefined variables"],  # B -1
              [False, "Error: Use of undefined labels"],  # C -2
              [False, "Error: Illegal use of FLAGS register"],  # D -3
              [False, "Error: Illegal Immediate values (less than 0 or more than 255)"],  # E -4
              [False, "Error: Misuse of labels as variables or vice-versa"],  # F -5
              [False, "Error: Variables not declared at the beginning"],  # G -6
              [False, "Error: Missing hlt instruction"],  # H -7
              [False, "Error: hlt not being used as the last instruction"],  # I -8
              [False, "Error: Wrong syntax used for instructions"],  # J -9
              [False, "General syntax Error"]]  # K -10
    reg_mem = [-1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0]  # r0 to r6 and FLAGS
    input_valid_lists = []
    nonvarcount = 0
    # taking and storing the input
    try:
        while True:
            rawline = input()
            if rawline == "":
                continue  # skip to next line input if input is empty
            line = rawline.rstrip().lstrip().split()
            if line[0] != "var":
                nonvarcount += 1
            if line[0][-1] == ":":  # label
                labels.append([line[0][:-1], nonvarcount])
            input_valid_lists.append(line)
    except EOFError:  # end of input, output is printed
        pass
    # print(input_valid_lists)
    # assembling the input
    count = 0
    result = []
    linecount = 0
    try:
        while linecount < len(input_valid_lists):
            line = input_valid_lists[linecount]
            firstword = line[0]
            if firstword == "var":  # variable declaration
                if len(line) == 2:
                    variables.append(line[1])
                else:
                    errors[10][0] = True
            elif firstword[-1] == ":":  # label
                labels.append([firstword[:-1], count])
                line.pop(0)
                result.append(instruction_flow(line, instructions, errors, variables, labels, nonvarcount))
                count += 1
            else:  # instructions
                result.append(instruction_flow(line, instructions, errors, variables, labels, nonvarcount))
                count += 1
            # print(errors)
            # print(count)
            # print(result)
            for err in errors:  # error gen
                if err[0]:
                    result = [err[1]]
                    assert False
            linecount += 1
        print("\n".join(result))
    except AssertionError:
        print("".join(result))


main()
