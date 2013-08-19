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

	Output the OSG Hadoop Local Configuration
	Uses Rocks Attributes: OSG_HadoopNameNode, OSG_HadoopDataDir, OSG_HadoopData,
	OSG_HadoopSecondaryNode, OSG_HadoopCheckPointDirs, OSG_HadoopCheckPointPeriod, 
        OSG_HadoopReplicationDefault, OSG_HadoopUpdateFstab, ganglia_address,
	Kickstart_PrivateDNSDomain

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /etc/sysconfig/hadoop
	</param>

	<example cmd='report host osg hadoop config compute-0-0'>
	Create the OSG Hadoop Configuration for compute-0-0
	</example>

	<example cmd='report host osg hadoop config compute-0-0 ConfigFile=/etc/sysconfig/hadooptest'>
	Create the OSG Hadoop Configuration for compute-0-0 on file /etc/sysconfig/hadooptest
	</example>
	"""

	def writeConfigFile(self, dictList, commentList, dictlines, configFile):
		self.addOutput(self.host, '<file name="%s">' % (configFile))
		lines = dictlines.keys()
		lines.sort()
		for line in lines:
			key = dictlines[line]
			if commentList.has_key(key) and commentList[key]:
				self.addOutput(self.host,'%s' %(commentList[key]))
			self.addOutput(self.host,'%s=%s' %(key,dictList[key]))
			self.addOutput(self.host,"")
		self.addOutput(self.host, '</file>')


	def initializeDictionary(self):
		### These are the OSG Hadoop Parameters that we will 
                ### Define. When Adding new ones, Add them here.
		self.dict = {}
		self.dictcomment={}
		self.dictlines={}
		self.dictlines['A001_LINE']='HADOOP_CONF_DIR'
		self.dictcomment['HADOOP_CONF_DIR']= "# The directory that contains the hadoop configuration files.\n# Don't change this unless you know what you're doing!"
		self.dict['HADOOP_CONF_DIR']='/etc/hadoop-0.20/conf'
		self.dictlines['A002_LINE']='HADOOP_NAMENODE'
		self.dictcomment['HADOOP_NAMENODE']="# The server that will act as the namenode.  This must match the\n# output of 'hostname -s' on the namenode server so that\n# /etc/init.d/hadoop can identify when it is being run on the namenode."
		self.dict['HADOOP_NAMENODE']='@HADOOP_NAMENODE@'
		self.dictlines['A003_LINE']='HADOOP_NAMEPORT'
		self.dictcomment['HADOOP_NAMEPORT']="# The port that the namenode will listen on.  This is usually set to\n# 9000 unless you are running an unsupported configuration with\n# a datanode and namenode on the same host."
		self.dict['HADOOP_NAMEPORT']='9000'
		self.dictlines['A004_LINE']='HADOOP_PRIMARY_HTTP_ADDRESS'
		self.dictcomment['HADOOP_PRIMARY_HTTP_ADDRESS']="# The host:port for accessing the namenode web interface.  This is\n# used by the checkpoint server for getting checkpoints."
		self.dict['HADOOP_PRIMARY_HTTP_ADDRESS']='${HADOOP_NAMENODE}:50070'
		self.dictlines['A005_LINE']='HADOOP_REPLICATION_DEFAULT'
		self.dictcomment['HADOOP_REPLICATION_DEFAULT']="# Default number of replicas requested by the client.  The default\n# number of replicas for each file is a _client_ side setting, not\n# a setting on the namenode."
		self.dict['HADOOP_REPLICATION_DEFAULT']='@HADOOP_REPLICATION_DEFAULT@'
		self.dictlines['A006_LINE']='HADOOP_REPLICATION_MIN'
		self.dictcomment['HADOOP_REPLICATION_MIN']="# Minimum number of replicas allowed by the server.  1 is a good\n# value.  Clients will not be able to request fewer than this\n# number of replicas."
		self.dict['HADOOP_REPLICATION_MIN']='1'
		self.dictlines['A007_LINE']='HADOOP_REPLICATION_MAX'
		self.dictcomment['HADOOP_REPLICATION_MAX']="# Maximum number of replicas allowed by the server.  Clients will\n# not be able to requeset more than this number of replicas."
		self.dict['HADOOP_REPLICATION_MAX']='512'
		self.dictlines['A008_LINE']='HADOOP_USER'
		self.dictcomment['HADOOP_USER']="# The user that the hadoop datanode and checkpoint server processes will run as."
		self.dict['HADOOP_USER']='hdfs'
		self.dictlines['A009_LINE']='HADOOP_DATADIR'
		self.dictcomment['HADOOP_DATADIR']="# The base directory where most datanode files are stored"
		self.dict['HADOOP_DATADIR']='@HADOOP_DATADIR@'
		self.dictlines['A010_LINE']='HADOOP_DATA'
		self.dictcomment['HADOOP_DATA']="# The directory that will store the actual hdfs data on this datanode\n# Multiple directories can be specified using a comma-separated list of\n# directory names (with no spaces)"
		self.dict['HADOOP_DATA']='${HADOOP_DATADIR}/data'
		self.dictlines['A011_LINE']='HADOOP_LOG'
		self.dictcomment['HADOOP_LOG']="# The directory where the namenode/datanode log files are stored"
		self.dict['HADOOP_LOG']='/var/log/hadoop'
		self.dictlines['A012_LINE']='HADOOP_SCRATCH'
		self.dictcomment['HADOOP_SCRATCH']="# The directory where the namenode stores the hdfs namespace"
		self.dict['HADOOP_SCRATCH']='${HADOOP_DATADIR}/scratch'
		self.dictlines['A013_LINE']='HADOOP_GANGLIA_ADDRESS'
		self.dictcomment['HADOOP_GANGLIA_ADDRESS']="# Set this to an empty string to have the hadoop-firstboot script\n# try to determine the ganglia multicast address from /etc/gmond.conf"
		self.dict['HADOOP_GANGLIA_ADDRESS']='@HADOOP_GANGLIA_ADDRESS@'
		self.dictlines['A014_LINE']='HADOOP_GANGLIA_PORT'
#		self.dictcomment['HADOOP_GANGLIA_PORT']=''
		self.dict['HADOOP_GANGLIA_PORT']='8649'
		self.dictlines['A015_LINE']='HADOOP_GANGLIA_INTERVAL'
		self.dictcomment['HADOOP_GANGLIA_INTERVAL']="# The interval, in seconds, at which metrics are reported to Ganglia."
		self.dict['HADOOP_GANGLIA_INTERVAL']='10'
		self.dictlines['A016_LINE']='HADOOP_SECONDARY_NAMENODE'
		self.dictcomment['HADOOP_SECONDARY_NAMENODE']="# The name of the checkpoint server.  This must match the output\n# of 'hostname -s' so that the hadoop init script knows where\n# to start the checkpoint service."
		self.dict['HADOOP_SECONDARY_NAMENODE']='@HADOOP_SECONDARY_NAMENODE@'
		self.dictlines['A017_LINE']='HADOOP_SECONDARY_HTTP_ADDRESS'
#		self.dictcomment['HADOOP_SECONDARY_HTTP_ADDRESS']=''
		self.dict['HADOOP_SECONDARY_HTTP_ADDRESS']='${HADOOP_SECONDARY_NAMENODE}:50090'
		self.dictlines['A018_LINE']='HADOOP_CHECKPOINT_DIRS'
		self.dictcomment['HADOOP_CHECKPOINT_DIRS']="# Comma-separated list of directories that will be used for storing namenode\n# checkpoints.  At least one of these should be on nfs."
		self.dict['HADOOP_CHECKPOINT_DIRS']='@HADOOP_CHECKPOINT_DIRS@'
		self.dictlines['A019_LINE']='HADOOP_CHECKPOINT_PERIOD'
		self.dictcomment['HADOOP_CHECKPOINT_PERIOD']="# The interval, in seconds, between checkpoints.  Set to 3600 to\n# generate a checkpoint once per hour.  If set to 3600, then if\n# the namenode gets corrupted then you should not lose any\n# namespace changes that are > 1 hour old."
		self.dict['HADOOP_CHECKPOINT_PERIOD']='@HADOOP_CHECKPOINT_PERIOD@'
		self.dictlines['A020_LINE']='HADOOP_DATANODE_BLOCKSIZE'
		self.dictcomment['HADOOP_DATANODE_BLOCKSIZE']="# The default block size for files in hdfs.  The default is 128M."
		self.dict['HADOOP_DATANODE_BLOCKSIZE']='134217728'
		self.dictlines['A021_LINE']='HADOOP_NAMENODE_HEAP'
		self.dictcomment['HADOOP_NAMENODE_HEAP']="# The jvm heap size for the namenode.  The rule of thumb is a\n# minimum of 1GB per million hdfs blocks.  With a 128MB block\n# size, this comes out to roughly 1GB per 128TB of storage space."
		self.dict['HADOOP_NAMENODE_HEAP']='2048'
		self.dictlines['A022_LINE']='HADOOP_MIN_DATANODE_SIZE'
		self.dictcomment['HADOOP_MIN_DATANODE_SIZE']="# The minimum size of the hadoop data directory, in GB.  The hadoop init\n# script checks that the partition is at least this size before\n# attempting to start the datanode.  This can be used to prevent starting\n# a datanode on systems that don't have very much data space.  Set to\n# zero to skip this check"
		self.dict['HADOOP_MIN_DATANODE_SIZE']='0'
		self.dictlines['A023_LINE']='HADOOP_RACK_AWARENESS_SCRIPT'
		self.dictcomment['HADOOP_RACK_AWARENESS_SCRIPT']="# The name of a script that takes a list of IP addresses and returns\n# a list of rack names.  Hadoop uses this to make rack-aware intelligent\n# decisions for data block replication."
		self.dict['HADOOP_RACK_AWARENESS_SCRIPT']=''
		self.dictlines['A024_LINE']='HADOOP_SYSLOG_HOST'
		self.dictcomment['HADOOP_SYSLOG_HOST']="# The central syslog collector.  If set, then logs will be sent to the\n# syslog server in addition to being stored locally."
		self.dict['HADOOP_SYSLOG_HOST']=''
		self.dictlines['A025_LINE']='HADOOP_UPDATE_FSTAB'
		self.dictcomment['HADOOP_UPDATE_FSTAB']="# Set this to '1' to automatically update fstab with an entry for \n# the hadoop fuse mount on /mnt/hadoop.  If you prefer to add this manually,\n# then you will need to add the following to fstab, replacing 'namenode.host'\n# with the fqdn of your namenode.\n# hdfs# /mnt/hadoop fuse server=namenode.host,port=9000,rdbuffer=131072,allow_other 0 0"
		self.dict['HADOOP_UPDATE_FSTAB']='0'


	def fillFromRollDefault(self):
		self.dict['HADOOP_NAMENODE'] = 'compute-0-0'
		self.dict['HADOOP_REPLICATION_DEFAULT']= '2'
		self.dict['HADOOP_DATADIR']= '/hadoop'
		self.dict['HADOOP_DATA']= '/hadoop/data'
		self.dict['HADOOP_GANGLIA_ADDRESS']= '223.0.0.3'
		self.dict['HADOOP_SECONDARY_NAMENODE'] = 'compute-0-1'
		self.dict['HADOOP_CHECKPOINT_DIRS']= '/home/hadoop,/var/log/hadoop'
		self.dict['HADOOP_CHECKPOINT_PERIOD']= '600'
		self.dict['HADOOP_UPDATE_FSTAB']= '0'

	def fillFromRocksAttributes(self):
		if self.db.getHostAttr(self.host,'OSG_HadoopNameNode') > 0:
			self.dict['HADOOP_NAMENODE'] = "%s" % \
				(self.db.getHostAttr(self.host, 'OSG_HadoopNameNode'))

		if self.db.getHostAttr(self.host,'OSG_HadoopReplicationDefault') > 0:
			self.dict['HADOOP_REPLICATION_DEFAULT']= "%s" % \
				(self.db.getHostAttr(self.host, 'OSG_HadoopReplicationDefault'))

		if self.db.getHostAttr(self.host,'OSG_HadoopDataDir') > 0:
			self.dict['HADOOP_DATADIR']="%s" % \
				(self.db.getHostAttr(self.host, 'OSG_HadoopDataDir'))

		if self.db.getHostAttr(self.host,'OSG_HadoopData') > 0:
			self.dict['HADOOP_DATA']="%s" % \
				(self.db.getHostAttr(self.host, 'OSG_HadoopData'))

		if self.db.getHostAttr(self.host,'ganglia_address') > 0:
			self.dict['HADOOP_GANGLIA_ADDRESS']="%s" % \
				(self.db.getHostAttr(self.host, 'ganglia_address'))

		if self.db.getHostAttr(self.host,'OSG_HadoopSecondaryNode') > 0:
			self.dict['HADOOP_SECONDARY_NAMENODE'] = "%s" % \
				(self.db.getHostAttr(self.host, 'OSG_HadoopSecondaryNode'))

		if self.db.getHostAttr(self.host,'OSG_HadoopCheckPointDirs') > 0:
			self.dict['HADOOP_CHECKPOINT_DIRS']= "%s" % \
				(self.db.getHostAttr(self.host, 'OSG_HadoopCheckPointDirs'))

		if self.db.getHostAttr(self.host,'OSG_HadoopCheckPointPeriod') > 0:
			self.dict['HADOOP_CHECKPOINT_PERIOD']="%s" % \
				(self.db.getHostAttr(self.host, 'OSG_HadoopCheckPointPeriod'))

		if self.db.getHostAttr(self.host,'OSG_HadoopUpdateFstab') > 0:
			self.dict['HADOOP_UPDATE_FSTAB']= "%s" % \
				(self.db.getHostAttr(self.host, 'OSG_HadoopUpdateFstab'))

#	def defineInternalStateVars(self):
#		self.user = "hdfs"
#		self.cm_fqdn = self.db.getHostAttr('localhost', 'OSG_Condor_Master')
#		self.cm_domainName = self.cm_fqdn[string.find(self.cm_fqdn, '.')+1:]
#		self.localDomain = self.db.getHostAttr('localhost','Kickstart_PrivateDNSDomain')

	def setDefaults(self):
		""" set hadoop location and config files """
		self.user = 'hdfs'
		self.releaseDir = '/usr'
		self.configMain = '/etc/condor/condor_config'
		self.configLocal = '/etc/sysconfig/hadoop' 

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

	def Config(self):
		""" configuration driver """
		self.setDefaults()



	def run(self, params, args):

		self.initializeDictionary()
#		self.type, self.UIDdomain, self.ConfigFile = self.fillParams([('type','Worker'),('UIDdomain',),('ConfigFile','/etc/sysconfig/hadoop') ])
		([self.ConfigFile ])= self.fillParams([('ConfigFile','/etc/sysconfig/hadoop') ])
#		self.defineInternalStateVars()
		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			self.fillFromRollDefault()
			self.fillFromRocksAttributes()
			self.Config()
#			self.runPlugins((host,self.dict))
#			self.writeConfigFile(self.dict, self.dictcomment, self.configLocal)
			self.writeConfigFile(self.dict, self.dictcomment, self.dictlines, self.ConfigFile)

		self.endOutput(padChar='')

