import re



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
        if len(line) == 3:
            tw = line[2]
            if tw[0] == "$":
                return "00010"
            elif tw[0] == "R":
                return "00011"
            elif tw == "FLAGS":
                return "00011"
            else:
                return ""
        else:
            return ""

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
    line_error = -2
    for i in range(len(instructions)):
        if first_instruction == instructions[i]:

            if i == 1 or i == 2 or i == 6 or i == 10 or i == 11 or i == 12:  # "add", "sub", "mul", "xor", "or", "and"
                # type A
                # error handling
                if len(ins_line) != 4:
                    if len(ins_line) > 4:
                        errors[-1][0] = True
                        line_error = -1
                    else:
                        if len(ins_line) == 3:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                check_a = True
                                for x in variables:
                                    if x == ins_line[2]:
                                        check_a = False
                                        errors[-1][0] = True
                                        line_error = -1
                                if check_a:
                                    if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    elif ins_line[2][0] == "$" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 255:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        else:
                            if len(ins_line) == 2:
                                flag_check = True
                                for x in labels:
                                    if x[0] == ins_line[1]:
                                        flag_check = False
                                        errors[9][0] = True
                                        line_error = 9
                                if flag_check:
                                    errors[-1][0] = True
                                    line_error = -1
                            else:
                                errors[9][0] = True
                                line_error = 9
                # assembling
                else:
                    ret.append(opcode(ins_line, instructions, errors))
                    ret.append("00")
                    if ins_line[1] != "FLAGS" and ins_line[2] != "FLAGS" and ins_line[3] != "FLAGS":
                        if ins_line[1][0] == "R" and ins_line[2][0] == "R" and ins_line[3][0] == "R":
                            if ins_line[1][1:].isnumeric() and ins_line[2][1:].isnumeric() and ins_line[3][
                                                                                               1:].isnumeric():
                                if 0 <= int(ins_line[1][1:]) <= 6 and 0 <= int(ins_line[2][1:]) <= 6 and 0 <= int(
                                        ins_line[3][1:]) <= 6:
                                    ret.append(reg_bin(ins_line[1][1:], instructions, errors))
                                    ret.append(reg_bin(ins_line[2][1:], instructions, errors))
                                    ret.append(reg_bin(ins_line[3][1:], instructions, errors))
                                else:
                                    errors[0][0] = True
                                    line_error = 0
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        else:
                            errors[-1][0] = True
                            line_error = -1
                    else:
                        errors[3][0] = True
                        line_error = 3
                return "".join(ret), line_error


            elif i == 8 or i == 9:  # "rs", "ls"
                # type B
                ret.append(opcode(ins_line, instructions, errors))
                if len(ins_line) == 3:
                    if ins_line[1][0] == "R":
                        if ins_line[1][1:].isnumeric():
                            if 0 <= int(ins_line[1][1:]) <= 6:
                                ret.append(reg_bin(ins_line[1][1:], instructions, errors))
                                if ins_line[2][0] == "$":
                                    if ins_line[2][1:].isnumeric():
                                        if 0 <= int(ins_line[2][1:]) <= 255:
                                            ret.append(num_to_8bit(int(ins_line[2][1:])))
                                        else:
                                            errors[4][0] = True
                                            line_error = 4
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    if ins_line[2][0] == "R" and not ins_line[2][1:].isalpha() and 0 <= int(
                                            ins_line[2][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        checker = True
                                        for x in variables:
                                            if x == ins_line[2]:
                                                checker = False
                                                errors[9][0] = True
                                                line_error = 9
                                        if checker:
                                            errors[-1][0] = True
                                            line_error = -1
                            else:
                                errors[0][0] = True
                                line_error = 0
                        else:
                            errors[-1][0] = True
                            line_error = -1
                    else:
                        if ins_line[1] == "FLAGS":
                            errors[3][0] = True
                            line_error = 3
                        else:
                            errors[-1][0] = True
                            line_error = -1
                else:
                    if len(ins_line) > 4:
                        errors[-1][0] = True
                        line_error = -1
                    else:
                        if len(ins_line) == 4:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                        ins_line[2][1:]) <= 6:
                                    if ins_line[3][0] == "R" and ins_line[3][1:].isnumeric() and 0 <= int(
                                            ins_line[3][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    errors[-1][0] = True
                                    line_error = -1
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        elif len(ins_line) == 2:
                            flag = True
                            for x in labels:
                                if x[0] == ins_line[1]:
                                    flag = False
                                    errors[9][0] = True
                                    line_error = 9
                            if flag:
                                errors[-1][0] = True
                                line_error = -1
                        else:
                            errors[9][0] = True
                            line_error = 9
                return "".join(ret),line_error


            elif i == 3:  # "mov"
                # mov instr (type B and C)
                ret.append(opcode(ins_line, instructions, errors))
                if len(ins_line) == 3:
                    if ins_line[1][0] == "R":
                        if ins_line[1][1:].isnumeric():
                            if ins_line[2][0] == "$":
                                if 0 <= int(ins_line[1][1:]) <= 6:
                                    ret.append(reg_bin(ins_line[1][1:], instructions, errors))
                                    if ins_line[2][1:].isnumeric():
                                        if 0 <= int(ins_line[2][1:]) <= 255:
                                            ret.append(num_to_8bit(int(ins_line[2][1:])))
                                        else:
                                            errors[4][0] = True
                                            line_error = 4
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    errors[0][0] = True
                                    line_error = 0
                            elif ins_line[2][0] == "R":
                                ret.append("00000")
                                if 0 <= int(ins_line[1][1:]) <= 6:
                                    ret.append(reg_bin(ins_line[1][1:], instructions, errors))
                                    if ins_line[2][1:].isnumeric():
                                        if 0 <= int(ins_line[2][1:]) <= 6:
                                            ret.append(reg_bin(ins_line[2][1:], instructions, errors))
                                        else:
                                            errors[0][0] = True
                                            line_error = 0
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    errors[0][0] = True
                                    line_error = 0
                            elif ins_line[2] == "FLAGS":
                                ret.append("00000")
                                # print(ret)
                                if 0 <= int(ins_line[1][1:]) <= 6:
                                    ret.append(reg_bin(ins_line[1][1:], instructions, errors))
                                    ret.append(reg_bin(ins_line[2], instructions, errors))
                                else:
                                    errors[0][0] = True
                                    line_error = 0
                                # print(ret)
                            else:
                                flag = True
                                for x in variables:
                                    if x == ins_line[2]:
                                        flag = False
                                        errors[9][0] = True
                                        line_error = 9
                                if flag:
                                    errors[-1][0] = True
                                    line_error = -1
                        else:
                            errors[-1][0] = True
                            line_error = -1
                    else:
                        if ins_line[1] == "FLAGS":
                            errors[3][0] = True
                            line_error = 3
                        else:
                            errors[-1][0] = True
                            line_error = -1
                else:
                    if len(ins_line) > 4:
                        errors[-1][0] = True
                        line_error = -1
                    else:
                        if len(ins_line) == 4:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                        ins_line[2][1:]) <= 6:
                                    if ins_line[3][0] == "R" and ins_line[3][1:].isnumeric() and 0 <= int(
                                            ins_line[3][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    errors[-1][0] = True
                                    line_error = -1
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        elif len(ins_line) == 2:
                            flag = True
                            for x in labels:
                                if x[0] == ins_line[1]:
                                    flag = False
                                    errors[9][0] = True
                                    line_error = 9
                            if flag:
                                errors[-1][0] = True
                                line_error = -1
                        else:
                            errors[9][0] = True
                            line_error = 9
                # print(ret)
                return "".join(ret),line_error


            elif i == 7 or i == 13 or i == 14:  # "div", "not", "cmp"
                # type C (except mul)
                ret.append(opcode(ins_line, instructions, errors))
                ret.append("00000")
                if len(ins_line) == 3:
                    if ins_line[1][0] == "R":
                        if ins_line[1][1:].isnumeric():
                            if ins_line[2][0] == "R":
                                if ins_line[2][1:].isnumeric():
                                    if 0 <= int(ins_line[1][1:]) <= 6:
                                        ret.append(reg_bin(ins_line[1][1:], instructions, errors))
                                        if 0 <= int(ins_line[2][1:]) <= 6:
                                            ret.append(reg_bin(ins_line[2][1:], instructions, errors))
                                        else:
                                            errors[0][0] = True
                                            line_error = 0
                                    else:
                                        errors[0][0] = True
                                        line_error = 0
                                else:
                                    errors[-1][0] = True
                                    line_error = -1
                            else:
                                checking = True
                                for x in variables:
                                    if x == ins_line[2]:
                                        checking = False
                                        errors[9][0] = True
                                        line_error = 9
                                if checking:
                                    if ins_line[2][0] == "$" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 255:
                                        errors[9][0] = True
                                        line_error = 9
                                    elif ins_line[2] == "FLAGS":
                                        errors[3][0] = True
                                        line_error = 3
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                        else:
                            errors[-1][0] = True
                            line_error = -1
                    else:
                        if ins_line[1] == "FLAGS":
                            errors[3][0] = True
                            line_error = 3
                        else:
                            errors[-1][0] = True
                            line_error = -1
                else:
                    if len(ins_line) > 4:
                        errors[-1][0] = True
                        line_error = -1
                    else:
                        if len(ins_line) == 4:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                        ins_line[2][1:]) <= 6:
                                    if ins_line[3][0] == "R" and ins_line[3][1:].isnumeric() and 0 <= int(
                                            ins_line[3][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    errors[-1][0] = True
                                    line_error = -1
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        elif len(ins_line) == 2:
                            flag = True
                            for x in labels:
                                if x[0] == ins_line[1]:
                                    flag = False
                                    errors[9][0] = True
                                    line_error = 9
                            if flag:
                                errors[-1][0] = True
                                line_error = -1
                        else:
                            errors[9][0] = True
                            line_error = 9
                return "".join(ret),line_error


            elif i == 4 or i == 5:  # "ld", "st"
                # type D
                ret.append(opcode(ins_line, instructions, errors))
                if len(ins_line) == 3:
                    if ins_line[1][0] == "R":
                        if ins_line[1][1:].isnumeric():
                            if 0 <= int(ins_line[1][-1]) <= 6:
                                ret.append(reg_bin(ins_line[1][1:], instructions, errors))
                                flag1 = True
                                for j in range(len(variables)):
                                    if variables[j] == ins_line[2]:
                                        ret.append(num_to_8bit(j + count))
                                        flag1 = False
                                for k in labels:
                                    if k[0] == ins_line[2]:
                                        flag1 = False
                                        errors[5][0] = True
                                        line_error = 5
                                if flag1:
                                    if ins_line[2][0] == "$" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 255:
                                        errors[9][0] = True
                                        line_error = 9
                                    elif ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[1][0] = True
                                        line_error = 1
                            else:
                                errors[0][0] = True
                                line_error = 0
                        else:
                            errors[-1][0] = True
                            line_error = -1
                    else:
                        if ins_line[1] == "FLAGS":
                            errors[3][0] = True
                            line_error = 3
                        else:
                            errors[-1][0] = True
                            line_error = -1
                else:
                    if len(ins_line) > 4:
                        errors[-1][0] = True
                        line_error = -1
                    else:
                        if len(ins_line) == 4:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                        ins_line[2][1:]) <= 6:
                                    if ins_line[3][0] == "R" and ins_line[3][1:].isnumeric() and 0 <= int(
                                            ins_line[3][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    errors[-1][0] = True
                                    line_error = -1
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        elif len(ins_line) == 2:
                            flag = True
                            for x in labels:
                                if x[0] == ins_line[1]:
                                    flag = False
                                    errors[9][0] = True
                                    line_error = 9
                            if flag:
                                errors[-1][0] = True
                                line_error = -1
                        else:
                            errors[9][0] = True
                            line_error = 9
                return "".join(ret),line_error


            elif i == 15 or i == 16 or i == 17 or i == 18:  # "jmp", "jlt", "jgt", "je"
                # type E
                ret.append(opcode(ins_line, instructions, errors))
                ret.append("000")
                if len(ins_line) == 2:
                    flag2 = True
                    for x in labels:
                        if x[0] == ins_line[1]:
                            ret.append(num_to_8bit(x[1]))
                            flag2 = False
                    for y in variables:
                        if y == ins_line[1]:
                            flag2 = False
                            errors[5][0] = True
                            line_error = 5
                    if flag2:
                        errors[2][0] = True
                        line_error = 2
                else:
                    if len(ins_line) > 4:
                        errors[-1][0] = True
                        line_error = -1
                    else:
                        if len(ins_line) == 4:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                        ins_line[2][1:]) <= 6:
                                    if ins_line[3][0] == "R" and ins_line[3][1:].isnumeric() and 0 <= int(
                                            ins_line[3][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    errors[-1][0] = True
                                    line_error = -1
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        elif len(ins_line) == 3:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                check_a = True
                                for x in variables:
                                    if x == ins_line[2]:
                                        check_a = False
                                        errors[-1][0] = True
                                        line_error = -1
                                if check_a:
                                    if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    elif ins_line[2][0] == "$" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 255:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        else:
                            errors[9][0] = True
                            line_error = 9

                return "".join(ret),line_error


            elif i == 0:
                # type F
                if len(ins_line) == 1:
                    ret.append(opcode(ins_line, instructions, errors))
                    ret.append("00000000000")
                else:
                    if len(ins_line) > 4:
                        errors[-1][0] = True
                        line_error = -1
                    else:
                        if len(ins_line) == 4:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                        ins_line[2][1:]) <= 6:
                                    if ins_line[3][0] == "R" and ins_line[3][1:].isnumeric() and 0 <= int(
                                            ins_line[3][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                                else:
                                    errors[-1][0] = True
                                    line_error = -1
                            else:
                                errors[-1][0] = True
                                line_error = -1
                        elif len(ins_line) == 3:
                            if ins_line[1][0] == "R" and ins_line[1][1:].isnumeric() and 0 <= int(ins_line[1][1:]) <= 6:
                                check_a = True
                                for x in variables:
                                    if x == ins_line[2]:
                                        check_a = False
                                        errors[-1][0] = True
                                        line_error = -1
                                if check_a:
                                    if ins_line[2][0] == "R" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 6:
                                        errors[9][0] = True
                                        line_error = 9
                                    elif ins_line[2][0] == "$" and ins_line[2][1:].isnumeric() and 0 <= int(
                                            ins_line[2][1:]) <= 255:
                                        errors[9][0] = True
                                        line_error = 9
                                    else:
                                        errors[-1][0] = True
                                        line_error = -1
                        elif len(ins_line) == 2:
                            flag = True
                            for x in labels:
                                if x[0] == ins_line[1]:
                                    flag = False
                                    errors[9][0] = True
                                    line_error = 9
                            if flag:
                                errors[-1][0] = True
                                line_error = -1
                return "".join(ret), line_error

    # no type (error gen)
    errors[-1][0] = True
    line_error = -1
    return "".join(ret),line_error


def main():
    memory_array = []
    labels = []
    variables = []
    instructions = ["hlt", "add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp",
                    "jmp", "jlt", "jgt", "je"]
    errors = [[False, "Typos in instruction name or register name",[]],  # A -0
              [False, "Use of undefined variables",[]],  # B -1
              [False, "Use of undefined labels",[]],  # C -2
              [False, "Illegal use of FLAGS register",[]],  # D -3
              [False, "Illegal Immediate values (less than 0 or more than 255)",[]],  # E -4
              [False, "Misuse of labels as variables or vice-versa",[]],  # F -5
              [False, "Variables not declared at the beginning",[]],  # G -6
              [False, "Missing hlt instruction",[]],  # H -7
              [False, "hlt not being used as the last instruction",[]],  # I -8
              [False, "Wrong syntax used for instructions",[]],  # J -9
              [False, "General syntax Error",[]]]  # K -10
    input_valid_lists = []
    nonvarcount = 0
    count_hlt = 0
    after_hlt = 0
    input_line_num = 0
    count_hlt_no = 0
    after_hlt_query = 0
    hlt_no = 0
    int_hlt = 0
    k = 0
    # taking and storing the input
    try:
        while True:
            rawline = input()
            input_line_num += 1

            if rawline == "":
                continue  # skip to next line input if input is empty

            line = rawline.rstrip().lstrip().split()

            if line[0] != "var":
                if after_hlt >= 1:
                    if line[0] != "hlt":
                        after_hlt_query += 1
                nonvarcount += 1

            if nonvarcount > 0:
                if line[0] == "var":
                    if after_hlt >= 1:
                        after_hlt_query += 1
                    if len(line) == 2:
                        errors[6][0] = True
                        errors[6][2].append(input_line_num)
                    else:
                        errors[-1][0] = True
                        errors[-1][2].append(input_line_num)

            if line[0][-1] == ":":  # label
                if len(line) > 1:
                    if line[1] == "hlt":
                        if k == 0:
                            int_hlt = input_line_num
                            k += 1
                        hlt_no = input_line_num
                        after_hlt = 1
                        count_hlt += 1
                        count_hlt_no = input_line_num
                        labels.append([line[0][:-1], nonvarcount - 1])
                    else:
                        if after_hlt >= 1:
                            after_hlt_query += 1
                        labels.append([line[0][:-1], nonvarcount - 1])

            input_valid_lists.append([line, input_line_num])
            if line[0] == "hlt":
                if k == 0:
                    int_hlt = input_line_num
                    k += 1
                if after_hlt >= 1:
                    after_hlt_query += 1
                hlt_no = input_line_num
                after_hlt = 1
                count_hlt += 1
                count_hlt_no = input_line_num

    except EOFError:  # end of input
        pass

    # assembling the input
    count = 0
    result = []
    linecount = 0
    if count_hlt > 1:
        errors[-1][0] = True
        errors[-1][2].append(int_hlt)
    if count_hlt == 0:
        errors[7][0] = True
        errors[7][2].append(input_line_num)
    if hlt_no != input_line_num:
        errors[8][0] = True
        errors[8][2].append(input_line_num - after_hlt_query+1)
    check_var_label_name = "^[A-Za-z0-9_]*$"

    try:
        while linecount < len(input_valid_lists):
            line = input_valid_lists[linecount][0]
            inputlinenumber = input_valid_lists[linecount][1]
            firstword = line[0]

            if firstword == "var":  # variable declaration
                if len(line) == 2:
                    if bool(re.match(check_var_label_name, line[1])):
                        variables.append(line[1])
                    else:
                        errors[10][0] = True
                        errors[10][2].append(inputlinenumber)
                else:
                    errors[10][0] = True
                    errors[10][2].append(inputlinenumber)

            elif firstword[-1] == ":":  # label
                if bool(re.match(check_var_label_name, firstword[:-1])):
                    # labels.append([firstword[:-1], count])
                    line.pop(0)
                    ps_result, line_error = instruction_flow(line, instructions, errors, variables, labels, nonvarcount)
                    if line_error == -2:
                        result.append(ps_result)
                    else:
                        errors[line_error][2].append(inputlinenumber)
                    count += 1
                else:
                    errors[10][0] = True
                    errors[10][2].append(inputlinenumber)

            else:  # instructions
                ps_result1, line_error1 = instruction_flow(line, instructions, errors, variables, labels, nonvarcount)
                if line_error1 == -2:
                    result.append(ps_result1)
                else:
                    errors[line_error1][2].append(inputlinenumber)
                count += 1

            # print(errors)
            # print(count)
            # print(result)
            for err in errors:  # error gen
                if err[0]:
                    result = ["Error: line ", str(err[2][0]), " ", err[1]]
                    assert False
            linecount += 1

        print("\n".join(result))
    except AssertionError:
        print("".join(result))


main()
