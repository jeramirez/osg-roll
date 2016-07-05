#$Id$
# 
# @Copyright@
#
# $Log$
# Revision 0.1  2014/02/13 05:48:54  eduardo
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

	Output the OSG xrootd Local Configuration Script 
	Uses Rocks Attributes: OSG_XRD,
	OSG_XROOTD_LOCAL_REDIRECTOR, OSG_XROOTD_REGIONAL_REDIRECTOR,
	OSG_CMS_LOCAL_SITE, OSG_XROOTD_STORAGE_XML

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /root/XrootdConfigurator
	</param>

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>

	<param type='string' name='ConfigXrootd'>
	Defaults to: /etc/xrootd/xrootd-clustered.cfg
	</param>

	<example cmd='report host osg xrootd config xrootd-0-0 ConfigXrootd="/etc/xrootd/xrootd.cfg.test"'>
	Set the OSG xrootd Configuration File for xrootd-0-0 as /etc/xrootd/xrootd.cfg.test 
	</example>
	"""

	def writeConfigXrootd(self, configFile):
		OSG_Manager        = self.db.getHostAttr(self.host,'OSG_XROOTD_LOCAL_REDIRECTOR')
		OSG_MetaManager    = self.db.getHostAttr(self.host,'OSG_XROOTD_REGIONAL_REDIRECTOR')
		OSG_Site           = self.db.getHostAttr(self.host,'OSG_CMS_LOCAL_SITE')
		OSG_Storagexml     = self.db.getHostAttr(self.host,'OSG_XROOTD_STORAGE_XML')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/xrootd/xrootd-clustered.cfg.template %s' % (configFile))
		if OSG_MetaManager > 0:
			self.addOutput(self.host, 'sed -i -e "s@all.role manager if xrootd.unl.edu@all.role manager if %s@" %s' % (OSG_Manager,configFile))
			self.addOutput(self.host, 'sed -i -e "s@all.manager xrootd.unl.edu:1213@all manager meta all %s 1213 \\nall.manager %s  1213@" %s' % (OSG_MetaManager,OSG_Manager,configFile))
		else:
			self.addOutput(self.host, 'sed -i -e "s@all.role manager if xrootd.unl.edu@#all.role manager if xrootd.unl.edu@" %s' % (configFile))
			self.addOutput(self.host, 'sed -i -e "s@all.manager xrootd.unl.edu:1213@all.manager %s  1213@" %s' % (OSG_Manager,configFile))
		self.addOutput(self.host, 'sed -i -e "s@if exec xrootd@#if exec xrootd@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@xrd.report xrootd.unl.edu:3333 every 300s all@xrd.report     xrootd.t2.ucsd.edu:9931 every 60s all sync@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@xrootd.monitor all flush 5s mbuff 1k window 1s dest files io info user xrootd.unl.edu:3334 dest files io info stage user brian-test.unl.edu:9930@xrootd.monitor all auth flush io 60s ident 5m mbuff 8k rbuff 4k rnums 3 window 10s dest files io info user redir xrootd.t2.ucsd.edu:9930@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@^fi@#fi@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@-crl:3@-crl:3 -authzfun:libXrdLcmaps.so -authzfunparms:--osg,--lcmapscfg,/etc/xrootd/lcmaps.cfg,--loglevel,0|useglobals -gmapopt:10 -gmapto:0@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@#oss.namelib@oss.namelib@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@/usr/bin/XrdOlbMonPerf@/usr/share/xrootd/utils/XrdOlbMonPerf@" %s' % (configFile) )
		if OSG_Storagexml >0:
			self.addOutput(self.host, 'sed -i -e "s@/etc/xrootd/storage.xml@%s@" %s' % (OSG_Storagexml,configFile) )
		self.addOutput(self.host, 'echo "all.sitename %s" &gt;&gt; %s' % (OSG_Site,configFile) )
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def run(self, params, args):

		test, ConfigFile, ConfigXrootd = self.fillParams([
				('test','n'),
				('ConfigFile','/root/XrootdConfigurator'),
				('ConfigXrootd','/etc/xrootd/xrootd-clustered.cfg')
			])

		istest = self.str2bool(test)
		if istest:
			ConfigXrootd      = ConfigXrootd + '_test'
		self.beginOutput()

                for host in self.getHostnames(args):
			self.host     = host
			self.IsXrootd = self.db.getHostAttr(self.host,'OSG_XRD')

			if self.IsXrootd:
				self.addOutput(self.host, '<file name="%s" perms="755" >' % (ConfigFile))
				self.addOutput(self.host, '#!/bin/bash')
				self.addOutput(self.host, '')
				self.writeConfigXrootd(ConfigXrootd)
				self.addOutput(self.host, '</file>')

		self.endOutput(padChar='')

