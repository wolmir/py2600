import sys
import py2600

END_OF_BLOCK = '#END_OF_BLOCK#'
PROGRAM_START = 0x00

class InvalidConstantError(Exception):
    def __init__(self, constant):
        Exception.__init__(self)
        print('Invalid constant: ' + constant)

class Tape:
    def __init__(self, initial_sequence):
        self.sequence = initial_sequence
        self.tape_head = 0
        self.tape_length = len(self.sequence)

    def __iter__(self):
        return self

    def __next__(self):
        if self.tape_head == len(self.sequence):
            raise StopIteration
        next_symbol = self.sequence[self.tape_head]
        if next_symbol == '\n':
            print('\\n')
        elif next_symbol == ' ':
            print('SPACE')
        elif next_symbol == '':
            print('EMPTY')
        else:
            print(next_symbol)
        self.tape_head += 1
        return next_symbol

    def insert(self, sequence):
        self.sequence = self.sequence[:self.tape_head] + sequence + self.sequence[self.tape_head:]


class State:
    def __init__(self, fsm):
        self.fsm = fsm
        self.state_table = {}


class LabelState(State):
    def __init__(self, label_name, fsm):
        State.__init__(self, fsm)
        self.label_name = label_name
        self.label_data = []

    def update(self, symbol):
        self.label_data.append(symbol)
        if symbol == END_OF_BLOCK:
            self.fsm.labeled[self.label_name] = self.label_data
            self.fsm.change_state(InitialState(self.fsm))


class LabelDefState(State):
    def __init__(self, fsm):
        State.__init__(self, fsm)
        self.label_name = ''

    def update(self, symbol):
        if symbol != '\n':
            self.label_name += symbol
        else:
            self.fsm.labeled[self.label_name] = []
            self.fsm.change_state(LabelState(self.label_name, self.fsm))


class PushState(State):
    def __init__(self, fsm):
        State.__init__(self, fsm)

    def update(self, symbol):
        if symbol != '':
            self.fsm.machine_code.append(py2600.PUSH)
            self.fsm.machine_code.append(int(symbol, 16))
            self.fsm.change_state(InitialState(self.fsm))


class CommentState(State):
    def __init__(self, fsm):
        State.__init__(self, fsm)

    def update(self, symbol):
        if (symbol == '\n'):
            self.fsm.change_state(InitialState(self.fsm))


class PushaState(State):
    def __init__(self, fsm):
        State.__init__(self, fsm)

    def update(self, symbol):
        if symbol != '':
            self.fsm.machine_code.append(py2600.PUSHA)
            try:
                value = int(symbol, 16)
                self.fsm.machine_code.append(value & 0x00FF)
                self.fsm.machine_code.append((value & 0xFF00) >> 8)
            except ValueError:
                addr = self.fsm.mark_for_resolution(symbol[1:-1])
            self.fsm.change_state(InitialState(self.fsm))


class InterruptState(State):
    def __init__(self, fsm):
        State.__init__(self, fsm)

    def update(self, symbol):
        if symbol != '':
            self.fsm.machine_code.append(py2600.INT)
            self.fsm.machine_code.append(int(symbol, 16))
            self.fsm.change_state(InitialState(self.fsm))


class DataState(State):
    def __init__(self, intial_symbol, fsm):
        State.__init__(self, fsm)
        self.fsm.machine_code.append(int(intial_symbol, 16))

    def update(self, symbol):
        if symbol != END_OF_BLOCK:
            try:
                if (symbol != '\n') and (symbol != ''):
                    data = int(symbol, 16)
                    self.fsm.machine_code.append(data)
            except ValueError:
                print('Invalid constant: ' + str(symbol))
                sys.exit()
        else:
            self.fsm.change_state(InitialState(self.fsm))

class BranchState(State):
    def __init__(self, branch_type, fsm):
        State.__init__(self, fsm)
        if branch_type == 'lt':
            self.fsm.machine_code.append(py2600.IFCMPLT)
        elif branch_type == 'eq':
            self.fsm.machine_code.append(py2600.IFCMPEQ)
        elif branch_type == 'jmp':
            self.fsm.machine_code.append(py2600.JMP)

    def update(self, symbol):
        if symbol != '':
            try:
                value = int(symbol, 16)
                self.fsm.machine_code.append(value & 0x00FF)
                self.fsm.machine_code.append((value & 0xFF00) >> 8)
            except ValueError:
                addr = self.fsm.mark_for_resolution(symbol[1:-1])
            self.fsm.change_state(InitialState(self.fsm))


class InitialState(State):
    def __init__(self, fsm):
        State.__init__(self, fsm)
        self.state_table['label'] = LabelDefState
        self.state_table['PUSH'] = PushState
        self.state_table['PUSHA'] = PushaState
        self.state_table['INT'] = InterruptState

    def update(self, symbol):
        next_state = None
        if symbol in self.state_table.keys():
            next_state = self.state_table[symbol]
            self.fsm.change_state(next_state(self.fsm))
        elif symbol == 'CPINC':
            self.fsm.machine_code.append(py2600.CPINC)
        elif symbol == 'CP':
            self.fsm.machine_code.append(py2600.CP)
        elif symbol == 'CPV':
            self.fsm.machine_code.append(py2600.CPV)
        elif symbol == 'CPINCV':
            self.fsm.machine_code.append(py2600.CPINCV)
        elif symbol == 'END':
            self.fsm.machine_code.append(py2600.END)
        elif symbol == 'STORE':
            self.fsm.machine_code.append(py2600.STORE)
        elif symbol == 'LOAD':
            self.fsm.machine_code.append(py2600.LOAD)
        elif symbol == 'INCM':
            self.fsm.machine_code.append(py2600.INCM)
        elif symbol == 'INCMIP':
            self.fsm.machine_code.append(py2600.INCMIP)
        elif symbol == 'IFCMPLT':
            self.fsm.change_state(BranchState('lt', self.fsm))
        elif symbol == 'IFCMPEQ':
            self.fsm.change_state(BranchState('eq', self.fsm))
        elif symbol == 'JMP':
            self.fsm.change_state(BranchState('jmp', self.fsm))
        elif symbol.startswith('['):
            self.fsm.resolve(symbol[1:-1])
        elif symbol.startswith(';'):
            self.fsm.change_state(CommentState(self.fsm))
        elif not symbol in ['', '\n', END_OF_BLOCK]:
            self.fsm.change_state(DataState(symbol, self.fsm))


class SymbolTable:
    def __init__(self):
        self.symbol_refs = []

    def get_refs_to(self, ref_name):
        return [x[1] for x in filter(lambda ref: ref[0] == ref_name, self.symbol_refs)]

    def mark(self, ref):
        self.symbol_refs.append(ref)


class PasmFSM:
    def __init__(self, src):
        self.addr_counter = PROGRAM_START
        self.currentState = InitialState(self)
        self.labeled = {}
        self.machine_code = bytearray()
        self.marked_symbols = SymbolTable()
        self.resolved_symbols = {}
        self.tape = Tape(PasmFSM.sanitize(src))

    def change_state(self, state):
        print('Change to: ' + state.__class__.__name__)
        self.currentState = state

    def getResults(self):
        return self.machine_code

    def mark_for_resolution(self, symbol):
        print('Marking for resolution: ' + symbol)
        if not self.resolve_for_position(symbol):
            self.marked_symbols.mark((symbol, len(self.machine_code) - 2))

    def resolve(self, ref_name):
        print("Resolving references to: " + ref_name)
        ref_values = self.labeled[ref_name]
        self.tape.insert(ref_values)
        symbol_addr = len(self.machine_code)
        self.resolved_symbols[ref_name] = (symbol_addr & 0x00FF, (symbol_addr & 0xFF00) >> 8)
        for addr in self.marked_symbols.get_refs_to(ref_name):
            print('\tAt addr: ' + str(addr))
            print('\t\tresolved to: ' + str(symbol_addr & 0x00FF) + ' ' + str((symbol_addr & 0xFF00) >> 8) + ' or ' + str(symbol_addr))
            self.machine_code[addr] = symbol_addr & 0x00FF
            self.machine_code[addr + 1] = (symbol_addr & 0xFF00) >> 8

    def resolve_for_position(self, symbol):
        if symbol in self.resolved_symbols.keys():
            addr_a = self.resolved_symbols[symbol][0]
            addr_b = self.resolved_symbols[symbol][1]
            print('\tAlready resolved to ' + str((addr_b << 8) | addr_a))
            self.machine_code.append(addr_a)
            self.machine_code.append(addr_b)
            return True
        self.machine_code.append(0x00)
        self.machine_code.append(0x00)
        return False

    def run(self):
        for symbol in self.tape:
            self.currentState.update(symbol)

    @staticmethod
    def sanitize(source_code):
        src = source_code.replace('\r\n', '\n')
        src = src.replace('\r', '\n')
        return src.replace('\n\n', '\n' + END_OF_BLOCK + ' ').replace('\n', ' \n ').split(' ')

class Assembler:
    def __init__(self, file_name):
        self.file_name = file_name
        if not self.file_name.endswith('.pasm'):
            raise Exception('Source files should always end with .pasm. Aborting.')

    def assemble(self):
        src = self.read_file()
        bytecode = self.build(src)
        self.write_rom(bytecode)

    def build(self, src):
        fsm = PasmFSM(src)
        fsm.run()
        return fsm.getResults()

    def read_file(self):
        src = None
        with open(self.file_name, 'r') as src_file:
            src = src_file.read().strip()
        return src

    def write_rom(self, bytecode):
        with open(self.file_name.replace('.pasm', '.rom'), 'wb') as rom_file:
            rom_file.write(memoryview(bytecode).tobytes())


if __name__ == '__main__':
    if len(sys.argv) < 0:
        print('Usage: pasm file_name')

    assembler = Assembler(sys.argv[1])
    assembler.assemble()
