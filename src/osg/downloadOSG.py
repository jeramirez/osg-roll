#! /opt/rocks/bin/python
# $Id: downloadOSG.py,v 0.0 2012/05/06 05:48:22 eduardo Exp $
#
# @Copyright@
# 
# $Log: downloadOSG.py,v $
# Revision 1.23  2012/05/06 05:48:22  eduardo
# Initial Version

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


class Command:
	"""	
	Download OSG packages from repository located at 'URL'.

	<arg type='string' name='path'> 
	The network location of the repository of packages.
	default path is a local mirror of OSG repository for el6
	http://localhost/install/repo.grid.iu.edu/osg/3.2/el6/release/x86_64
	</arg>

	<example cmd='downloadOSG.py http://repo.grid.iu.edu/osg/3.2/el6/release/x86_64 >
	Will download all the packages found under the URL
	http://repo.grid.iu.edu/osg/3.2/el6/release/x86_64 and will create
	dirs 5/x86_64 5/debug 5/noarch
	</example>
	"""

	def abort(self, msg):
		rocks.commands.Abort(msg, 0)
		sys.exit(-1)
 
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

#debug#		print ' copying ... %s to %s' % (file.getName(), dir)
		shutil.copy2(file.getFullName(), fullname)


	def clean(self):
		if os.path.islink('RPMS'):
			os.unlink('RPMS')


	def run(self, params, args):

		if len(args) != 1:
			print 'running args=%s' % args
			self.abort('must supply one path')
		mirror_path = args[0]
		

		self.clean()
		
		self.mirror(mirror_path)

		list = []
		list.extend(self.getRPMS('RPMS'))

#                rockscmd='lsb_release -rs | cut -d . -f 1'
#for python 2.7
#		getrocksversion=subprocess.check_output(rockscmd)
		getrocksversion=subprocess.Popen([ 'lsb_release', '-rs' ],stdout=subprocess.PIPE).communicate()[0]
		for file in list:
			osgdir=getrocksversion[0:1]+'/x86_64'
			rpmfile=file.getName()
			if '-debuginfo-' in rpmfile:
				osgdir=getrocksversion[0:1]+'/debug'
			if 'noarch.rpm' in rpmfile:
				osgdir=getrocksversion[0:1]+'/noarch'
			self.copyFile(osgdir,file)

		self.clean()
                print 'test rocks version=%s dir=%s' % (getrocksversion[0:1],osgdir)

#check if arguments are empty, set a default
if len(sys.argv) == 1:
#        args = [ 'http://localhost/install/repo.grid.iu.edu/3.0/el5/osg-release'] 
        args = [ 'http://localhost/install/repo.grid.iu.edu/osg/3.2/el6/release/x86_64'] 
else:
        args = sys.argv[1:]

print '#args=%s' % len(args)
print 'args=%s' % args
mycommand = Command()
mycommand.run(len(args),args)
