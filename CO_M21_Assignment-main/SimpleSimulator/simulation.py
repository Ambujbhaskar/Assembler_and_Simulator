from Memory import Memory
from registerfile import registerfile
from executionengine import executionengine
from programcounter import programcounter
import matplotlib.pyplot as plt


def main():
    memory = Memory()
    registerFile = registerfile()
    executionEngine = executionengine(memory, registerFile)     # execution engine change memory and registerfile depending upon what ever instruction are given.
    PC = programcounter(0)
    halted = False
    cycle = 0
    PClst = []
    cyclelst = []
    while not halted:
        inst = memory.fetch(PC.getVal(), cycle)     # it will fetch the instruction depending upon fetching PC value.
        halted, nextPC = executionEngine.execute(inst, cycle, PC.PC)    # it will execute instruction and update the register_file.
        PClst.append(PC.getPCdec())        # for plot
        cyclelst.append(cycle+1)    # for plot
        pc_print = PC.dump()
        reg_print = registerFile.dump()
        print(pc_print + " " + reg_print)
        PC.update(nextPC)   # it might be +1 or not, depending upon jump instruction used or not.
        cycle += 1

    memory.dump()
    plt.scatter(cyclelst, PClst)
    plt.show()
    plt.savefig("plot.png")
    # memory.showTraces()  # at what cycle we are using what memory location


if __name__ == '__main__':
    main()
