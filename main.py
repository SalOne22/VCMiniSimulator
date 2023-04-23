from enum import Enum


class Opcodes(Enum):
    NOP = 0
    LDA = 1
    ADD = 2
    SUB = 3
    STA = 4
    LDI = 5
    JMP = 6
    JZ = 7
    JC = 8
    OUT = 14
    HLT = 15


class CPU:
    def __init__(self) -> None:
        self.pc = 0

        self.regA = 0
        self.regB = 0
        self.MAR = 0
        self.IReg = 0
        self.flags = {"ZF": False, "CF": False}

        self.RAM = [0] * 16

        self.running = False

    def load(self, program):
        address = 0
        for instruction in program:
            self.RAM[address] = instruction
            address += 1

    def run(self):
        self.running = True
        while self.running:
            # Fetch
            self.MAR = self.pc
            if self.MAR >= len(self.RAM):
                self.pc = 0

            self.IReg = self.RAM[self.MAR]
            self.pc += 1

            # Decode
            op = self.IReg >> 4
            arg = self.IReg & 0x0F

            # Execute
            if op == Opcodes.NOP.value:
                continue
            elif op == Opcodes.LDA.value:
                self.MAR = arg
                self.regA = self.RAM[self.MAR]
            elif op == Opcodes.ADD.value:
                self.MAR = arg
                self.regB = self.RAM[self.MAR]
                self.regA = self.regA + self.regB
                if self.regA > 255:
                    self.flags["CF"] = True
                    self.regA = 0
                if self.regA == 0:
                    self.flags["ZF"] = True
            elif op == Opcodes.SUB.value:
                self.MAR = arg
                self.regB = self.RAM[self.MAR]
                self.regA = self.regA - self.regB
                if self.regA < 0:
                    self.flags["CF"] = True
                    self.regA = 0
                if self.regA == 0:
                    self.flags["ZF"] = True
            elif op == Opcodes.STA.value:
                self.MAR = arg
                self.RAM[self.MAR] = self.regA
            elif op == Opcodes.LDI.value:
                self.regA = arg
            elif op == Opcodes.JMP.value:
                self.pc = arg
            elif op == Opcodes.JZ.value:
                if self.flags["ZF"]:
                    self.pc = arg
            elif op == Opcodes.JC.value:
                if self.flags["CF"]:
                    self.pc = arg
            elif op == Opcodes.OUT.value:
                print(self.regA)
            elif op == Opcodes.HLT.value:
                self.running = False


def main():
    cpu = CPU()

    program = [
        # Multiply 2 and 3
        Opcodes.LDA.value << 4 | 14,
        Opcodes.STA.value << 4 | 0,
        Opcodes.LDA.value << 4 | 15,
        Opcodes.SUB.value << 4 | 13,
        Opcodes.STA.value << 4 | 15,
        Opcodes.JZ.value << 4 | 10,
        Opcodes.LDA.value << 4 | 0,
        Opcodes.ADD.value << 4 | 14,
        Opcodes.STA.value << 4 | 0,
        Opcodes.JMP.value << 4 | 2,
        Opcodes.LDA.value << 4 | 0,
        Opcodes.OUT.value << 4 | 0,
        Opcodes.HLT.value << 4 | 0,
        1,
        10,
        5,
    ]

    cpu.load(program)
    cpu.run()


if __name__ == "__main__":
    main()
