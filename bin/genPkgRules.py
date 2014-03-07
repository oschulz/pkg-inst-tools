#!/usr/bin/env python

# Copyright (C) 2014 Oliver Schulz <oliver.schulz@tu-dortmund.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


import sys
if sys.version_info < (2, 7):
    raise SystemExit("ERROR: Python version >= 2.7 required.")

import codecs
import json
from collections import namedtuple
import glob
import re

def ntFromJSONFile(ntName, fileName):
	with codecs.open(fileName, encoding="utf-8") as file:
		data = json.load(file, object_hook=lambda d: namedtuple(ntName, d.keys())(*d.values()))
	return data

def toVarName(s):
	r = s.replace("+", "x")
	r = re.sub(r"[.-]", "_", r)
	return re.sub(r"^[^A-Za-z]|\W", "", r)

def instVar(pkgName):
	return toVarName(pkgName) + "_INST"

packages = [p for f in sys.argv[1:] for p in ntFromJSONFile("Struct", f).packages]

print("# Package installation detection")
print("")

for pkg in packages:
	print("{} = $(PREFIX)/bin/{}-config".format(instVar(pkg.name), pkg.name))

print("")
print("# Package rules and dependencies")

pkgNames = [pkg.name for pkg in packages]

for pkg in packages:
	print("")
	print(".PHONY: install-{}".format(pkg.name, pkg.name))
	print("INSTALL_ALL += install-{}".format(pkg.name))
	print("install-{}: $({})".format(pkg.name, instVar(pkg.name)))
	if hasattr(pkg, "options"):
		print("$({}): PKGFLAGS = {}".format(instVar(pkg.name), pkg.options))
	if hasattr(pkg, "requires") and set(pkg.requires).intersection(pkgNames):
		depString = " ".join(["$({})".format(instVar(dep)) for dep in pkg.requires if dep in pkgNames])
		print("$({}): {}".format(instVar(pkg.name), depString))
