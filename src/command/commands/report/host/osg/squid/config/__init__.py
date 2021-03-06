#$Id$
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log$
# Revision 1.10  2012/10/26 05:48:54  eduardo
# Creation
#

import sys
import os
import pwd
import string
import types
import rocks.commands
from syslog import syslog

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""

	Output the OSG frontier squid Local Configuration
	Uses Rocks Attributes: Kickstart_PublicNetmaskCIDR, Kickstart_PublicNetwork, Kickstart_PrivateNetmaskCIDR,
	Kickstart_PrivateNetwork, OSG_SquidCacheMem, OSG_SquidCacheDir, OSG_SquidCacheDirSize

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /etc/squid/customize.sh
	</param>

	<example cmd='report host osg squid config squid-0-0'>
	Create/Modify the OSG frontier squid Configuration for squid-0-0
	</example>

	<example cmd='report host osg squid config squid-0-0 ConfigFile=/etc/squid/test.sh'>
	Create the OSG frontier squid Configuration for squid-0-0 on file /etc/squid/test.sh
	</example>
	"""

	def writeConfigFile(self, dictList, dictlines, configFile):
		self.addOutput(self.host, '<file name="%s">' % (configFile))
		lines = dictlines.keys()
		lines.sort()
		self.addOutput(self.host,'#!/bin/bash')
		self.addOutput(self.host,'#')
		self.addOutput(self.host,'# Edit customize.sh as you wish to customize squid.conf.')
		self.addOutput(self.host,'# It will not be overwritten by upgrades.')
		self.addOutput(self.host,'# See customhelps.awk for information on predefined edit functions.')
		self.addOutput(self.host,'# In order to test changes to this, run this to regenerate squid.conf:')
		self.addOutput(self.host,'# \tservice frontier-squid')
		self.addOutput(self.host,'# and to reload the changes into a running squid use')
		self.addOutput(self.host,'# \tservice frontier-squid reload')
		self.addOutput(self.host,'# Avoid single quotes in the awk source or you have to protect them from bash.')
		self.addOutput(self.host,'#')
		self.addOutput(self.host,"")
		self.addOutput(self.host,"awk --file `dirname $0`/customhelps.awk --source '{")

		for line in lines:
			key = dictlines[line]
			self.addOutput(self.host,'%s' %(dictList[key]))
		self.addOutput(self.host,"print")
		self.addOutput(self.host,"}'")
		self.addOutput(self.host, '</file>')


	def initializeDictionary(self):
		### These are the OSG squid Parameters that we will define.
                ### When Adding new ones, Add them here.
		self.dict = {}
		self.dictcomment={}
		self.dictlines={}
		self.dictlines['A001_LINE']='acl NET_LOCAL src'
		self.dict['acl NET_LOCAL src']='setoption("acl NET_LOCAL src", "10.0.0.0/8 172.16.0.0/12 192.168.0.0/16")'
		self.dictlines['A002_LINE']='cache_mem'
		self.dict['cache_mem']='setoption("cache_mem", "128 MB")'
		self.dictlines['A003_LINE']='cache_dir2'
		self.dict['cache_dir2']='setoptionparameter("cache_dir", 2, "/var/cache/squid")'
		self.dictlines['A004_LINE']='cache_dir3'
		self.dict['cache_dir3']='setoptionparameter("cache_dir", 3, "10000")'

	def fillFromRollDefault(self):
		self.dict['acl NET_LOCAL src'] = 'setoption("acl NET_LOCAL src", "10.0.0.0/8 172.16.0.0/12 192.168.0.0/16")'
		self.dict['cache_mem']= 'setoption("cache_mem", "512 MB")'
		self.dict['cache_dir2']= 'setoptionparameter("cache_dir", 2, "/var/cache/squid")'
		self.dict['cache_dir3']= 'setoptionparameter("cache_dir", 3, "10000")'

	def fillFromRocksAttributes(self):
		Networks=''
		if self.db.getHostAttr(self.host,'Kickstart_PrivateNetwork') > 0:
			Networks += "%s" % \
				(self.db.getHostAttr(self.host, 'Kickstart_PrivateNetwork'))
		if self.db.getHostAttr(self.host,'Kickstart_PrivateNetmaskCIDR') > 0:
			Networks += "/%s" % \
				(self.db.getHostAttr(self.host, 'Kickstart_PrivateNetmaskCIDR'))

		if self.db.getHostAttr(self.host,'Kickstart_PublicNetwork') > 0:
			Networks += " %s" % \
				(self.db.getHostAttr(self.host, 'Kickstart_PublicNetwork'))

		if self.db.getHostAttr(self.host,'Kickstart_PublicNetmaskCIDR') > 0:
			Networks += "/%s" % \
				(self.db.getHostAttr(self.host, 'Kickstart_PublicNetmaskCIDR'))

		if Networks > 0:
			self.dict['acl NET_LOCAL src']='setoption("acl NET_LOCAL src", "%s")' % Networks

		if self.db.getHostAttr(self.host,'OSG_SquidCacheMem') > 0:
			self.dict['cache_mem']='setoption("cache_mem", "%s")' % \
				(self.db.getHostAttr(self.host, 'OSG_SquidCacheMem'))

		if self.db.getHostAttr(self.host,'OSG_SquidCacheDir') > 0:
			self.dict['cache_dir2']='setoptionparameter("cache_dir", 2, "%s")' % \
				(self.db.getHostAttr(self.host, 'OSG_SquidCacheDir'))

		if self.db.getHostAttr(self.host,'OSG_SquidCacheDirSize') > 0:
			self.dict['cache_dir3'] = 'setoptionparameter("cache_dir", 3, "%s")' % \
				(self.db.getHostAttr(self.host, 'OSG_SquidCacheDirSize'))


	def find_executable(self, executable, path=None):
		""" find a path to the executable """
		if os.path.isfile(executable):
			return executable

		if path is None:
			path = os.environ['PATH']
		paths = string.split(path, os.pathsep)
	
		for path in paths:
			fullname = os.path.join(path, executable)
			if os.path.isfile(fullname):
				return fullname
		return ''


	def run(self, params, args):

		self.initializeDictionary()
		self.ConfigFile, = self.fillParams([('ConfigFile','/etc/squid/customize.sh') ])
		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			osg_squid = self.db.getHostAttr(host,'OSG_SQUID')
			is_ce     = self.db.getHostAttr(host,'OSG_CE') > 0
			if osg_squid or is_ce:
				self.fillFromRollDefault()
				self.fillFromRocksAttributes()
				self.writeConfigFile(self.dict, self.dictlines, self.ConfigFile)

		self.endOutput(padChar='')

