#$Id$
# 
# @Copyright@
# 
# $Log$
# Revision 0.10  2012/10/26 05:48:54  eduardo
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

	Output the OSG frontier-squid wrapper install script

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host osg squid install squid-0-0'>
	Create wrapper script to install OSG frontier squid for squid-0-0
	</example>

	"""

	def run(self, params, args):

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			loginstall = '/var/log/frontier_squid-install.log'
			osg_squid     = self.db.getHostAttr(host,'OSG_SQUID')
			if osg_squid > 0 and osg_squid == 'true':
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_squidgid; squid')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_squiduid; -g &OSG_squidgid; -c "squid management user" -s /sbin/nologin -d /etc/squid squid')
				self.addOutput(self.host, '')
				self.addOutput(self.host, 'touch %s' % loginstall)
				self.addOutput(self.host, 'yum install frontier-squid  &gt;&gt; %s 2&gt;&amp;1' % loginstall)
				self.addOutput(self.host, '')

		self.endOutput(padChar='')
