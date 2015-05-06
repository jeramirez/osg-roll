#$Id$
# 
# @Copyright@
#
# $Log$
# Revision 0.1  2015/02/26 05:48:54  eduardo
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

	Output the OSG rsv Local Configuration Script 
	Uses Rocks Attributes: OSG_RSV, OSG_RSV_Port, OSG_RSV_SPort

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /root/rsv_iniConfigurator
	</param>

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>

	<param type='string' name='ConfigRsv'>
	Defaults to: /etc/osg/config.d/30-rsv.ini
	</param>

	<example cmd='report host osg rsv config rsv-0-0 ConfigRsv="/etc/osg/config.d/30-rsv.ini.test"'>
	Set the OSG rsv Configuration ini File for rsv-0-0 as /etc/osg/config.d/30-rsv.ini.test 
	</example>
	"""

	def run(self, params, args):

		Configs    = {}
		#input parameters keys and default values
		ParmKeys   = [
				('test','n'),
				('ConfigFile','/root/rsv_iniConfigurator'),
				('ConfigRsv','/etc/osg/config.d/30-rsv.ini'),
				('Confighttp','/etc/httpd/conf/httpd.conf'),
				('Configssl','/etc/httpd/conf.d/ssl.conf')
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
			if self.db.getHostAttr(host,'OSG_RSV') > 0:
				self.addOutput(host, '<file name="%s" perms="755" >' % (Configs['ConfigFile']))
				self.addOutput(host, '#!/bin/bash')
				self.addOutput(host, '')
				self.runPlugins((host,self.addOutput,Configs))
				self.addOutput(host, '</file>')

		self.endOutput(padChar='')

