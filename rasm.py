#!/usr/bin/python
# Revised Assembly

# Revised Assembly creates either 1 or 2 byte addresses (Called 32 and 64 bit for the sake of simplicity)
# 32-bit registries have a memory-width of 8 bytes, and
# 64-bit registries have a memory-width of 16 bytes.
from time import gmtime, strftime

end = -1
reg32len, reg64len, = 8, 16
reg32addr, reg64addr = 2**8, 2**16
# "32"-bit registries have a total storage space of 2 kB
# "64"-bit registries have a total storage space of 1 MB
reg32 = [[''] * reg32len] * reg32addr # Creates 256 8-byte memory blocks, or 2048 characters (Not addresses!)
reg64 = [[''] * reg64len] * reg64addr # Creates 65536 16-byte memory blocks, or 1048576 characters (Not addresses!)
tagDict = {}
activeReg = 0

def nfr(): # "Next free register"
	global activeReg
	for i, j in enumerate(reg32 if activeReg == 0 else reg64):
		if ''.join(j) == '': return i

def put(val, start, end, tag, recurse=False): # "put"
	val = list(val)
	global activeReg
	if activeReg == 0:
		if len(val) < reg32len:
			for i in range(0, reg32len - len(val)):
				val.append('')
			reg32[start] = val
			if not recurse and tag: tagDict.setdefault(tag, ''.join(val))
		elif len(val) > reg32len:
			if (end if end != -1 else reg32addr - 1) > start + 1:
				reg32[start] = val[:reg32len]
				if not recurse and tag: tagDict.setdefault(tag, ''.join(val))
				put("".join(val[reg32len:]), nfr(), end, tag, True)
			else:
				del val[reg32len:]
				reg32[start] = val
				if not recurse and tag: tagDict.setdefault(tag, ''.join(val))
		else:
			reg32[start] = val
			if not recurse and tag: tagDict.setdefault(tag, ''.join(val))
	else:
		if len(val) < reg64len:
			for i in range(0, reg64len - len(val)):
				val.append('')
			reg64[start] = val
			if not recurse and tag: tagDict.setdefault(tag, ''.join(val))
		elif len(val) > reg64len:
			if (end if end != -1 else reg64addr - 1) > start + 1:
				reg64[start] = val[:reg64len]
				if not recurse and tag: tagDict.setdefault(tag, ''.join(val))
				put("".join(val[reg64len:]), nfr(), end, tag, True)
			else:
				del val[reg64len:]
				reg64[start] = val
				if not recurse and tag: tagDict.setdefault(tag, ''.join(val))
		else:
			reg64[start] = val
			if not recurse and tag: tagDict.setdefault(tag, ''.join(val))

def chg(reg): # "change"
	global activeReg
	if reg == 0:
		activeReg = 0
	elif reg == 1:
		activeReg = 1

def clr(start, end): # "clear"
	global activeReg
	if activeReg == 0:
		for i in range(start, end if end != -1 else reg32addr):
			reg32[i] = [''] * reg32len
	else:
		for i in range(start, end if end != -1 else reg64addr):
			reg64[i] = [''] * reg64len

def dmp(file=None): # "dump"
	global activeReg
	if file:
		out = open(file, 'w')
		for i in (reg32 if activeReg == 0 else reg64):
			out.write(''.join(i) + "\n")
	else:
		for i in (reg32 if activeReg == 0 else reg64):
			print ''.join(i)
	clr(0, end)

def clo(): # "clone"
	for i, j in enumerate(reg32 if activeReg == 0 else reg64):
		if ''.join(j) != '': print hex(i) + "\t" + ''.join(j)
	print('...')
	print(hex(len(reg32) - 1) if activeReg == 0 else hex(len(reg64) - 1))

# Interpreter
while True:
	userIn = raw_input(">")
	userIn = userIn.split(" ")
	baseCommand = userIn[0]
	args = userIn[1:]
	if baseCommand == "chg":
		chg(int(args[0]))
	elif baseCommand == "put":
		put(" ".join(args[3:]), nfr() if args[0] == "nfr" else int(args[0]),\
		 	end if args[1] == "end" else int(args[1]), None if args[2] == "null" else args[2])
	elif baseCommand == "clo":
		clo()
	elif baseCommand == "clr":
		if len(args) == 0:
			clr(0, end)
		elif len(args) == 1:
			clr(int(args[0], 16), end) # Ewwww.
		elif len(args) == 2:
			clr(int(args[0], 16), int(args[1], 16))
	elif baseCommand == "dmp":
		dmp()
	elif baseCommand == "nfr":
		print(nfr())
	elif baseCommand == "_break":
		break

# Example

# Don't even try to store all of this in the 32-bit register. You *will* get errors.
# Meanwhile, it only takes up 0.24% of the 64-bit register.
chg(1)
put("0123456789ABCDEF", 0, end, None)
put("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent id turpis mi. Ut efficitur dui quis lorem convallis vulputate. Vivamus iaculis augue ac urna vulputate suscipit a ut turpis. Nunc facilisis quis velit quis cursus. Nunc ullamcorper sapien vitae libero tempus venenatis non non odio. Ut at arcu varius, condimentum massa luctus, dictum ante. Fusce metus enim, interdum ac tristique vitae, ultricies non diam. Proin augue quam, suscipit ac augue in, tristique hendrerit arcu. Cras non enim et dolor scelerisque porttitor ut molestie lacus. Etiam ultrices pulvinar metus ac maximus.", nfr(), end, "msg0")
put("Nunc ex arcu, vehicula nec nisi quis, bibendum suscipit urna. Vivamus nec sem vitae ex pharetra ultricies. Aenean elementum metus nunc, et malesuada mi tristique id. Ut suscipit et diam non eleifend. In hac habitasse platea dictumst. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Etiam eu sem vitae erat aliquam finibus ut vitae dolor. Phasellus imperdiet eu est in blandit. Suspendisse at erat consequat, dignissim enim at, blandit dolor. Ut lacinia orci eu nibh gravida, et lobortis purus fermentum. Donec lectus augue, tempus eget arcu quis, dictum malesuada nunc.", nfr(), end, "msg1")
put("Vestibulum at magna quis urna finibus efficitur. Nunc eu elementum sapien, sed lobortis metus. Quisque lacus nisl, auctor id arcu et, ullamcorper lacinia lacus. Phasellus consectetur augue lectus, eget feugiat nulla dapibus ut. Nam at arcu nec sapien ornare rutrum. Donec quis arcu fermentum, mattis enim quis, pharetra est. Suspendisse potenti. Curabitur ex metus, lobortis in elit ultricies, volutpat euismod nibh. Vivamus tristique turpis sed venenatis pellentesque. Phasellus nisi neque, interdum et enim eu, facilisis dignissim sem. In sem tortor, venenatis sed fringilla quis, aliquet sed nisl.", nfr(), end, "msg2")
put("Nam facilisis ante ornare dolor pretium euismod. Maecenas sed blandit diam. Proin ac maximus odio, quis luctus orci. Nunc bibendum libero neque, non vestibulum velit fringilla quis. Duis id felis condimentum lacus porttitor tempor. Suspendisse ac dolor turpis. Fusce ullamcorper pretium nisl, a gravida lacus condimentum sit amet. Morbi venenatis nec erat consequat ornare. Nam nulla tellus, tristique quis hendrerit non, eleifend sed dui. Vestibulum lorem augue, aliquam vel urna non, semper vehicula leo. Vivamus feugiat euismod urna, vel commodo libero tristique sed. Aenean ut eleifend elit, quis euismod purus.", nfr(), end, "msg3")
put("The time is: ", nfr(), end, "timePre")
put(strftime("%H:%M:%S"), nfr(), end, "time")
clo()

print(tagDict["msg0"] + "\n" +\
	tagDict["msg1"] + "\n" +\
	tagDict["msg2"] + "\n" +\
	tagDict["msg3"] + "\n" +\
	tagDict["timePre"] + tagDict["time"])
