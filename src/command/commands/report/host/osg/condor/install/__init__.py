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

	Output the OSG condor wrapper install script

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host osg condor install node-0-0'>
	Create wrapper script to install OSG condor for node-0-0
	</example>

	"""

	def run(self, params, args):

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			osg_condor  = self.db.getHostAttr(host,'OSG_Condor_Client')
			osg_ce      = self.db.getHostAttr(host,'OSG_CE')
			condorgid   = self.db.getHostAttr(host,'OSG_condorgid')
			condoruid   = self.db.getHostAttr(host,'OSG_condoruid')
			config02    = '/etc/condor/config.d/02_rocks_condor_config.local'

			if (osg_condor > 0 and osg_condor == 'true') or (osg_ce > 0 and osg_ce == 'condor'):
#				self.addOutput(self.host, '/usr/sbin/groupadd -g &OSG_condorgid; condor')
#				self.addOutput(self.host, '/usr/sbin/useradd -r -u &OSG_condoruid; -g &OSG_condorgid; -c "Owner of Condor Daemons" -s /bin/nologin -d /var/lib/condor condor')
				self.addOutput(self.host, 'touch /var/log/condor-install.log')
				self.addOutput(self.host, 'yum -y install condor  &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
				if (condorgid > 0):
					self.addOutput(self.host, 'swapgid=`/usr/bin/getent group condor | cut -d: -f3`')
					self.addOutput(self.host, 'echo swapgid=$swapgid &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
					self.addOutput(self.host, 'swapgroup=`/usr/bin/getent group &OSG_condorgid; | cut -d: -f1`')
					self.addOutput(self.host, 'echo swapgroup=$swapgroup &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
					self.addOutput(self.host, '[ ! -z "$swapgroup" ]&amp;&amp;[ "x$swapgroup" != "xcondor" ]&amp;&amp;/usr/sbin/groupmod -o -g $swapgid $swapgroup')
					self.addOutput(self.host, '[ ! -z "$swapgroup" ]&amp;&amp;[ "x$swapgroup" != "xcondor" ]&amp;&amp;echo "/usr/sbin/groupmod -o -g $swapgid $swapgroup" &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
					self.addOutput(self.host, '[ ! -z "$swapgroup" ]&amp;&amp;[ "x$swapgroup" != "xcondor" ]&amp;&amp;/usr/sbin/groupmod -g &OSG_condorgid; condor')
					self.addOutput(self.host, '[ ! -z "$swapgroup" ]&amp;&amp;[ "x$swapgroup" != "xcondor" ]&amp;&amp;echo "/usr/sbin/groupmod -g &OSG_condorgid; condor" &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
				if (condoruid > 0):
					self.addOutput(self.host, 'swapuid=`/usr/bin/getent passwd condor | cut -d: -f3`')
					self.addOutput(self.host, 'echo swapuid=$swapuid &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
					self.addOutput(self.host, 'swapuser=`/usr/bin/getent passwd &OSG_condoruid; | cut -d: -f1`')
					self.addOutput(self.host, 'echo swapuser=$swapuser &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
					self.addOutput(self.host, '[ ! -z "$swapuser" ]&amp;&amp;[ "x$swapuser" != "xcondor" ]&amp;&amp;/usr/sbin/usermod -o -u $swapuid $swapuser')
					self.addOutput(self.host, '[ ! -z "$swapuser" ]&amp;&amp;[ "x$swapuser" != "xcondor" ]&amp;&amp;echo "/usr/sbin/usermod -o -u $swapuid $swapuser" &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
					self.addOutput(self.host, '[ ! -z "$swapuser" ]&amp;&amp;[ "x$swapuser" != "xcondor" ]&amp;&amp;/usr/sbin/usermod -u &OSG_condoruid; -g &OSG_condorgid;  condor')
					self.addOutput(self.host, '[ ! -z "$swapuser" ]&amp;&amp;[ "x$swapuser" != "xcondor" ]&amp;&amp;echo "/usr/sbin/usermod -u &OSG_condoruid; -g &OSG_condorgid;  condor" &gt;&gt; /var/log/condor-install.log 2&gt;&amp;1')
				self.addOutput(self.host, '')
				if (condoruid > 0 or condorgid > 0):
					self.addOutput(self.host, '#Make sure ownership is fine')
					self.addOutput(self.host, '/bin/chown condor:condor /var/log/condor')
					self.addOutput(self.host, '/bin/chown condor:condor /var/lib/condor')
					self.addOutput(self.host, '/bin/chown condor:condor /var/lib/condor/spool')
					self.addOutput(self.host, '/bin/chown condor:condor /var/lib/condor/execute')
					self.addOutput(self.host, '/bin/chgrp condor /var/lib/condor/oauth_credentials')
				self.addOutput(self.host, '/bin/mkdir -p /var/lib/condor/cred_dir')
				self.addOutput(self.host, '')
#				With large memory footprints, java doesn't start. See
#				http://www.cs.wisc.edu/condor/manual/v6.8/3_14Java_Support.html#sec:java-install
#				for workaround used here (Most likely obsolete JAVA_MAXHEAP_ARGUMENT in condor v9_0)
				self.addOutput(self.host, '#Write Java part:%s (if needed)' % (config02) )
				self.addOutput(self.host, '[ -f %s ] || touch %s' % (config02,config02) )
				self.addOutput(self.host, '[ "`grep -c First %s`" != "0"  ] ||echo "# First set JAVA_MAXHEAP_ARGUMENT to null, to disable the default of max RAM" &gt;&gt; %s' % (config02,config02) )
				self.addOutput(self.host, '[ "`grep -v ^# %s | grep -c JAVA_MAXHEAP_ARGUMENT`" != "0" ]||echo "JAVA_MAXHEAP_ARGUMENT =" &gt;&gt; %s' % (config02,config02) )
				self.addOutput(self.host, '')
				self.addOutput(self.host, '# Now calculate the JAVA_EXTRA_ARGUMENTS for %s (if needed)' % (config02) )
				self.addOutput(self.host, "export localmem=`/usr/bin/free -m | awk '/^Mem:/{print $2}'`" )
				self.addOutput(self.host, 'if [ $localmem -gt 1906 ] ; then' )
				self.addOutput(self.host, '\tlocalmem=1906' )
				self.addOutput(self.host, 'fi' )
				self.addOutput(self.host, '[ "`grep -v ^# %s | grep -c JAVA_EXTRA_ARGUMENTS`" != "0" ] || echo "JAVA_EXTRA_ARGUMENTS = -Xmx${localmem}m" &gt;&gt; %s' % (config02,config02) )
				self.addOutput(self.host, '')

		self.endOutput(padChar='')
