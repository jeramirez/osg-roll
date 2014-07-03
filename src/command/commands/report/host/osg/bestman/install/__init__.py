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

	Output the OSG bestman wrapper install script

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host osg bestman install se-0-0'>
	Create wrapper script to install OSG SE (bestman) for se-0-0
	</example>

	"""

	def run(self, params, args):

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			osg_se     = self.db.getHostAttr(host,'OSG_SE')
			osg_gums   = self.db.getHostAttr(host,'OSG_GumsServer')
			if osg_se > 0 and osg_se == 'true':
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_bestmangid; bestman')
				self.addOutput(self.host, '/usr/sbin/useradd -u &OSG_bestmanuid; -g &OSG_bestmangid; -c "Bestman 2 Server user" -s /bin/nologin -d /etc/bestman2 bestman')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_gratiagid; gratia')
				self.addOutput(self.host, '/usr/sbin/useradd -u &OSG_gratiauid; -g &OSG_gratiagid; -c "gratia runtime user" -s /sbin/nologin -d /etc/gratia gratia')
				self.addOutput(self.host, 'touch /var/log/se-install.log')
				self.addOutput(self.host, 'yum install osg-ca-certs  &gt;&gt; /var/log/se-install.log 2&gt;&amp;1')
				self.addOutput(self.host, 'yum install bestman2-server &gt;&gt; /var/log/se-install.log 2&gt;&amp;1')
				self.addOutput(self.host, '')
				self.addOutput(self.host, '#Make sure config templates exists')
				self.addOutput(self.host, '[ ! -f /etc/bestman2/conf/bestman2.rc.template ]&amp;&amp;cp -p /etc/bestman2/conf/bestman2.rc /etc/bestman2/conf/bestman2.rc.template')
				self.addOutput(self.host, '[ ! -f /etc/sysconfig/bestman2.template ]&amp;&amp;cp -p /etc/sysconfig/bestman2 /etc/sysconfig/bestman2.template')
				self.addOutput(self.host, '')
				if osg_gums > 0:
					self.addOutput(self.host, '#Set Gums Client')
					self.addOutput(self.host, 'sed -i -e "s#yourgums.yourdomain#%s#" /etc/lcmaps.db' % osg_gums )
					self.addOutput(self.host, 'sed -i -e "s@localhost@%s@" /etc/gums/gums-client.properties' % osg_gums )
					self.addOutput(self.host, 'sed -i -e "s@# globus_mapping@globus_mapping@" /etc/grid-security/gsi-authz.conf' )
					self.addOutput(self.host, '')

		self.endOutput(padChar='')
