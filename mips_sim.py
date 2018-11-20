print("Welcome to ECE366 MIPS_sim")

def op(_hex, dataMem, array, pc, multicycleCount, Hazards, _prev, _next):
    print("\n")
    print("Result of run:", "\n")
    binaryNum = hex_bin(_hex)

    # ADD: multicycle = 4
    if binaryNum[21:32] == "00000100000" and binaryNum[0:6] == "000000":
        
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        rd = int(binaryNum[16:21], 2)

        print("ADD $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
 
        array[rd] = array[rs] + array[rt]

        multicycleCount[1] = multicycleCount[1] + 1
   
    # SUB: multicycle = 4
    elif binaryNum[21:32] == "00000100010" and binaryNum[0:6] == "000000":

        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        rd = int(binaryNum[16:21], 2)

        print("SUB $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        
        array[rd] = array[rs] - array[rt]

        multicycleCount[1] = multicycleCount[1] + 1
    
    # XOR: multicycle = 4
    elif binaryNum[26:32] == "100110" and binaryNum[0:6] == "000000":

        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        rd = int(binaryNum[16:21], 2)

        print("XOR $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
     
        array[rd] = array[rt] ^ array[rs]

        multicycleCount[1] = multicycleCount[1] + 1
      

    # ADDI: multicycle = 4
    elif binaryNum[0:6] == "001000":

        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        imm = binaryNum[16:32]

        _imm = bin_dec(imm)
        print("ADDI $" + str(rt) + ", $" + str(rs) + ", " + str(_imm))
        
        array[rt] = array[rs] + _imm

        multicycleCount[1] = multicycleCount[1] + 1
     

    # BEQ: multicycle = 3
    # requires a stall;
    # flushes next instruction
    
    elif binaryNum[0:6] == "000100":
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        imm = binaryNum[16:32]

        _imm = bin_dec(imm)
        print("BEQ $" + str(rs) + ", $" + str(rt) + ", " + str(_imm))
        
        if array[rt] == array[rs]:
            pc = pc + (4 * _imm)

            Hazards[1] = Hazards[1] + 1

        multicycleCount[0] = multicycleCount[0] + 1


        dataReg = instr(_prev)
        targetReg = dataReg[1]

        if targetReg == rs or targetReg == rt: 
            Hazards[0] = Hazards[0] + 1 
            
    # BNE: multicycle = 3
    # requires a stall
    # flushes next instruction
    
    elif binaryNum[0:6] == "000101":

        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        imm = binaryNum[16:32]

        _imm = bin_dec(imm)
        print("BNE $" + str(rt) + ", $" + str(rs) + ", " + str(_imm))
        
        if array[rt] != array[rs]:
            pc = pc + (4 * _imm)

            Hazards[1] = Hazards[1] + 1

        multicycleCount[0] = multicycleCount[0] + 1

        dataReg = instr(_prev)
        targetReg = dataReg[1]

        if targetReg == rs or targetReg == rt:
            Hazards[0] = Hazards[0] + 1

    # SLT: multicycle = 4
    
    elif binaryNum[21:32] == "00000101010" and binaryNum[0:6] == "000000":

        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        rd = int(binaryNum[16:21], 2)

        print("SLT $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        
        if array[rs] < array[rt]:
            array[rd] = 1
        else:
            array[rd] = 0

        multicycleCount[1] = multicycleCount[1] + 1

    # LW: multicycle = 5 "longest cycles required here"
    # requires a delay
    
    elif binaryNum[0:6] == "100011":
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        imm = binaryNum[16:32]

        _imm = bin_dec(imm)
        print("LW $" + str(rt) + ", " + str(_imm) + "($" + str(rs) + ")")
        
        dataMem_index = int((array[rs] - 0x2000 + _imm) / 4)
        dataMem_value = dataMem[dataMem_index]

        array[rt] = dataMem_value

        multicycleCount[2] = multicycleCount[2] + 1

        dataReg = instr(_next)
        sourceReg = dataReg[0]

        for i in range(0, len(sourceReg)):
            cur_sourceReg = sourceReg[i]

            if cur_sourceReg == rt:
                Hazards[0] = Hazards[0] + 1

    # SW: multicycle = 4
    
    elif binaryNum[0:6] == "101011":
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        imm = binaryNum[16:32]

        _imm = bin_dec(imm)
        print("SW $" + str(rt) + ", " + str(_imm) + "($" + str(rs) + ")")
        
        dataMem_index = int((array[rs] - 0x2000 + _imm) / 4)
        dataMem[dataMem_index] = array[rt]

        multicycleCount[1] = multicycleCount[1] + 1
    pc = pc + 4

    return [dataMem, array, pc, multicycleCount, Hazards]


def bin_dec(binaryNum):
    if binaryNum[0] == "1":
        number = int(binaryNum, 2)
        _bin = 0b1111111111111111
        decimal = _bin - number + 1
        return 0 - decimal
    else:
        decimal = int(binaryNum, 2)
        return decimal    

def hex_bin(hexNum):
    return str(bin(int(hexNum, 16))[2:].zfill(32))

def file_array(file):
    newArray = []
    for line in file:
        newArray.append(line[0:10].rstrip())
    return newArray

def output(array, pc):
    print("PC: ", pc)
    for i in range(1, 8):
        print("$" + str(i) + ": ", array[i])

def instr(_hex):
    binaryNum = hex_bin(_hex)
    rs = 0
    rt = 0
    rd = 0
    sourceReg = []
    targetReg = 0
    if binaryNum[0:6] == "000000": #R-type
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        rd = int(binaryNum[16:21], 2)
        sourceReg = [rt, rs]
        targetReg = rd
        print("*** $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
    elif binaryNum[0:6] == "000100" or binaryNum[0:6] == "000101": #branch
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        sourceReg = [rt, rs]
    elif binaryNum[0:6] == "001000": #addi
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        targetReg = rt
        sourceReg = [rs]
    elif binaryNum[0:6] == "100011": #lw
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        targetReg = rt
        sourceReg = [rs]
    elif binaryNum[0:6] == "101011": #sw
        rs = int(binaryNum[6:11], 2)
        rt = int(binaryNum[11:16], 2)
        sourceReg = [rt, rs]
    return [sourceReg, targetReg]


def simulator(fileName):

    file = open(fileName, "r")
    instrMem = file_array(file)
    dataMem = [0] * 1023  
    array = [0, 0, 0, 0, 0, 0, 0, 0]  
    i = 0
    pc = 0
    multicycleCount = [0, 0, 0]    
    instrCount = 0     
    Hazards = [0, 0]
    _hex = instrMem[pc]
    _prev = "0xffffffff"
    _next = "0xffffffff"

    
    while _hex != "0x1000FFFF" or _hex != "0x1000ffff":
        if _hex == "0x1000ffff":
            instrCount = instrCount + 1
            multicycleCount[0] = multicycleCount[0] + 1
            break
    
        if i == 0:
            _prev = "0xffffffff"
            _next = instrMem[i + 1]
            
        elif i == (len(instrMem) - 2):
            _prev = instrMem[i - 1]
            _next = "0xffffffff"

        else:
            _prev = instrMem[i - 1]
            _next = instrMem[i + 1]
            
        x = op(_hex, dataMem, array, pc, multicycleCount, Hazards, _prev, _next)
        dataMem = x[0]
        array = x[1]
        pc = x[2]
        multicycleCount = x[3]
        Hazards = x[4]
    
        output(array, pc)
        print("Data Memory:", dataMem[0:10])
        i = int(pc / 4)
        _hex = instrMem[i]
        
        instrCount = instrCount + 1
        
    dataHazard = Hazards[0]
    ctrlHazard = Hazards[1]
    pipelineCount = instrCount + 4 + dataHazard + ctrlHazard

    Count_3_cycle_instr = multicycleCount[0]
    Count_4_cycle_instr = multicycleCount[1]
    Count_5_cycle_instr = multicycleCount[2]
    
    multicycle = (Count_3_cycle_instr * 3) + (Count_4_cycle_instr * 4) + (Count_5_cycle_instr * 5)

    
    
    print("Dynamic Instruction Count = ", instrCount, "\n")
    print("Cycle number details:")
    print("\n")
    print("a. Multi-cycle MIPS CPU:")
    print("Num of 3 Cycle Instructions = ", Count_3_cycle_instr)
    print("Num of 4 Cycle Instructions = ", Count_4_cycle_instr)
    print("Num of 5 Cycle Instructions = ", Count_5_cycle_instr)
    print("Total Number of Cycles      = ", multicycle)
    print("\n")
    print("b. Pipelined MIPS CPU:")
    print("Num of Data Hazard     =", dataHazard)
    print("Num of Ctrl Hazard     =", ctrlHazard)
    print("Total Number of Cycles =", pipelineCount)
    print("\n")

#simulator("i_mem.txt")
#print("The above results are for i_mem")
#simulator("A1.txt")
#print("The above results are for A1")
#simulator("A2.txt")
#print("The above results are for  A2")
#simulator("B1.txt")
#print("The above results are for  B1")
simulator("B2.txt")
print("The above results are for  B2")

 
