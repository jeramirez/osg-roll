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

	Output the OSG worker client wrapper install script

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host osg wnclient install compute-0-0'>
	Create wrapper script to install OSG client for compute-0-0
	</example>

	"""

	def FixGid(self, thegid, thegroup):
		self.addOutput(self.host, 'swapgid=`getent group %s | cut -d: -f3`' % thegroup)
		self.addOutput(self.host, 'swapgroup=`getent group %s | cut -d: -f1`' % thegid)
		self.addOutput(self.host, '[ ! -z "$swapgroup" ]&amp;&amp;[ "x$swapgroup" != "x%s" ]&amp;&amp;/usr/sbin/groupmod -o -g $swapgid $swapgroup' % thegroup)
		self.addOutput(self.host, '/usr/sbin/groupmod -g %s %s' % (thegid,thegroup))

	def FixUid(self, theuid, theuser):
		self.addOutput(self.host, 'swapuid=`getent passwd %s | cut -d: -f3`' % theuser)
		self.addOutput(self.host, 'swapuser=`getent passwd %s | cut -d: -f1`' % theuid)
		self.addOutput(self.host, '[ ! -z "$swapuser" ]&amp;&amp;[ "x$swapuser" != "x%s" ]&amp;&amp;/usr/sbin/usermod -o -u $swapuid $swapuser' % theuser)
		self.addOutput(self.host, '/usr/sbin/usermod -u %s %s' % (theuid,theuser))

	def run(self, params, args):

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			loginstall = '/var/log/wnclient-install.log'
			osg_client = self.db.getHostAttr(host,'OSG_Client')
			startGID   = self.db.getHostAttr(host,'OSG_wn_StartGIDGlexecGroup')
			nGID       = self.db.getHostAttr(host,'OSG_wn_numberGIDsGlexec')

			if not startGID > 0:
				startGID = '65000'
			if not nGID > 0:
				nGID = '50'
			if osg_client > 0 and osg_client == 'true':
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_glexecgid; glexec')
				self.FixGid('&OSG_glexecgid;','glexec')
				self.addOutput(self.host, '')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_gratiagid; gratia')
				self.FixGid('&OSG_glexecgid;','gratia')
				self.addOutput(self.host, '')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_glexecuid; -g &OSG_glexecgid; -c "gLExec user account" -s /sbin/nologin -d /etc/glexec glexec')
				self.FixUid('&OSG_glexecuid;','glexec')
				self.addOutput(self.host, '')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_gratiauid; -g &OSG_gratiagid; -c "gratia runtime user" -s /sbin/nologin -d /etc/gratia gratia')
				self.FixUid('&OSG_gratiauid;','gratia')
				self.addOutput(self.host, '')
				self.addOutput(self.host, '#make sure condor user exist already to avoid different uid/gid for condor')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_condorgid; condor')
				self.FixGid('&OSG_condorgid;','condor')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_condoruid; -g &OSG_condorgid; -c "Condor Daemon Account" -s /bin/nologin -d /var/lib/condor condor')
				self.FixUid('&OSG_condoruid;','condor')
				self.addOutput(self.host, '')
				gid = int(startGID)
				for gindex in range(0,int(nGID)):
					self.addOutput(self.host, '/usr/sbin/groupadd -g %s glexec%2.2d' % (gid,gindex))
					gid += 1
				self.addOutput(self.host, '')
				self.addOutput(self.host, 'touch %s' % loginstall )
				self.addOutput(self.host, 'yum install osg-ca-certs  &gt;&gt; %s 2&gt;&amp;1' % loginstall)
				self.addOutput(self.host, 'yum install osg-wn-client-glexec  &gt;&gt; %s 2&gt;&amp;1' % loginstall)
				self.addOutput(self.host, '')
				self.addOutput(self.host, '#Make sure config templates exists')
				self.addOutput(self.host, '[ ! -d /etc/grid-security/certificates.osg-ca-certs ]&amp;&amp;mv /etc/grid-security/certificates /etc/grid-security/certificates.osg-ca-certs')
				self.addOutput(self.host, '[ ! -f /etc/lcmaps.db.template ]&amp;&amp;cp -p /etc/lcmaps.db /etc/lcmaps.db.template')
				self.addOutput(self.host, '')
				self.addOutput(self.host, '#Create links for voms-mapfile and grid-mapfile')
				self.addOutput(self.host, '#        should be needed but useful for tests')
				self.addOutput(self.host, '[ ! -f /etc/grid-security/voms-mapfile ]&amp;&amp;ln -s &OSG_CE_Mount_ShareDir;/ce/grid-security/voms-mapfile /etc/grid-security/.')
				self.addOutput(self.host, '[ ! -f /etc/grid-security/grid-mapfile ]&amp;&amp;ln -s &OSG_CE_Mount_ShareDir;/ce/grid-security/grid-mapfile /etc/grid-security/.')
				self.addOutput(self.host, '')

		self.endOutput(padChar='')
