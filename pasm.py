import sys
import py2600

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
		if symbol != '\n':
			self.label_data.append(symbol)
		else:
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


class InitialState(State):
	def __init__(self, fsm):
		State.__init__(self, fsm)
		self.state_table['label'] = LabelDefState
		self.state_table['PUSH'] = PushState

	def update(self, symbol):
		next_state = None
		if symbol in self.state_table.keys():
			next_state = self.state_table[symbol]
		elif symbol != '':
			next_state = DataState
			self.fsm.change_state(next_state(self.fsm))


class PasmFSM:
	def __init(self, src):
		self.tape = src.replace('\n', ' \n ').split(' ')
		self.currentState = InitialState(self)

	def run(self):
		for symbol in self.tape:
			self.currentState.update(symbol)


class Assembler:
	def __init__(self, file_name):
		self.file_name = file_name

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
		with open(self.file_name.replace('.asm', '.rom'), 'wb') as rom_file:
   			rom_file.write(memoryview(bytecode).tobytes())


if __name__ == '__main__':
	if len(sys.argv) < 0:
		print 'Usage: pasm file_name'

	Assembler(sys.argv[1]).assemble()
