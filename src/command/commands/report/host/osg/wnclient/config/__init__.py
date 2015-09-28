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

	Output the OSG wnclient Configuration Script 
	Uses Rocks Attributes: OSG_Client, OSG_CE_Mount_ShareDir,
	OSG_GumsServer, OSG_wn_Cacert, OSG_wn_LcmapsCertType

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /root/wnclientConfigurator
	</param>

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>

	<param type='string' name='ConfigLcmaps'>
	Defaults to: /etc/lcmaps.db
	</param>

	<param type='string' name='ConfigCacert'>
	Defaults to: /etc/grid-security/certificates
	</param>

	<example cmd='report host osg wnclient config compute-0-0 ConfigLcmaps="/etc/lcmaps.db.test"'>
	Set the OSG wnclient Configuration lcmaps.db for compute-0-0 as /etc/lcmaps.db.test 
	</example>
	"""

	def run(self, params, args):

		Configs    = {}
		#input parameters keys and default values
		ParmKeys   = [
				('test','n'),
				('ConfigFile','/root/wnclientConfigurator'),
				('ConfigCacert','/etc/grid-security/certificates'),
				('ConfigFetchCrl','/etc/fetch-crl.d/osg_roll.conf'),
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
			if self.db.getHostAttr(host,'OSG_Client') > 0:
				self.addOutput(host, '<file name="%s" perms="755" >' % (Configs['ConfigFile']))
				self.addOutput(host, '#!/bin/bash')
				self.addOutput(host, '')
				self.runPlugins((host,self.addOutput,Configs))
				self.addOutput(host, '</file>')

		self.endOutput(padChar='')

