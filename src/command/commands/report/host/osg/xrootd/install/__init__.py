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

	Output the OSG xrootd wrapper install script

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host osg xrootd install xrootd-0-0'>
	Create wrapper script to install OSG xrootd for xrootd-0-0
	</example>

	"""

	def run(self, params, args):

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			osg_xrd    = self.db.getHostAttr(host,'OSG_XRD')
			osg_shareddir = self.db.getHostAttr(host,'OSG_CE_Mount_ShareDir')
			if osg_xrd > 0 and osg_xrd == 'true':
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_xrootdgid; xrootd')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_xrootduid; -g &OSG_xrootdgid; -c "XRootD runtime user" -s /bin/nologin -d /var/spool/xrootd xrootd')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_gratiagid; gratia')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_gratiauid; -g &OSG_gratiagid; -c "gratia runtime user" -s /sbin/nologin -d /etc/gratia gratia')
				self.addOutput(self.host, 'touch /var/log/xrootd-install.log')
				self.addOutput(self.host, 'yum -y install lcmaps  &gt;&gt; /var/log/xrootd-install.log 2&gt;&amp;1')
				self.addOutput(self.host, 'yum -y install vo-client-lcmaps-voms  &gt;&gt; /var/log/xrootd-install.log 2&gt;&amp;1')
				self.addOutput(self.host, 'yum -y install osg-ca-certs  &gt;&gt; /var/log/xrootd-install.log 2&gt;&amp;1')
				self.addOutput(self.host, 'yum -y install cms-xrootd-hdfs &gt;&gt; /var/log/xrootd-install.log 2&gt;&amp;1')
				self.addOutput(self.host, '')
				self.addOutput(self.host, '#Make sure config templates exists')
				self.addOutput(self.host, '[ ! -f /etc/xrootd/xrootd-clustered.cfg.original &amp;&amp; -f /etc/xrootd/xrootd-clustered.cfg ]&amp;&amp;mv /etc/xrootd/xrootd-clustered.cfg /etc/xrootd/xrootd-clustered.cfg.original')
				self.addOutput(self.host, '[ ! -f /etc/xrootd/xrootd-clustered.cfg.template ]&amp;&amp;cp -p /etc/xrootd/xrootd.sample.hdfs.cfg /etc/xrootd/xrootd-clustered.cfg.template')
				self.addOutput(self.host, '[ ! -f /etc/xrootd/lcmaps.cfg.template ]&amp;&amp;cp -p /etc/xrootd/lcmaps.cfg /etc/xrootd/lcmaps.cfg.template')
				self.addOutput(self.host, '[ ! -f /etc/xrootd/Authfile.template ]&amp;&amp;cp -p /etc/xrootd/Authfile /etc/xrootd/Authfile.template')
				self.addOutput(self.host, '[ ! -f /etc/grid-security/gsi-authz.conf.template ]&amp;&amp;cp -p /etc/grid-security/gsi-authz.conf /etc/grid-security/gsi-authz.conf.template')
				self.addOutput(self.host, '')
				self.addOutput(self.host, 'sed -i -e "s@# globus_mapping@globus_mapping@" /etc/grid-security/gsi-authz.conf' )
				self.addOutput(self.host, '')
				if osg_shareddir > 0:
					self.addOutput(self.host, '[ -f /etc/grid-security/voms-mapfile ]||ln -s %s/ce/grid-security/voms-mapfile /etc/grid-security/voms-mapfile' % osg_shareddir )
					self.addOutput(self.host, '[ -f /etc/grid-security/grid-mapfile ]||ln -s %s/ce/grid-security/grid-mapfile /etc/grid-security/grid-mapfile' % osg_shareddir )
					self.addOutput(self.host, '')

		self.endOutput(padChar='')
