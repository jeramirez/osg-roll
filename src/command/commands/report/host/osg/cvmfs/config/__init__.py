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

	Output the OSG cvmfs Configuration
	Uses Rocks Attributes: OSG_CVMFS_REPOSITORIES, OSG_CVMFS_CACHE_BASE, OSG_CVMFS_QUOTA_LIMIT,
	OSG_CVMFS_HTTP_PROXY, OSG_CMS_LOCAL_SITE, OSG_CVMFS_SERVER_URL,OSG_CVMFS_NFS_SOURCE,OSG_CVMFS_MEMCACHE_SIZE

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /etc/cvmfs/default.local
	</param>

	<param type='string' name='CMSConfigFile'>
	Defaults to: /etc/cvmfs/config.d/cms.cern.ch.local
	</param>

	<param type='string' name='CVMFSServerConfigFile'>
	Defaults to: /etc/cvmfs/domain.d/cern.ch.local
	</param>

	<example cmd='report host osg cvmfs config compute-0-0'>
	Create/Modify the OSG cvmfs Configuration for compute-0-0
	</example>

	<example cmd='report host osg cvmfs config compute-0-0 ConfigFile=/etc/cvmfs/test.local'>
	Create the OSG cvmfs Configuration for compute-0-0 on files 
        /etc/cvmfs/test.local, /etc/cvmfs/config.d/cms.cern.ch.local and /etc/cvmfs/domain.d/cern.ch.local
	</example>

	<example cmd='report host osg cvmfs config compute-0-0 ConfigFile=/etc/cvmfs/test.local CVMFSServerConfigFile=/etc/cvmfs/CvmfsServerTest.local'>
	Create the OSG cvmfs Configuration for compute-0-0 on files 
        /etc/cvmfs/test.local, /etc/cvmfs/config.d/cms.cern.ch.local and /etc/cvmfs/CvmfsServerTest.local
	</example>
	"""

	def writeConfigFile(self, dictList, dictlines, configFile):
		self.addOutput(self.host, '<file name="%s" perms="0644">' % (configFile))
		lines = dictlines.keys()
		lines.sort()

		for line in lines:
			key = dictlines[line]
			self.addOutput(self.host,'%s=%s' %(key,dictList[key]))
		self.addOutput(self.host, '</file>')


	def initializeDictionary(self):
		### These are the OSG cvmfs Parameters that we will define.
                ### When Adding new ones, Add them here.
		self.dict = {}
		self.dictcomment={}
		self.dictlines1={}
		self.dictlines2={}
		self.dictlines3={}
		self.dictlines1['A001_LINE']='CVMFS_REPOSITORIES'
		self.dict['CVMFS_REPOSITORIES']="`echo $(ls /cvmfs)|tr ' ' ,`"
		self.dictlines1['A002_LINE']='CVMFS_CACHE_BASE'
		self.dict['CVMFS_CACHE_BASE']="/var/cache/cvmfs"
		self.dictlines1['A003_LINE']='CVMFS_QUOTA_LIMIT'
		self.dict['CVMFS_QUOTA_LIMIT']=20000
		self.dictlines1['A004_LINE']='CVMFS_HTTP_PROXY'
		self.dict['CVMFS_HTTP_PROXY']='"http://login-0-0:3128"'
		self.dictlines2['B001_LINE']='CMS_LOCAL_SITE'
		self.dict['CMS_LOCAL_SITE']="T3_US_PuertoRico"
		self.dictlines3['C001_LINE']='CVMFS_SERVER_URL'
		self.dict['CVMFS_SERVER_URL']='"http://cvmfs.fnal.gov:8000/opt/@org@;http://cvmfs.racf.bnl.gov:8000/opt/@org@;http://cvmfs-stratum-one.cern.ch:8000/opt/@org@;http://cernvmfs.gridpp.rl.ac.uk:8000/opt/@org@"'

	def fillFromRollDefault(self):
		self.dict['CVMFS_REPOSITORIES'] = "cms.cern.ch"
		self.dict['CVMFS_CACHE_BASE']= "/var/cache/cvmfs"
		self.dict['CVMFS_QUOTA_LIMIT']= 10000
		self.dict['CVMFS_HTTP_PROXY']= "http://login-0-2:3128"
		self.dict['CMS_LOCAL_SITE']="T3_US_PuertoRico"

	def fillFromRocksAttributes(self):
		if self.db.getHostAttr(self.host,'OSG_CVMFS_REPOSITORIES') > 0:
			self.dict['CVMFS_REPOSITORIES']='%s' % \
				(self.db.getHostAttr(self.host, 'OSG_CVMFS_REPOSITORIES'))

		if self.db.getHostAttr(self.host,'OSG_CVMFS_CACHE_BASE') > 0:
			self.dict['CVMFS_CACHE_BASE']='%s' % \
				(self.db.getHostAttr(self.host, 'OSG_CVMFS_CACHE_BASE'))

		if self.db.getHostAttr(self.host,'OSG_CVMFS_QUOTA_LIMIT') > 0:
			self.dict['CVMFS_QUOTA_LIMIT'] = '%s' % \
				(self.db.getHostAttr(self.host, 'OSG_CVMFS_QUOTA_LIMIT'))

		if self.db.getHostAttr(self.host,'OSG_CVMFS_HTTP_PROXY') > 0:
			self.dict['CVMFS_HTTP_PROXY'] = '%s' % \
				(self.db.getHostAttr(self.host, 'OSG_CVMFS_HTTP_PROXY'))

		if self.db.getHostAttr(self.host,'OSG_CMS_LOCAL_SITE') > 0:
			self.dict['CMS_LOCAL_SITE'] = '%s' % \
				(self.db.getHostAttr(self.host, 'OSG_CMS_LOCAL_SITE'))

		if self.db.getHostAttr(self.host,'OSG_CVMFS_SERVER_URL') > 0:
			self.dict['CVMFS_SERVER_URL'] = '%s' % \
				(self.db.getHostAttr(self.host, 'OSG_CVMFS_SERVER_URL'))

		#Non-default attrs but useful when using nfs
		if self.db.getHostAttr(self.host,'OSG_CVMFS_NFS_SOURCE') > 0:
			self.dictlines1['A005_LINE']='CVMFS_NFS_SOURCE'
			self.dict['CVMFS_NFS_SOURCE'] = '%s' % \
				(self.db.getHostAttr(self.host, 'OSG_CVMFS_NFS_SOURCE'))

		if self.db.getHostAttr(self.host,'OSG_CVMFS_MEMCACHE_SIZE') > 0:
			self.dictlines1['A006_LINE']='CVMFS_MEMCACHE_SIZE'
			self.dict['CVMFS_MEMCACHE_SIZE'] = '%s' % \
				(self.db.getHostAttr(self.host, 'OSG_CVMFS_MEMCACHE_SIZE'))


	def run(self, params, args):

		self.initializeDictionary()
		self.ConfigFile, = self.fillParams([('ConfigFile','/etc/cvmfs/default.local') ])
		self.CMSConfigFile, = self.fillParams([('CMSConfigFile','/etc/cvmfs/config.d/cms.cern.ch.local') ])
		self.CVMFSServerConfigFile, = self.fillParams([('CVMFSServerConfigFile','/etc/cvmfs/domain.d/cern.ch.local') ])
		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			self.fillFromRollDefault()
			self.fillFromRocksAttributes()
			self.writeConfigFile(self.dict, self.dictlines1, self.ConfigFile)
			self.writeConfigFile(self.dict, self.dictlines2, self.CMSConfigFile)
			self.writeConfigFile(self.dict, self.dictlines3, self.CVMFSServerConfigFile)
			self.addOutput(self.host, '<file name="/etc/fuse.conf" perms="0644" >')
			self.addOutput(self.host, 'user_allow_other')
			self.addOutput(self.host, '</file>')
			self.addOutput(self.host, 'service autofs restart')

		self.endOutput(padChar='')

