#$Id$
# 
# @Copyright@
#
# $Log$
# Revision 0.1  2018/02/19 05:48:54  eduardo
# Initial Version
#

import sys
import os
import pwd
import string
import types
import re
import rocks.commands
from syslog import syslog

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""

	Output the OSG lcmaps Configuration Script
	Uses Rocks Attributes: OSG_Client, OSG_CE, OSG_SE,
	OSG_GRIDFTP,OSG_GFTP_HDFS,
	OSG_GumsServer, OSG_wn_LcmapsCertType

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /root/lcmapsConfigurator
	</param>

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>

	<param type='string' name='ConfigLcmaps'>
	Defaults to: /etc/lcmaps.db
	</param>

	<example cmd='report host osg lcmaps config compute-0-0 ConfigLcmaps="/etc/lcmaps.db.test"'>
	Set the OSG lcmaps Configuration lcmaps.db for compute-0-0 as /etc/lcmaps.db.test
	</example>
	"""

	def run(self, params, args):

		Configs    = {}
		#input parameters keys and default values
		ParmKeys   = [
				('test','n'),
				('ConfigFile','/root/lcmapsConfigurator'),
				('ConfigLcmaps','/etc/lcmaps.db')
			]
		#get running values
		ParmValues = self.fillParams(ParmKeys)

		#fill up Configs variables (will be passed to plugins)
		nparm=0
		for ParmKey in ParmKeys:
			name = ParmKey[0]
			if name == 'test' or name == 'ConfigFile':
				Configs[name]=ParmValues[nparm]
			else :
				Configs[name[6:]]=ParmValues[nparm]
			nparm+=1

		#in case of testing add '_test' to config files output
		istest = self.str2bool(Configs['test'])
		if istest:
			for config in Configs.items():
				key=config[0]
				if key != 'test' and key != 'ConfigFile':
					Configs[key]=Configs[key]+'_test'

		self.beginOutput()

		for host in self.getHostnames(args):
			if (self.db.getHostAttr(host,'OSG_Client') > 0) or \
			(self.db.getHostAttr(host,'OSG_GRIDFTP') > 0) or \
			(self.db.getHostAttr(host,'OSG_GFTP_HDFS') > 0) or \
			(self.db.getHostAttr(host,'OSG_CE') > 0) or \
			(self.db.getHostAttr(host,'OSG_SE') > 0):
					self.addOutput(host, '<file name="%s" perms="755" >' % (Configs['ConfigFile']))
					self.addOutput(host, '#!/bin/bash')
					self.addOutput(host, '')
					self.runPlugins((host,self.addOutput,Configs))
					self.addOutput(host, '</file>')

		self.endOutput(padChar='')

