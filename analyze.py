
""" 
Analyzer of if-conditions 
Set directory as path to analysing project
Set stat_file, module_file, call_file, log_file as pathes for result
	Module file - list of analysed and error modules
	Call file - list of functions, calling in if-constructions
	Log file - contains path to a module with unknown if-construction and ast of its node
	Stat file - common statistics of project with basic counters and grouping:
		Total lines - lines of analyzed code
		Total if - number of if-nodes
		Total cond - number of subconditions in all if-nodes (Ex. "if (a > 10) and not foo(b):" - total if = 1; total = 4)
		Next are counters with basic infomation about conditions (Ex. single condition is "if a:", single not is "if not a:" or "if (b > c) and (not a):")
		Next are grouping by different ways: work with kinds of information (Integer, String, Type, Object, Collection) and work comparison with None-Bool values
"""

#---------------------------------------------------------------------------------------------------------------------------------
import ast
import sys
import os
import math
import cmath
import random
from datetime import datetime

start = datetime.now()

directory     = "/home/user/My_project"               # folder with analysing project     
stat_file     = "/home/user/Documents/Statistics.csv"	# file with if-statistics
module_file   = "/home/user/Documents/Modules.txt"	  # file with list of analysed modules
call_file     = "/home/user/Documents/Calls.csv"	  	# file with list of functions
log_file      = "/home/user/Documents/log.txt"     	  # file with information about unknown if-nodes

directory_lib = "/usr/lib/python2.7"  # directory with standart modules
#---------------------------------------------------------------------------------------------------------------------------------

class Stat:              # statistics class, contains counters and cashes
	total_line     = 0
	total_if       = 0
	total          = 0   
	
	compare        = 0
	compare_eq     = 0
	compare_noteq  = 0
	compare_gt     = 0
	compare_lt     = 0
	compare_gte    = 0
	compare_lte    = 0
	compare_is     = 0
	compare_in     = 0
	compare_notin  = 0
	compare_isnot  = 0
	
	call           = 0
	
	binop          = 0
	binop_add      = 0
	binop_sub      = 0
	binop_div      = 0
	binop_floordiv = 0
	binop_mod      = 0
	binop_rshift   = 0
	binop_lshift   = 0
	binop_bitor    = 0
	binop_bitand   = 0
	binop_mult     = 0
	binop_pow      = 0
	
	unop           = 0
	unop_uadd      = 0
	unop_usub      = 0
	unop_invert    = 0
	unop_not       = 0
	single_not     = 0
	
	boolop         = 0
	boolop_and     = 0
	boolop_or      = 0

	single_cond    = 0   # total single conditions (ex: "if a:")
	single_name    = 0   # "if a:"
	single_variable= 0   # unknow variable
	single_subscript=0   # index
	single_attribute=0   # attribute name
	single_num     = 0   # "if 1:"
	single_str     = 0   # "if 'a':"
	single_collect = 0
	 
	genexp         = 0
	listcomp       = 0
	setcomp        = 0
	lambda_condition=0
	ifexp          = 0
		
	unknown_condition= 0  
	
	num_condition  = 0  # conditions with numbers
	str_condition  = 0  # conditions with strings
	collection     = 0  # conditions with collections
	set_condition  = 0
	tuple_condition= 0
	dict_condition = 0
	list_condition = 0
	sub_condition  = 0  # operation with element of collection throw index (subscript)
	attribute_condition = 0
	
	none           = 0  # comparisions with none and bool
	none_eq        = 0
	none_noteq     = 0
	bool_eq        = 0
	bool_noteq     = 0
	none_is        = 0
	none_isnot     = 0
	bool_is        = 0
	bool_isnot     = 0
	none_other     = 0
	
	group_type     = 0   # grouping conditions
	group_string   = 0
	group_collection=0
	group_object   = 0
	group_integer  = 0
	
	
	nesting_flag   = 0	# flag to detect a single name condition, should be reset before calling outside the determine()
	not_flag       = 0  # flag to detect a single not condition (if not a:)
	
	func_cash = {}	    # dictionary of call statistics
	dir_files = []      # list of .py-files with path in all directories of current project path
	dir_filenames = []  # list of names .py files in project directory
	import_cash = []    # list of names standard modules, that have been analysed
	import_error = []   # list of names module that haven't been analysed
	lib_files = []      # list with all directories usr/lib/python2.7
	
	call_str = {}       # dictionaries for grouping functions
	call_int = {}
	call_collection = {}
	call_type = {}
	call_object = {}
	list_func_type = ['isinstance','type','istype', 'get_type']  # hard coded type-functions
	list_func_object = ['hasattr','getattr', '_hasattr', 'get_attribute']  # hard coded object-functions
	list_func_int = ['_isinfinity']
	
	debug = ""   # get log-file information


#---------------------------------------------------------------------------------------------------------------------------------
	
class Analyse(ast.NodeVisitor):   # class to analyse AST

	def determine(self, node):    # function determines kind of condition IF and change counters in Stat
		
		if isinstance(node, ast.Compare):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			Stat.compare += 1
			Stat.total += 1
			
			if isinstance(node.comparators[0], ast.Name):  # comparision with none-value
				if node.comparators[0].id == 'None':
					Stat.none += 1
					if isinstance(node.ops[0], ast.Eq):
						Stat.none_eq += 1
					elif isinstance(node.ops[0], ast.Is):
						Stat.none_is += 1
					elif isinstance(node.ops[0], ast.IsNot):
						Stat.none_isnot += 1
					elif isinstance(node.ops[0], ast.NotEq):
						Stat.none_noteq += 1
					else:
						Stat.none_other += 1
				if (node.comparators[0].id == 'False') or (node.comparators[0].id == 'True'):  # bool comparision
					Stat.none += 1
					if isinstance(node.ops[0], ast.Eq):
						Stat.bool_eq += 1
					elif isinstance(node.ops[0], ast.Is):
						Stat.bool_is += 1
					elif isinstance(node.ops[0], ast.IsNot):
						Stat.bool_isnot += 1
					elif isinstance(node.ops[0], ast.NotEq):
						Stat.bool_noteq += 1
					else:
						Stat.none_other += 1	
			if isinstance(node.ops[0], ast.Eq):     # ==
				Stat.compare_eq += 1
			if isinstance(node.ops[0], ast.NotEq):  # !=
				Stat.compare_noteq += 1
			if isinstance(node.ops[0], ast.Lt):     # <
				Stat.compare_lt += 1
			if isinstance(node.ops[0], ast.Gt):     # >
				Stat.compare_gt += 1	
			if isinstance(node.ops[0], ast.LtE):    # <=
				Stat.compare_lte += 1
			if isinstance(node.ops[0], ast.GtE):    # >=
				Stat.compare_gte += 1
			if isinstance(node.ops[0], ast.In):     # in
				Stat.compare_in += 1
			if isinstance(node.ops[0], ast.NotIn):  # not in
				Stat.compare_notin += 1	
			if isinstance(node.ops[0], ast.Is):     # is
				Stat.compare_is += 1
			if isinstance(node.ops[0], ast.IsNot):  # is not
				Stat.compare_isnot += 1
			self.determine(node.left)				# recoursive parsing expression
			for stmt in node.comparators:           
				self.determine(stmt)
					
		elif isinstance(node, ast.Call):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			if isinstance(node.func, ast.Name):	        # "if func(param):"
				if node.func.id not in Stat.func_cash:
					Stat.func_cash[node.func.id] = 1
					Stat.call += 1
					Stat.total += 1
				else:
					Stat.func_cash[node.func.id] += 1
					Stat.call += 1
					Stat.total += 1
			if isinstance(node.func, ast.Attribute):	# "if module.func(param):"
				if node.func.attr not in Stat.func_cash:
					Stat.func_cash[node.func.attr] = 1
					Stat.call += 1
					Stat.total += 1
				else:
					Stat.func_cash[node.func.attr] += 1
					Stat.call += 1
					Stat.total += 1
			for stmt in node.args:           		# recoursive parsing expression
				self.determine(stmt)
			
		elif isinstance(node, ast.BinOp):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			Stat.binop += 1
			Stat.total += 1
			if isinstance(node.op, ast.Add):        # +
				Stat.binop_add += 1
			if isinstance(node.op, ast.Sub):        # -
				Stat.binop_sub += 1
			if isinstance(node.op, ast.Div):        # /
				Stat.binop_div += 1
			if isinstance(node.op, ast.Mod):        # %
				Stat.binop_floordiv += 1
			if isinstance(node.op, ast.RShift):     # >>
				Stat.binop_rshift += 1
			if isinstance(node.op, ast.LShift):     # <<
				Stat.binop_lshift += 1
			if isinstance(node.op, ast.BitOr):      # &
				Stat.binop_bitor += 1
			if isinstance(node.op, ast.BitAnd):     # |
				Stat.binop_bitand += 1
			if isinstance(node.op, ast.FloorDiv):   # //
				Stat.binop_floordiv += 1
			if isinstance(node.op, ast.Mult):       # *
				Stat.binop_mult += 1
			if isinstance(node.op, ast.Pow):        # **
				Stat.binop_pow += 1
			self.determine(node.left)				# recoursive parsing expression
			self.determine(node.right)
				
		elif isinstance(node, ast.UnaryOp):
			Stat.not_flag = 0
			Stat.unop  += 1
			Stat.total += 1
			if isinstance(node.op, ast.UAdd):       # +
				Stat.unop_uadd += 1
			if isinstance(node.op, ast.USub):       # -
				Stat.unop_usub += 1
			if isinstance(node.op, ast.Invert):     # ~
				Stat.unop_invert += 1
			if isinstance(node.op, ast.Not):        # not
				Stat.unop_not += 1
				Stat.not_flag = 1
			Stat.nesting_flag += 1
			self.determine(node.operand)			# recoursive parsing expression
				
		elif ((isinstance(node, ast.Name)) or (isinstance(node, ast.Num)) or (isinstance(node, ast.Str)) or \
(isinstance(node, ast.List)) or (isinstance(node, ast.Set)) or (isinstance(node, ast.Tuple)) or \
(isinstance(node, ast.Dict)) or (isinstance(node, ast.Subscript)) or (isinstance(node, ast.Attribute))):
			if isinstance(node, ast.Name):
				if Stat.nesting_flag == 0:
					Stat.total += 1
					Stat.single_cond += 1
					Stat.single_name += 1
					Stat.single_variable += 1
				if (Stat.not_flag == 1) and (Stat.nesting_flag != 0):
					Stat.single_not += 1
					Stat.not_flag = 0
			if isinstance(node, ast.Subscript):
				if Stat.nesting_flag == 0:
					Stat.total += 1
					Stat.single_cond += 1
					Stat.single_name += 1
					Stat.single_subscript += 1
				Stat.collection += 1  # work with collection
				Stat.sub_condition += 1
				if (Stat.not_flag == 1) and (Stat.nesting_flag != 0):
					Stat.single_not += 1
					Stat.not_flag = 0
			if isinstance(node, ast.Attribute):
				if Stat.nesting_flag == 0:
					Stat.total += 1
					Stat.single_cond += 1
					Stat.single_name += 1
					Stat.single_attribute += 1
				Stat.attribute_condition += 1
				if (Stat.not_flag == 1) and (Stat.nesting_flag != 0):
					Stat.single_not += 1
					Stat.not_flag = 0
			if isinstance(node, ast.Num):
				if Stat.nesting_flag == 0:
					Stat.single_cond += 1
					Stat.single_num += 1
					Stat.total += 1
				Stat.num_condition += 1					
			if isinstance(node, ast.Str):
				if Stat.nesting_flag == 0:
					Stat.single_cond += 1
					Stat.single_str += 1
					Stat.total += 1
				Stat.str_condition += 1	
			if isinstance(node, ast.Set):
				if Stat.nesting_flag == 0:
					Stat.single_cond += 1
					Stat.single_collect += 1
					Stat.total += 1
				Stat.collection += 1
				Stat.set_condition += 1	
			if isinstance(node, ast.List):
				if Stat.nesting_flag == 0:
					Stat.single_cond += 1
					Stat.single_collect += 1
					Stat.total += 1
				Stat.collection += 1
				Stat.list_condition += 1	
			if isinstance(node, ast.Dict):
				if Stat.nesting_flag == 0:
					Stat.single_cond += 1
					Stat.single_collect += 1
					Stat.total += 1
				Stat.collection += 1
				Stat.dict_condition += 1	
			if isinstance(node, ast.Tuple):
				if Stat.nesting_flag == 0:
					Stat.single_cond += 1
					Stat.single_collect += 1
					Stat.total += 1
				Stat.collection += 1
				Stat.tuple_condition += 1	
							
		elif isinstance(node, ast.BoolOp):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			Stat.boolop += 1
			Stat.total += 1
			if isinstance(node.op, ast.And):   # and
				Stat.boolop_and += 1
			if isinstance(node.op, ast.Or):    # or
				Stat.boolop_or += 1
			for stmt in node.values:           # recoursive parsing expression
				self.determine(stmt)
				
		elif isinstance(node, ast.GeneratorExp):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			Stat.total += 1
			Stat.genexp += 1
			next_node = node.elt      # recoursive parsing expression
			self.determine(next_node)
			
		elif isinstance(node, ast.ListComp):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			Stat.total += 1
			Stat.listcomp +=1
			self.determine(node.elt)
			
		elif isinstance(node, ast.SetComp):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			Stat.total += 1
			Stat.setcomp +=1
			self.determine(node.elt)
			
		elif isinstance(node, ast.Lambda):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			Stat.total += 1
			Stat.lambda_condition += 1
			self.determine(node.body)
			
		elif isinstance(node, ast.IfExp):
			Stat.not_flag = 0
			Stat.nesting_flag += 1
			Stat.total += 1
			Stat.ifexp +=1
			self.determine(node.test)
			self.determine(node.body)
			
		else:
			Stat.total += 1                    
			Stat.unknown_condition += 1           
			debug_log.write(ast.dump(node) + "\n")
			debug_log.write(Stat.debug + "\n\n\n\n\n")
			
			
			
#---------------------------------------------------------------------------------------------------------------------------------
			
	def visit_If(self, node):      # call determine method with test node 
		test = node.test
		Stat.nesting_flag = 0      # reset flag to distinguish single conditions from complex
		Stat.total_if += 1
		self.determine(test)
		self.generic_visit(node)   # walking all child nodes
		
#---------------------------------------------------------------------------------------------------------------------------------

	def visit_Import(self, node):  # only modules not from project directory
		try:
			if node.names[0].name != None:   #if None-imported package in the project directory, and it will be analysed later
				flag = 0   # flag to detect missed modules: 1-module missed, 2-module imported, 0-module in cash or in project dir
				filename = node.names[0].name
				if filename.find(".") != -1:   # if it is package import search module name after last point
					filename = filename[filename.rfind(".")+1:] + ".py"
				else:
					filename += ".py"
				if ((filename not in Stat.dir_filenames) and (filename not in Stat.import_cash)):	
					flag = 1
					for path in Stat.lib_files:  # walking all directories with standart modules
						if path != sys.path[0]:      # except a directory with analyse.py
							filepath = path + "/" + filename
							if os.path.isfile(filepath):
								flag = 2
								if filename not in Stat.import_cash:
									Stat.import_cash.append(filename)
									for line in open(filepath, 'r'):
										if not line.isspace():
											Stat.total_line += 1
								new_ast = ast.parse(open(filepath).read())
								Stat.debug = filepath
								Analyse().visit(new_ast)
				if flag == 1:
					if filename not in Stat.import_error:
						Stat.import_error.append(filename)
		except Exception:
			print "visit_Import ERROR" 
			if filename not in Stat.import_error:
				Stat.import_error.append(filename)
			
		
			
	def visit_ImportFrom(self, node):  # only standard modules
		try:
			if node.module != None: #if None-imported module in the project directory, and it will be analysed later
				flag = 0  # flag to detect missed modules: 1-module missed, 2-module imported, 0-module in cash or in project dir
				filename = node.module
				if filename.find(".") != -1: # if it is package import search module name after last point
					filename = filename[filename.rfind(".")+1:] + ".py"
				else:
					filename += ".py"
				if ((filename not in Stat.dir_filenames) and (filename not in Stat.import_cash)):	
					flag = 1
					for path in Stat.lib_files:  # walking all directories with standart modules
						if path != sys.path[0]:      # besides a directory with analyse.py
							filepath = path + "/" + filename
							if os.path.isfile(filepath):
								flag = 2
								if filename not in Stat.import_cash:
									Stat.import_cash.append(filename)
									for line in open(filepath, 'r'):
										if not line.isspace():
											Stat.total_line += 1
								new_ast = ast.parse(open(filepath).read())
								Stat.debug = filepath
								Analyse().visit(new_ast)
				if flag == 1:
					if filename not in Stat.import_error:
						Stat.import_error.append(filename) 
		except Exception:
			print "visit_ImportFrom ERROR" 
			if filename not in Stat.import_error_module:
				Stat.import_error.append(filename)
						
#----------------------------------------------------------------------------------------------------------------------

for root, dirs, files in os.walk(directory):   # walking all directories in current catalog
	for name in files:
		if name[-3:] == ".py":
			Stat.dir_files.append(os.path.join(root, name))   # list of all .py files in project directory
			Stat.dir_filenames.append(name)					  # list of names of all .py files in project directory 

for root, dirs, files in os.walk(directory_lib):   #full python 2.7 catalog
	for name in files:    
		if root not in Stat.lib_files:
			Stat.lib_files.append(root)

for item in sys.path:                     # join sys.path and lib_files
	if item not in Stat.lib_files:
		Stat.lib_files.append(item)
		
debug_log = open(log_file, 'w')           # log with other if-conditions	
for item in Stat.dir_files:               # main loop, rounds dir_files
	try:
		for line in open(item, 'r'):      # count lines of code
			if not line.isspace():        # make sure that line is not empty
				Stat.total_line += 1
		my_ast = ast.parse(open(item).read())
		#print ast.dump(my_ast)
		Stat.nesting_flag = 0
		Stat.debug = item
		Analyse().visit(my_ast)
	except Exception:
		print "main ERROR" + item
		Stat.import_error.append(os.path.basename(item) + "     PROJECT FILE")
		Stat.dir_files.remove(item)
		Stat.dir_filenames.remove(os.path.basename(item))
debug_log.close()

## Output 
i = 0
symbol1 = "*"
symbol2 = "+"
while i < 30:
	symbol1 += "*"
	if i < 19:
		symbol2 += "+"
	i += 1

## Output call file
calls_file = open(call_file, 'w')
call_list = list(Stat.func_cash.items())  
call_list.sort(key = lambda item: item[1], reverse = True) 
for item in call_list:
	if ((item[0] in str.__dict__) or ("__"+item[0]+"__" in str.__dict__)) and (item[0] != 'len'):
		Stat.call_str[item[0]] = item[1]
	elif item[0] in (int.__dict__) or ("__"+item[0]+"__" in (int.__dict__)) or (item[0] in dir(math)) or ("__"+item[0]+"__" in dir(math)) or (item[0] in dir(random)) or (item[0] in dir(cmath)) or item[0] in Stat.list_func_int:
		Stat.call_int[item[0]] = item[1]
	elif item[0] in (list.__dict__) or item[0] in (set.__dict__) or item[0] in (tuple.__dict__) or item[0] in (dict.__dict__) or\
	"__"+item[0]+"__" in (list.__dict__) or "__"+item[0]+"__" in (set.__dict__) or "__"+item[0]+"__" in (tuple.__dict__) or\
	"__"+item[0]+"__" in (dict.__dict__):
		Stat.call_collection[item[0]] = item[1]
	elif item[0] in Stat.list_func_type:
		Stat.call_type[item[0]] = item[1]
	elif item[0] in Stat.list_func_object:
		Stat.call_object[item[0]] = item[1]
calls_file.write(symbol2+ "\n" + "Call string: " + str(int(math.fsum(Stat.call_str.values())))+\
"\n"+symbol2+ "\n" + "Call int: " + str(int(math.fsum(Stat.call_int.values())))+\
"\n"+symbol2+ "\n" + "Call collection: " + str(int(math.fsum(Stat.call_collection.values())))+\
"\n"+symbol2+ "\n" + "Call type: " + str(int(math.fsum(Stat.call_type.values())))+\
"\n"+symbol2+ "\n" + "Call object: " + str(int(math.fsum(Stat.call_object.values()))))	
calls_file.write("\n\n\n")	
for item in call_list:
	calls_file.write(item[0] + ":" + str(item[1]) + '\n')
calls_file.close()

## Output statistics file 

Stat.group_integer = Stat.num_condition + Stat.binop_sub + Stat.binop_pow + Stat.binop_div + Stat.binop_floordiv \
+ Stat.binop_mod + Stat.binop_bitor + Stat.binop_bitand + Stat.binop_lshift + Stat.binop_rshift \
+ Stat.unop_uadd + Stat.unop_usub + Stat.unop_invert+ int(math.fsum(Stat.call_int.values()))
Stat.group_type = Stat.none_eq + Stat.none_noteq + Stat.none_is + Stat.none_isnot + int(math.fsum(Stat.call_type.values()))
Stat.group_collection = Stat.collection + Stat.compare_in + Stat.compare_notin + Stat.listcomp + Stat.setcomp + int(math.fsum(Stat.call_collection.values()))
Stat.group_string = Stat.str_condition + int(math.fsum(Stat.call_str.values()))
Stat.group_object = Stat.attribute_condition + int(math.fsum(Stat.call_object.values()))

statistics = open(stat_file, 'w')
title = os.path.basename(directory)
statistics.write(title + "\n\n" + symbol2 + \
"\nTotal lines:  " + str(Stat.total_line) + \
"\nTotal if:     "    + str(Stat.total_if) + \
"\n" + symbol2 + \
"\nTotal:        " + str(Stat.total) + \
"\n" + symbol1 + \
"\nCompare:     "+ str(Stat.compare)+\
"\n  ==:        "+ str(Stat.compare_eq)+\
"\n  !=:        "+ str(Stat.compare_noteq)+\
"\n   >:        "+ str(Stat.compare_gt)+\
"\n   <:        "+ str(Stat.compare_lt)+\
"\n  >=:        "+ str(Stat.compare_gte)+\
"\n  <=:        "+ str(Stat.compare_lte)+\
"\n  is:        "+ str(Stat.compare_is)+\
"\n  in:        "+ str(Stat.compare_in)+\
"\nNot In:      "+ str(Stat.compare_notin)+\
"\nIs Not:      "+ str(Stat.compare_isnot)+\
"\n"+ symbol1 +\
"\nCall:        " + str(Stat.call) +\
"\n"+ symbol1+\
"\nBinOp:       "+ str(Stat.binop) +\
"\n   +:        "+ str(Stat.binop_add)+\
"\n   -:        "+ str(Stat.binop_sub)+\
"\n   *:        "+ str(Stat.binop_mult)+\
"\n  **:        "+ str(Stat.binop_pow)+\
"\n   /:        "+ str(Stat.binop_div)+\
"\n  //:        "+ str(Stat.binop_floordiv)+\
"\n   %:        "+ str(Stat.binop_mod)+\
"\n   &:        "+ str(Stat.binop_bitor)+\
"\n   |:        "+ str(Stat.binop_bitand)+\
"\n  <<:        "+ str(Stat.binop_lshift)+\
"\n  >>:        "+ str(Stat.binop_rshift)+\
"\n"+ symbol1+\
"\nUnaryOp:     "+ str(Stat.unop) +\
"\n   +:        "+ str(Stat.unop_uadd)+\
"\n   -:        "+ str(Stat.unop_usub)+\
"\n   ~:        "+ str(Stat.unop_invert)+\
"\n not:        "+ str(Stat.unop_not - Stat.single_not)+\
"\n single not: "+ str(Stat.single_not)+\
"\n"+ symbol1+\
"\nBoolOp:      "+ str(Stat.boolop) +\
"\n and:        "+ str(Stat.boolop_and)+\
"\n  or:        "+ str(Stat.boolop_or)+\
"\n"+ symbol1+\
"\nSingle:      "+ str(Stat.single_cond) +\
"\nname:        "+ str(Stat.single_name)+\
"\n  variable:  "+ str(Stat.single_variable)+\
"\n  subscript: "+ str(Stat.single_subscript)+\
"\n  attribute: "+ str(Stat.single_attribute)+\
"\nnum:         "+ str(Stat.single_num)+\
"\nstr:         "+ str(Stat.single_str)+\
"\ncollect:     "+ str(Stat.single_collect)+\
"\n"+ symbol1+\
"\nOther:       "+ str(Stat.unknown_condition+Stat.genexp + Stat.ifexp + Stat.listcomp + Stat.setcomp + Stat.lambda_condition) +\
"\n   GenExp:   "+ str(Stat.genexp) +\
"\n    IfExp:   "+ str(Stat.ifexp) +\
"\n ListComp:   "+ str(Stat.listcomp) +\
"\n  SetComp:   "+ str(Stat.setcomp) +\
"\n   Lambda:   "+ str(Stat.lambda_condition) +\
"\n  Unknown:   "+ str(Stat.unknown_condition) +\
"\n" + symbol2 + "\n\n\n" + \
symbol2 + "\nConditions by groups\n" + symbol1 +\
"\nNumeric:     " + str(Stat.group_integer)+\
"\nString:      " + str(Stat.group_string)+\
"\nObject:      " + str(Stat.group_object)+\
"\nType:        " + str(Stat.group_type)+\
"\nCollection:  " + str(Stat.group_collection)+\
"\n      set:   " + str(Stat.set_condition + Stat.setcomp)+\
"\n    tuple:   " + str(Stat.tuple_condition)+\
"\n     list:   " + str(Stat.list_condition + Stat.listcomp)+\
"\n     dict:   " + str(Stat.dict_condition)+\
"\n      sub:   " + str(Stat.sub_condition)+\
"\n  unknown:   " + str(Stat.compare_in + Stat.compare_notin + int(math.fsum(Stat.call_collection.values()))) +\
"\n"+ symbol1+ "\n" + \
"None and Bool conditions\n" + symbol1 +\
"\nTotal cond:  " + str(Stat.none)+\
"\n  is None:   " + str(Stat.none_is)+\
"\n   is T/F:   " + str(Stat.bool_is)+\
"\nis not None: " + str(Stat.none_isnot)+\
"\nis not T/F:  " + str(Stat.bool_isnot)+\
"\n  == None:   " + str(Stat.none_eq)+\
"\n   == T/F:   " + str(Stat.bool_eq)+\
"\n  != None:   " + str(Stat.none_noteq)+\
"\n   != T/F:   " + str(Stat.bool_noteq)+\
"\n    other:   " + str(Stat.none_other)+ "\n" + symbol2)
statistics.close()

## Output module file
find_modules = open(module_file, 'w')
find_modules.write('Project modules:' + '\n' + symbol2 + '\n')
for filename in Stat.dir_filenames:
	find_modules.write(filename + '\n')
find_modules.write(symbol2 + '\n' + 'Other modules:' + '\n' + symbol2 + '\n')
for filename in Stat.import_cash:
	find_modules.write(filename + '\n')	
find_modules.write(symbol2 + '\n' + 'ERROR modules:' + '\n' + symbol2 + '\n')
for filename in Stat.import_error:
	find_modules.write(filename + '\n')		
find_modules.close()

end = datetime.now()
print "Program end in " + str(end - start)
