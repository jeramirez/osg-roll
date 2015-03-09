#$Id$
# 
# @Copyright@
# 
# $Log$
# Revision 0.10  2015/02/26 05:48:54  eduardo
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

	Output the OSG rsv wrapper install script

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host osg rsv install rsv-0-0'>
	Create wrapper script to install OSG rsv for rsv-0-0
	</example>

	"""

	def run(self, params, args):

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			loginstall = '/var/log/rsv-install.log'
			osg_rsv    = self.db.getHostAttr(host,'OSG_RSV')
			if osg_rsv > 0 and osg_rsv:
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_tomcatgid; tomcat')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_tomcatuid; -g &OSG_tomcatgid; -c "Tomcat" -s /bin/sh -d /usr/share/tomcat&rocks_version_major; tomcat')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_gratiagid; gratia')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_gratiauid; -g &OSG_gratiagid; -c "gratia runtime user" -s /sbin/nologin -d /etc/gratia gratia')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_cndrcrongid; cndrcron')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_cndrcronuid; -g &OSG_cndrcrongid; -c "Condor-cron service" -s /sbin/nologin -d /var/lib/condor-cron cndrcron')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_rsvgid; rsv')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_rsvuid; -g &OSG_rsvgid; -c "RSV monitoring user" -s /bin/bash -d /var/rsv rsv')
				self.addOutput(self.host, 'touch %s' % loginstall )
				self.addOutput(self.host, 'yum install rsv  &gt;&gt; %s 2&gt;&amp;1' % loginstall)
				self.addOutput(self.host, 'yum install mod_ssl  &gt;&gt; %s 2&gt;&amp;1' % loginstall)
				self.addOutput(self.host, '')
				self.addOutput(self.host, '#Make sure config templates exists')
				self.addOutput(self.host, '[ ! -f /etc/httpd/conf/httpd.conf.template ]&amp;&amp;cp -p /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.template')
				self.addOutput(self.host, '[ ! -f /etc/httpd/conf.d/ssl.conf.template ]&amp;&amp;cp -p /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.template')
				self.addOutput(self.host, '')

		self.endOutput(padChar='')
