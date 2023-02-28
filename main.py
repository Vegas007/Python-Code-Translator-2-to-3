# !/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "VegaS"
__date__ = "2021-01-22"
__version__ = "1.0.1"

import sys
import os
import re
import typing

from chardet.universaldetector import UniversalDetector

# test

# Check python version
if sys.version_info < (3, 7):
	print("This script needs at least Python 3.7.\nYou're using {}.".format('.'.join(map(str, sys.version_info[:3]))))
	sys.exit(0)

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Working directory
INPUT_DIRECTORY: str = 'modules'

# Disable pycharm inspections
DISABLE_PYCHARM_INSPECTION_TUPLE: tuple = (
	# [...]
)

"""
Print regex patterns
Replace the print statement with a print() function, with keyword arguments
to replace most of the special syntax of the old print statement.
:examples:
	print 100						print (100)
	print "test {}".format(100)		print ("test {}".format(100))
	print var #comment				print (var) #comment
"""
REGEX_PRINT_DICT: typing.Dict[str, str] = {
	r'print\s+(?![\'\"])([^#\n\r]+(?<! ))?': r'print(\1)',
	r'print\s+(ur|ru)?([\'\"]{1,3})([\w\W]+?)(\2)([^#\n\r]+(?<! ))?': r'print(\1\2\3\4\5)',
	r'print\s+(ur|ru)?([\'\"])(?!\2)([^\r\n]+)(\2)([^#\n\r]+(?<! ))?': r'print(\1\2\3\4\5)',
}

"""
Exception regex patterns
Fix all exceptions for all versions of python.

BaseException is the base class for all built-in exceptions.
Handling of exceptions has slightly changed in Python3+.
We have to use the 'as' keyword now.

:examples:
	except RuntimeError, msg:		except RuntimeError as msg:
	except:							except BaseException:
"""
EXCEPT_REGEX_DICT: typing.Dict[str, str] = {
	r'except\s+(.*?),(.*?:)': r'except \1 as \2',
	'except:': 'except BaseException:',
}

"""
# General regex patterns
Fix general changes made in python3.
	dict.has_key(), use the in operator instead.
	range() now behaves like xrange() used to behave, except it works with values of arbitrary size. 
	dict.iterkeys(), dict.iteritems() and dict.itervalues() methods are no longer supported.

:examples:
	for i in xrange(100)		for i in range(100
	if dict.has_key(100)		if 100 in dict
"""
GENERAL_REGEX_DICT: typing.Dict[str, str] = {
	'xrange': 'range',
	r'if\s+([\w.]+)\.has_key\(([^)]+)\)': r'if \2 in \1',
	'iteritems': 'items',
	'viewitems': 'items',
	'itervalues': 'values',
	'viewvalues': 'values',
	'iterkeys': 'keys',
	'viewkeys': 'keys',
}

"""
Raise exception regex patterns
Fix raising for all versions of python.
Raises an exception with the same syntax as calling a method,
it used to behave just like the syntax of calling an exception

:example:
	raise IOError, ('File not found')		raise IOError('File not found')
"""
RAISE_REGEX_DICT: typing.Dict[str, str] = {
	r'raise\s+(.*?),\s+(.*)': r'raise \1(\2)',
}

"""
Exec regex patterns
Fix exec calls for all versions of python.


:example:
	exec code in foo.__dict__		exec(code, foo.__dict__)
"""
EXEC_REGEX_DICT: typing.Dict[str, str] = {
	r'exec\s+(.*?)in\s+(.*)': r'exec(\1, \2)',
}

"""
Lib modules regex patterns
Fix renamed Lib modules names changed in python 3

:examples:
	__builtin__     builtins
"""
LIB_MODULES_REGEX_DICT: typing.Dict[str, str] = {
	r'__builtin__': r'builtins',
}


"""
Apply regex patterns
Fix calls for methods called from object using apply for python 3


:example:
	apply(method, args)		method(*args)
"""
APPLY_REGEX_DICT: typing.Dict[str, str] = {
	r'apply\((.*?),(.*?)\)': r'\1(*\2)',
}

# List for all the regex dicts of changes
regexDictList = (
	REGEX_PRINT_DICT,
	EXCEPT_REGEX_DICT,
	RAISE_REGEX_DICT,
	GENERAL_REGEX_DICT,
	EXEC_REGEX_DICT,
	LIB_MODULES_REGEX_DICT,
	APPLY_REGEX_DICT
)


class CodeTranslatorPy2To3:
	def __init__(self) -> typing.NoReturn:
		self.moduleNameSet: set = set()

	@staticmethod
	def has_inspection(fileContent: str) -> bool:
		"""
		A method that checking if a specific disabled inspection already exists in a specific file.
		:param fileContent: str
		:return: bool
		"""
		if not DISABLE_PYCHARM_INSPECTION_TUPLE:
			return True

		for inspectionName in DISABLE_PYCHARM_INSPECTION_TUPLE:
			if inspectionName in fileContent:
				return True
		return False

	@staticmethod
	def append_inspection(fileContent: str) -> str:
		"""
		A prepend method to insert a line to the beginning of a file.
		:param fileContent: str
		:return: str
		"""
		inspections = '\n'.join(DISABLE_PYCHARM_INSPECTION_TUPLE)
		return f"{inspections}\n{fileContent}"

	@staticmethod
	def process_function(regexDict: typing.Dict[str, str], fileContent: str, flags: int = re.IGNORECASE) -> str:
		"""
		A method that processes different replacements by regex patterns.
		:param regexDict: typing.Dict[str, str]
		:param fileContent: str
		:param flags: int
		:return: str
		"""
		for pattern, replace in sorted(regexDict.items()):
			fileContent = re.sub(pattern, replace, fileContent, flags=flags)
		return fileContent

	def initialize(self) -> typing.NoReturn:
		"""
		A method that generates the file names in a directory tree by walking the tree either top-down or bottom-up.
		If topdown is set to False, directories are scanned from the bottom-up.
		"""
		for root, dirs, files in os.walk(INPUT_DIRECTORY, topdown=False):
			for fileName in files:
				if fileName.endswith('.py'):
					self.moduleNameSet.add(os.path.join(root, fileName))

	def process_modules(self) -> typing.NoReturn:
		"""
		A method that opening all modules and doing specific actions.
		"""
		for moduleName in self.moduleNameSet:
			detected_encoding = detect_encoding(moduleName)

			print(f"Processing {moduleName} ({detected_encoding})")

			with open(moduleName, 'r+', encoding=detected_encoding) as fileStream:
				# Store the content of the file
				fileContent: str = fileStream.read()
				# Sets the file's current position at the offset, the position of the read/write pointer within the file
				fileStream.seek(0, 0)
				#  Truncates the file's size
				fileStream.truncate()

				# Process regex patterns
				for regexDict in regexDictList:
					fileContent = self.process_function(regexDict, fileContent)

				# Rewrite the processed content of the file
				fileStream.write(fileContent)


def detect_encoding(fileName):
	detector = UniversalDetector()

	for line in open(fileName, 'rb'):
		detector.feed(line)
		if detector.done:
			break

	detector.close()
	return detector.result["encoding"]


if __name__ == '__main__':
	instance = CodeTranslatorPy2To3()
	instance.initialize()
	instance.process_modules()
