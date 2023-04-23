from cpu import CPU, Opcodes
import argparse
from pprint import pprint


def main():
    cpu = CPU()
    parser = argparse.ArgumentParser(description="Emulate a VCMini 8-bit CPU")

    parser.add_argument(
        "program",
        metavar="program",
        type=str,
        nargs="?",
        help="the program to run in binary format",
    )

    parser.add_argument(
        "-a",
        "--assemble",
        metavar="input",
        # action="store_true",
        type=str,
        nargs="?",
        help="assemble the program from an assembly file",
    )

    parser.add_argument(
        "-o",
        "--output",
        metavar="output",
        type=str,
        nargs="?",
        help="the output file for the assembled program",
    )

    args = parser.parse_args()

    # program = [
    #     # Multiply 2 and 3
    #     Opcodes.LDA.value << 4 | 14,
    #     Opcodes.STA.value << 4 | 0,
    #     Opcodes.LDA.value << 4 | 15,
    #     Opcodes.SUB.value << 4 | 13,
    #     Opcodes.STA.value << 4 | 15,
    #     Opcodes.JZ.value << 4 | 10,
    #     Opcodes.LDA.value << 4 | 0,
    #     Opcodes.ADD.value << 4 | 14,
    #     Opcodes.STA.value << 4 | 0,
    #     Opcodes.JMP.value << 4 | 2,
    #     Opcodes.LDA.value << 4 | 0,
    #     Opcodes.OUT.value << 4 | 0,
    #     Opcodes.HLT.value << 4 | 0,
    #     1,
    #     10,
    #     5,
    # ]

    if args.assemble:
        from assembler import assemble

        if not args.output:
            args.output = args.assemble.replace(".asm", ".bin")

        assemble(args.assemble, args.output)

    if args.program:
        with open(args.program, "r") as f:
            program = [int(line, 16) for line in f.readlines()]

            cpu.load(program)
            cpu.run()


if __name__ == "__main__":
    main()
