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
	Install OSG Frontier Squid on the named hosts.

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>


	<example cmd='sync host osg squid install squid-0-0'>
	install frontier squid on host squid-0-0 
	if attr OSG_SQUID is set to true in this host.
	</example>

	<example cmd='sync host osg squid install squid-0-0 test=yes'>
	Show the bash script that will run to install frontier squid on host squid-0-0
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
			attrs         = self.db.getHostAttrs(host)
			is_squid      = self.db.getHostAttr(host,'OSG_SQUID')
			squid_network = self.db.getHostAttr(host,'OSG_SQUID_OPEN_NETWORK')

			if not squid_network:
				squid_network = "128.142.0.0/16,188.184.128.0/17,188.185.128.0/17"
			cmd = '/opt/rocks/bin/rocks report host osg squid install '
			cmd += '%s | ' % host
			cmd += '/opt/rocks/bin/rocks report script '

			if istest:
				cmd += 'attrs="%s" ' % attrs
				cmd += ';echo " | ssh %s bash" ' % host
				if is_squid>0 :
					cmd += ';echo " OSG_SQUID  will run on host %s" ' % (host)
				else:
					cmd += ';echo " OSG_SQUID not set on host %s, will not run" ' % host
			else:
				cmd += 'attrs="%s" | ' % attrs
				cmd += 'ssh %s bash > /dev/null 2>&1 ' % host

			if is_squid>0:
				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks add firewall host=%s rulename=A20-SQUID-UDP-PORT network=public service=3401 protocol="udp" action="ACCEPT" chain="INPUT" flags="-m state --state NEW --source %s"' % (host,squid_network)

				if istest:
					cmd += ';echo'
				else:
					cmd += ';'
				cmd +=' /opt/rocks/bin/rocks sync host firewall %s' % host


			if is_squid>0 or istest:
				p = Parallel(cmd)
				threads.append(p)
				p.start()

		#
		# collect the threads
		#
		for thread in threads:
			thread.join(timeout)

		threads = []
