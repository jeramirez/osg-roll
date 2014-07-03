# $Id$
# 
# @Copyright@
#
# $Log$
# Revision 0.0  2012/11/09 05:48:55  eduardo
# Copyright Storm for Mamba
#

import os
import time
import rocks.commands
import threading

max_threading = 512
timeout = 30.0

class Parallel(threading.Thread):
	def __init__(self, cmd):
		threading.Thread.__init__(self)
		self.cmd = cmd

	def run(self):
		os.system(self.cmd)


class Command(rocks.commands.sync.host.command):
	"""
	Install Bestman on the named hosts.

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>


	<example cmd='sync host osg bestman install se-0-0'>
	add bestman user, add bestman group, add gratia group and install osg-ce-certs and bestman-server rpms
        on host se-0-0 if attr OSG_SE is set on host.
	</example>

	<example cmd='sync host osg bestman install se-0-0 test=yes'>
	Show the bash script that will run to install bestman-server on host se-0-0
	</example>
	"""

	def run(self, params, args):
		hosts = self.getHostnames(args, managed_only=1)
		istest, = self.fillParams([ ('test', 'n') ])
		istest = self.str2bool(istest)

		threads = []
		for host in hosts:
			if max_threading > 0:
				while threading.activeCount() > max_threading:
					#
					# need to wait for some threads to
					# complete before starting any new ones
					#
					time.sleep(0.001)

			#
			# get the attributes for the host
			#
			attrs     = self.db.getHostAttrs(host)
			is_bestman= self.db.getHostAttr(host,'OSG_SE')
			portrange = self.db.getHostAttr(host,'OSG_GlobusPortRange')
			sourcerange = self.db.getHostAttr(host,'OSG_GlobusSourceRange')
			cmd = '/opt/rocks/bin/rocks report host osg bestman install '
			cmd += '%s | ' % host
			cmd += '/opt/rocks/bin/rocks report script '

			if istest:
				cmd += 'attrs="%s" ' % attrs
				cmd += ';echo " | ssh %s bash" ' % host
				if is_bestman>0 :
					cmd += ';echo " [OSG_SE =%s] will run on host %s" ' % (is_bestman,host)
				else:
					cmd += ';echo " OSG_SE not set on host %s, will not run" ' % host
			else:
				cmd += 'attrs="%s" | ' % attrs
				cmd += 'ssh %s bash > /dev/null 2>&1 ' % host

			if is_bestman>0:
				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks add firewall host=%s rulename=A20-GLOBUS-TCP-PORT-RANGE network=public service="%s" protocol="tcp" action="ACCEPT" chain="INPUT" flags="-m state --state NEW"' % (host,portrange)

				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks add firewall host=%s rulename=A20-GLOBUS-UDP-PORT-RANGE network=public service="%s" protocol="udp" action="ACCEPT" chain="INPUT" flags="-m state --state NEW"' % (host,portrange)

				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks add firewall host=%s rulename=A20-BESTMAN-SECURE-TCP-PORT network=public service=8443 protocol="tcp" action="ACCEPT" chain="INPUT" flags="-m state --state NEW"' % host

				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks add firewall host=%s rulename=A20-BESTMAN-SECURE-UDP-PORT network=public service=8443 protocol="udp" action="ACCEPT" chain="INPUT" flags="-m state --state NEW"' % host

				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks add firewall host=%s rulename=A20-BESTMAN-TCP-PORT network=public service=8080 protocol="tcp" action="ACCEPT" chain="INPUT" flags="-m state --state NEW"' % host

				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks add firewall host=%s rulename=A20-BESTMAN-UDP-PORT network=public service=8080 protocol="udp" action="ACCEPT" chain="INPUT" flags="-m state --state NEW"' % host

				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks sync host firewall %s' % host


			if is_bestman or istest:
				p = Parallel(cmd)
				threads.append(p)
				p.start()

		#
		# collect the threads
		#
		for thread in threads:
			thread.join(timeout)

		threads = []
