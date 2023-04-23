import unittest
from cpu import Opcodes


def assemble(input_file, output_file, ram_size=16):
    print("Assembling...")

    variables = {}
    variable_addrs = []

    labels = {}
    label_refs = {}

    instructions = []

    with open(input_file, "r") as f:
        line_num = 0
        for line in f.readlines():
            line_num += 1
            line = line.strip().lower()

            if not line or line.startswith(";"):
                continue

            tokens = line.split()

            if tokens[0] == "def":
                if len(tokens) != 3:
                    raise SyntaxError("Invalid variable definition")
                if tokens[1] in variables:
                    raise SyntaxError("Variable already defined")
                variables[tokens[1]] = ram_size - 1 - len(variable_addrs)
                variable_addrs.append(int(tokens[2]))
                continue

            if tokens[0].endswith(":"):
                if len(tokens) != 1:
                    raise SyntaxError("Invalid label")
                if tokens[0][:-1] in labels:
                    raise SyntaxError("Label already defined")
                labels[tokens[0][:-1]] = len(instructions)
                # check if there are any instructions that reference this label
                if tokens[0][:-1] in label_refs:
                    for ref in label_refs[tokens[0][:-1]]:
                        instructions[ref] |= len(instructions)
                    del label_refs[tokens[0][:-1]]
                continue

            opcode = Opcodes[tokens[0].upper()].value
            arg = 0

            if len(tokens) == 2:
                if tokens[1].isdigit():
                    arg = int(tokens[1])
                elif tokens[1] in variables:
                    arg = variables[tokens[1]]
                elif tokens[1] in labels:
                    arg = labels[tokens[1]]
                else:
                    # record the instruction address that references the label
                    if tokens[1] not in label_refs:
                        label_refs[tokens[1]] = []
                    label_refs[tokens[1]].append(len(instructions))
                    # reserve a placeholder for the address
                    instructions.append(opcode << 4)
                    continue

            instructions.append(opcode << 4 | arg)

    # check if there are any labels that were referenced but not defined
    undefined_labels = set(label_refs.keys())
    if undefined_labels:
        raise SyntaxError("Undefined labels: %s" % ", ".join(undefined_labels))

    # Write the machine code to the output file
    with open(output_file, "wb") as f:
        # Convert the list of integers to bytes and write to the file
        f.write(bytes(instructions))

        # Fill the rest of the RAM with zeros
        for _ in range(ram_size - len(instructions) - len(variable_addrs)):
            f.write(bytes([0]))

        # Write the addresses of variables to the end of the file
        for addr in reversed(variable_addrs):
            f.write(bytes([addr]))

    print("Assembly complete.")


class TestAssembler(unittest.TestCase):
    def test_assemble(self):
        assemble("multiply.asm", "program.bin")
        with open("program.bin", "r") as f:
            program = [int(line, 16) for line in f.readlines()]
            self.assertEqual(
                program,
                [
                    0x1A,
                    0x40,
                    0x1F,
                    0x3D,
                    0x4F,
                    0x7A,
                    0x10,
                    0x2E,
                    0x40,
                    0x62,
                    0x10,
                    0xE0,
                    0xF0,
                    0x01,
                    0x05,
                    0x0A,
                ],
            )


if __name__ == "__main__":
    unittest.main()
