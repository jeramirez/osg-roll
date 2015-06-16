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

	Output the OSG CE wrapper install script

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host osg CE install ce-0-0'>
	Create wrapper script to install OSG CE for ce-0-0
	</example>

	"""

	def run(self, params, args):

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			osg_ce     = self.db.getHostAttr(host,'OSG_CE')
			osg_gums   = self.db.getHostAttr(host,'OSG_GumsServer')
			osg_export = self.db.getHostAttr(host,'OSG_CE_Export_LocalDir')
			ksphost    = self.db.getHostAttr(host,'Kickstart_PrivateKickstartHost')
			kspn       = self.db.getHostAttr(host,'Kickstart_PrivateNetwork')
			kspm       = self.db.getHostAttr(host,'Kickstart_PrivateNetmask')
			if osg_ce > 0:
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_tomcatgid; tomcat')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_tomcatuid; -g &OSG_tomcatgid; -c "Tomcat" -s /bin/sh -d /usr/share/tomcat&rocks_version_major; tomcat')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_gratiagid; gratia')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_gratiauid; -g &OSG_gratiagid; -c "gratia runtime user" -s /sbin/nologin -d /etc/gratia gratia')
				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_squidgid; squid')
				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_squiduid; -g &OSG_squidgid; -c "squid management user" -s /sbin/nologin -d /etc/squid squid')
				self.addOutput(self.host, 'touch /var/log/ce-install.log')
				self.addOutput(self.host, 'yum install osg-ca-certs  &gt;&gt; /var/log/ce-install.log 2&gt;&amp;1')
				self.addOutput(self.host, 'yum install osg-ce-%s &gt;&gt; /var/log/ce-install.log 2&gt;&amp;1' % (osg_ce))
				self.addOutput(self.host, 'yum install globus-gram-job-manager-managedfork  &gt;&gt; /var/log/ce-install.log 2&gt;&amp;1')
				self.addOutput(self.host, '')
				self.addOutput(self.host, '#Make sure config templates exists')
				self.addOutput(self.host, '[ ! -f /etc/osg/config.d/01-squid.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/01-squid.ini /etc/osg/config.d/01-squid.ini.template')
				self.addOutput(self.host, '[ -f /etc/osg/config.d/10-gateway.ini ]&amp;&amp;[ ! -f /etc/osg/config.d/10-gateway.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/10-gateway.ini /etc/osg/config.d/10-gateway.ini.template')
				self.addOutput(self.host, '[ ! -f /etc/osg/config.d/10-misc.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/10-misc.ini /etc/osg/config.d/10-misc.ini.template')
				self.addOutput(self.host, '[ ! -f /etc/osg/config.d/10-storage.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/10-storage.ini /etc/osg/config.d/10-storage.ini.template')
				self.addOutput(self.host, '[ ! -f /etc/osg/config.d/15-managedfork.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/15-managedfork.ini /etc/osg/config.d/15-managedfork.ini.template')
				self.addOutput(self.host, '[ -f /etc/osg/config.d/20-%s.ini ]&amp;&amp;[ ! -f /etc/osg/config.d/20-%s.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/20-%s.ini /etc/osg/config.d/20-%s.ini.template' % (osg_ce,osg_ce,osg_ce,osg_ce))
				self.addOutput(self.host, '[ ! -f /etc/osg/config.d/30-gip.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/30-gip.ini /etc/osg/config.d/30-gip.ini.template')
				self.addOutput(self.host, '[ ! -f /etc/osg/config.d/40-network.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/40-network.ini /etc/osg/config.d/40-network.ini.template')
				self.addOutput(self.host, '[ ! -f /etc/osg/config.d/40-siteinfo.ini.template ]&amp;&amp;cp -p /etc/osg/config.d/40-siteinfo.ini /etc/osg/config.d/40-siteinfo.ini.template')
				self.addOutput(self.host, '')
				if osg_gums > 0:
					self.addOutput(self.host, '#Set Gums Client')
					self.addOutput(self.host, 'sed -i -e "s#yourgums.yourdomain#%s#" /etc/lcmaps.db' % osg_gums )
					self.addOutput(self.host, 'sed -i -e "s@localhost@%s@" /etc/gums/gums-client.properties' % osg_gums )
					self.addOutput(self.host, 'sed -i -e "s@# globus_mapping@globus_mapping@" /etc/grid-security/gsi-authz.conf' )
					self.addOutput(self.host, '')
				if osg_export > 0:
					self.addOutput(self.host, '# Rocks attr OSG_CE_Export_LocalDir = %s' % osg_export )
					self.addOutput(self.host, '#     means CE LocalDir = %s' % osg_export )
					self.addOutput(self.host, '# create if needed %s/ce/globus/share' % osg_export )
					self.addOutput(self.host, '[ -d %s/ce/globus/share ]||mkdir -p %s/ce/globus/share' % (osg_export,osg_export) )
					self.addOutput(self.host, '[ -d %s/ce/globus/share/certificates ]||mv /etc/grid-security/certificates %s/ce/globus/share/.' % (osg_export,osg_export) )
					self.addOutput(self.host, '[ -d /etc/grid-security/certificates ]||ln -s %s/ce/globus/share/certificates /etc/grid-security/certificates' % osg_export )
					self.addOutput(self.host, '# create if needed %s/app/etc' % osg_export )
					self.addOutput(self.host, '[ -d %s/app/etc ]||mkdir -p %s/app/etc' % (osg_export,osg_export) )
					self.addOutput(self.host, '# create if needed %s/app/cmssoft' % osg_export )
					self.addOutput(self.host, '[ -d %s/app/cmssoft ]||mkdir -p %s/app/cmssoft' % (osg_export,osg_export) )
					self.addOutput(self.host, '# create if needed %s/app/cmssoft/cms' % osg_export )
					self.addOutput(self.host, '[ -e %s/app/cmssoft/cms ]||ln -s /cvmfs/cms.cern.ch %s/app/cmssoft/cms' % (osg_export,osg_export) )
					self.addOutput(self.host, 'chmod 1777 %s/app' % osg_export )
					self.addOutput(self.host, 'chmod 1777 %s/app/etc' % osg_export )
					self.addOutput(self.host, '# if needed add %s/ce to /etc/exports' % osg_export )
					self.addOutput(self.host, '[ "`grep -c %s/ce /etc/exports`" != "0" ]||echo "%s/ce %s(rw,async,no_root_squash) %s/%s(rw,async)" &gt;&gt; /etc/exports ' % (osg_export,osg_export,ksphost,kspn,kspm) )
					self.addOutput(self.host, '# if needed add %s/app to /etc/exports' % osg_export )
					self.addOutput(self.host, '[ "`grep -c %s/app /etc/exports`" != "0" ]||echo "%s/app %s(rw,async,no_root_squash) %s/%s(rw,async)" &gt;&gt; /etc/exports ' % (osg_export,osg_export,ksphost,kspn,kspm) )
				self.addOutput(self.host, '')
				self.addOutput(self.host, 'touch /var/tmp/globus-port-state.log')
				self.addOutput(self.host, 'chmod 666 /var/tmp/globus-port-state.log')
				self.addOutput(self.host, '')

		self.endOutput(padChar='')
