# $Id: download.py,v 0.0 2012/05/06 05:48:22 eduardo Exp $
#
# @Copyright@
# 
# $Log: download.py,v $
# Revision 0.1  2012/12/06 05:48:22  eduardo
# Copyright Storm for Mamba
#

import os
import stat
import time
import shutil
import sys
import string
import subprocess
import rocks
import rocks.commands
import rocks.file

class Command(rocks.commands.create.command):
	"""	
	Download the OSG packages found in the
	repository located at 'URL'.

	<arg type='string' name='path'>	
	The network location of the repository of packages.
	</arg>
	
	<param type='string' name='version'>
	The OS version number to download. (default = the version of 
	Rocks running on this machine).
	</param>

	<param type='string' name='arch'>
	Architecture of the mirror to download. (default = the architecture of 
	of the OS running on this machine).
	</param>

	<example cmd='create osg download http://repo.grid.iu.edu/osg/3.1/el6/release/x86_64 version=6.5 arch=x86_64'>
	Will mirror(download) all the packages found under the URL
	http://repo.grid.iu.edu/osg/3.1/el6/release/x86_64 and will create a tree of dirs 6/x86_64 6/noarch 6/debug
	with latest version of osg packages ready to create osg roll.
	</example>
	"""


	def mirror(self, mirror_path):
		cmd = 'wget -erobots=off --reject "anaconda*rpm" -m -nv -np %s' % (mirror_path)
		os.system(cmd)

		if len(mirror_path) > 6:
			if mirror_path[0:6] == 'ftp://':
				mirrordir = mirror_path[6:]
			elif mirror_path[0:7] == 'http://':
				mirrordir = mirror_path[7:]
			else:
				mirrordir = mirror_path

		os.symlink(mirrordir, 'RPMS')


	def getRPMS(self, path):
		"""Return a list of all the RPMs in the given path, if multiple
		versions of a package are found only the most recent one will
		be included (just like rocks-dist)"""

		dict = {}
		tree = rocks.file.Tree(os.path.join(os.getcwd(), path))
		for dir in tree.getDirs():
			for file in tree.getFiles(dir):
				try:
					file.getPackageName()
				except AttributeError:
					continue # skip all non-rpm files

				# Resolve package versions

				name = file.getUniqueName()
				if not dict.has_key(name) or file >= dict[name]:
					dict[name] = file

		# convert the dictionary to a list and return all the RPMFiles

		list = []
		for e in dict.keys():
			list.append(dict[e])
		return list

	def copyFile(self, path, file):
		cwd = os.getcwd()
		dir      = os.path.join(cwd,path)
		fullname = os.path.join(dir, file.getName())
		if not os.path.isdir(dir):
			os.makedirs(dir)

		shutil.copy2(file.getFullName(), fullname)


	def clean(self):
		if os.path.islink('RPMS'):
			os.unlink('RPMS')


	def run(self, params, args):

		if len(args) != 1:
			self.abort('must supply one path')
		mirror_path = args[0]
		
		(version, arch) = self.fillParams(
			[('version', rocks.version),
			('arch',self.arch)])

		self.clean()
		
		self.mirror(mirror_path)

                list = []
		list.extend(self.getRPMS('RPMS'))

		for file in list:
			osgdir=version[0:1]+'/'+arch
			rpmfile=file.getName()
			if '-debuginfo-' in rpmfile:
				osgdir=version[0:1]+'/debug'
			if 'noarch.rpm' in rpmfile:
				osgdir=version[0:1]+'/noarch'
			if 'src.rpm' in rpmfile:
				osgdir=version[0:1]+'/src'
			self.copyFile(osgdir,file)

#debug#			print 'file base name %s ,full name=%s ' % (file.getBaseName(), file.getName())
		self.clean()


