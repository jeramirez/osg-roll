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

	Output the OSG Bestman Loca 
	Uses Rocks Attributes: OSG_SE, OSG_GumsServer,
	OSG_SRMlocalPathListAllowed, OSG_SRMsupportedProtocolList, OSG_SRMusepluging,
	OSG_GlobusTcpSourceRange, OSG_GlobusTcpPortRange

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /root/BestmanConfigurator
	</param>

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>

	<param type='string' name='ConfigRCFile'>
	Defaults to: /etc/bestman2/conf/bestman2.rc
	</param>

	<param type='string' name='ConfigSysconfig'>
	Defaults to: /etc/sysconfig/bestman2
	</param>

	<example cmd='report host osg bestman config se-0-0 ConfigRCFile="/etc/bestman2/conf/bestman2.rc.test"'>
	Set the OSG RC Configuration File for se-0-0 as /etc/bestman2/conf/bestman2.rc.test 
	</example>
	"""

	def writeBestman2RC(self, configFile):
		OSG_GumsServer           = self.db.getHostAttr(self.host,'OSG_GumsServer')
		localpathallowed         = self.db.getHostAttr(self.host,'OSG_SRMlocalPathListAllowed')
		supportedprotocol        = self.db.getHostAttr(self.host,'OSG_SRMsupportedProtocolList')
		useplugin                = self.db.getHostAttr(self.host,'OSG_SRMusepluging')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/bestman2/conf/bestman2.rc.template %s' % (configFile))
		if localpathallowed > 0:
			self.addOutput(self.host, 'sed -i -e "s@### localPathListAllowed=@localPathListAllowed=%s@" %s' % (localpathallowed,configFile))
		if supportedprotocol > 0:
			self.addOutput(self.host, 'sed -i -e "s@### supportedProtocolList=@supportedProtocolList=%s@" %s' % (supportedprotocol,configFile))
		if OSG_GumsServer > 0:
			self.addOutput(self.host, 'sed -i -e "s@### GUMSProtocol=XACML@GUMSProtocol=XACML@" %s' % (configFile))
			self.addOutput(self.host, 'sed -i -e "s@### GUMSserviceURL=@GUMSserviceURL=https://%s:8443/gums/services/GUMSXACMLAuthorizationServicePort@" %s' % (OSG_GumsServer,configFile))
		if useplugin > 0 and useplugin:
			self.addOutput(self.host, 'sed -i -e "s@### pluginLib=/usr/share@pluginLib=/usr/share@" %s' % (configFile))
			self.addOutput(self.host, 'sed -i -e "s@### protocolSelectionPolicy=PROTOCOL_POLICY@protocolSelectionPolicy=class=plugin.RoundRobinWithPath\&amp;jarFile=RRWP.jar\&amp;name=gsiftp\&amp;param=/usr/share/java/bestman2/plugin/gsiftp.servers.txt@" %s' % (configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeSysConfig(self, configFile):
		OSG_GumsServer          = self.db.getHostAttr(self.host,'OSG_GumsServer')
		tcpportrange            = self.db.getHostAttr(self.host,'OSG_GlobusTcpPortRange')
		tcpsourcerange          = self.db.getHostAttr(self.host,'OSG_GlobusTcpSourceRange')
		useplugin               = self.db.getHostAttr(self.host,'OSG_SRMusepluging')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/sysconfig/bestman2.template %s' % (configFile))
		if tcpportrange > 0:
			self.addOutput(self.host, 'sed -i -e "s@# GLOBUS_TCP_PORT_RANGE=@GLOBUS_TCP_PORT_RANGE=%s@" %s' % (tcpportrange,configFile))
		if tcpsourcerange > 0:
			self.addOutput(self.host, 'sed -i -e "s@# GLOBUS_TCP_SOURCE_RANGE=@GLOBUS_TCP_SOURCE_RANGE=%s@" %s' % (tcpsourcerange,configFile))
		if useplugin > 0 and useplugin:
			self.addOutput(self.host, 'sed -i -e "s@# BESTMAN_PLUGIN=@BESTMAN_PLUGIN=/usr/share/java/bestman2/plugin/RRWP.jar@" %s' % (configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def run(self, params, args):

		test, ConfigFile, ConfigRCFile, ConfigSysconfig = self.fillParams([
				('test','n'),
				('ConfigFile','/root/BestmanConfigurator'),
				('ConfigRCFile','/etc/bestman2/conf/bestman2.rc'),
				('ConfigSysconfig','/etc/sysconfig/bestman2')
			])

		istest = self.str2bool(test)
		if istest:
			ConfigRCFile      = ConfigRCFile + '_test'
			ConfigSysconfig   = ConfigSysconfig + '_test'
		self.beginOutput()

                for host in self.getHostnames(args):
			self.host      = host
			self.IsBestman = self.db.getHostAttr(self.host,'OSG_SE')

			if self.IsBestman>0 and self.IsBestman:
				self.addOutput(self.host, '<file name="%s" perms="755" >' % (ConfigFile))
				self.addOutput(self.host, '#!/bin/bash')
				self.addOutput(self.host, '')
				self.writeBestman2RC(ConfigRCFile)
				self.writeSysConfig(ConfigSysconfig)
				self.addOutput(self.host, '</file>')

		self.endOutput(padChar='')

