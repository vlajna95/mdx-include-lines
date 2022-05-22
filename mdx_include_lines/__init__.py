#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# {[type] [start at line]-[end at line] [file]  [caption]  [show line numbers (use 0 or 1)}
# example: 
# {python 15-20 include.py  An example of a Python function  1}
# In case you want to include the whole file: 
# {python * include.py  A function written in Python  1}
# In case you want to include only one line: 
# {python 15 include.py  The return line  0}
# In case you want to include only certain lines of code: 
# {python [15,20,3] include.py  All return expressions  1}

from __future__ import print_function
import re
import os.path
from codecs import open
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

# version 1.0
#SYNTAX = re.compile(r'\{([a-z]+)\s(([0-9]+)\s-\s([0-9]+)|([0-9]+)-([0-9]+)|([0-9]+)\s-([0-9]+)|([0-9]+)-\s([0-9]+)|\*)\s(.*)}')
#version 1.1
# SYNTAX = re.compile(r'\{([a-z]+)\s(([0-9]+)\s-\s([0-9]+)|([0-9]+)-([0-9]+)|([0-9]+)\s-([0-9]+)|([0-9]+)-\s([0-9]+)|\*|([0-9]+)|\[(.*)\])\s(.*)}')

SYNTAX = re.compile(r'\{([a-z]+)\s(([0-9]+)\s-\s([0-9]+)|([0-9]+)-([0-9]+)|([0-9]+)\s-([0-9]+)|([0-9]+)-\s([0-9]+)|\*|([0-9]+)|\[(.*)\])\s(.*)\s{2}(.*)\s{2}(\d{1})}')


class MarkdownIncludeLines(Extension):
	def __init__(self, configs={}):
		self.config = {
			"base_path": [os.getcwd(), "Default location for the file to be checked - relative paths for the include statement."],
			"encoding": ["utf-8", "Encoding of the file."],
			"line_nums": [False, "Include the line numbers - False/True"],
		}
		for key, value in configs.items():
			self.setConfig(key, value)
	
	def extendMarkdown(self, md, md_globals):
		md.preprocessors.add(
			'include_lines', IncLinePreprocessor(md,self.getConfigs()),'_begin'
		)


class IncLinePreprocessor(Preprocessor):
	#member vars:
	#contains
	m_filename = None
	m_code = []
	
	#methods:
	def __init__(self,md,config):
		super(IncLinePreprocessor, self).__init__(md)
		self.base_path = config['base_path']
		self.encoding = config['encoding']
		self.line_nums = config['line_nums']
	
	def run(self,lines):
		done = False
		while not done:
			for line in lines:
				loc = lines.index(line)
				m = SYNTAX.search(line)
				if m:
					match = SYNTAX.match(line);
					codetype = match.group(1)
					filename = match.group(13)
					description = match.group(14)
					self.line_nums = int(match.group(15))
					start = -1;
					end = -1;
					rangeList = []
					# print (match.groups())
					for x in range(2, 13):
						if match.group(x) != None and match.group(x) != "*" and x != 2 and x != 12:
							if start == -1:
								start = int(match.group(x))
								continue
							elif end == -1:
								end = int(match.group(x))
						elif match.group(x) == "*":
							break
						elif x == 12 and match.group(x) != None:
							rangeList = match.group(x).split(",")
							break;
				#include lines of the range start - end
					if (start <= 0 or end <= 0) and start <= end and len(rangeList) == 0:
						lines = lines[:loc] + self.makeCode(filename, codetype, self.parse(filename), description) + lines[loc+1:]
					elif len(rangeList) == 0:
						lines = lines[:loc] + self.makeCode(filename, codetype, self.parse(filename, start, end, False), description) + lines[loc+1:]
					else:
						result = []
						for index in rangeList:
							line = self.parse(filename, int(index), -1, False)
							if len(line) > 0:
								result.append("[...]")
								result.extend()
							else:
								result.append("Line " + index + " could not be found.")
						lines = lines[:loc] + self.makeCode(filename, codetype, result, description) + lines[loc+1:]
					if filename != self.m_filename:
						self.m_filename = filename;
				else:
					done = True
		return lines
	
	def makeCode(self, filename, codeType, codeList, buttonText):
		output = [];
		output.append(f"??? \"{buttonText}\"")
		output.append("\t```"+codeType) #+" {aria-label='"+buttonText+"'}")
		# output.append("Source file: "+filename+"\n\n")
		output.extend([f"\t{codeLine}" for codeLine in codeList])
		output.append("\t```\n")
		return output
	
	def parse(self, filename, start=0, end=0, wholepage=True):
		#correct start
		if start == 1:
			start -= 1
		#check if filename is not the same then load data
		data = None
		if filename != self.m_filename:
			data = self.readFile(filename)
		else:
			data = self.m_code
		#parse
		outcome = []
		for cnt, line in enumerate(data):
			line = line.rstrip('\n')
			# if cnt >= start and cnt <= end or wholepage == True:
			outcome.append(f"{str(cnt) + ' ' if self.line_nums else ''}{line}")
			"""
			elif end == -1 and cnt == start:
				outcome.append(f"\t{str(cnt) + ' ' if self.line_nums else '\t'}{line}")
			"""
		return outcome		
	
	def readFile(self,filename):
		filename = os.path.expanduser(filename)
		if not os.path.isabs(filename):
			filename = os.path.normpath(
				os.path.join(self.base_path,filename)
			)
		try:
			#open file:
			with open(filename, 'r', encoding=self.encoding) as file:
				self.m_code = file.readlines()
				return self.m_code
		except Exception as e:
			print('Warning: could not find file {}. Ignoring include statement. Error: {}'.format(self.m_filename, e))
			return ['Warning: could not find file {}. File:'.format(self.m_filename, e)]
		


def makeExtension(*args,**kwargs):
	return MarkdownIncludeLines(kwargs)
