# $Id$
# 
# @Copyright@
#
# $Log$
# Revision 0.1  2018/02/19 05:48:55  eduardo
# Initial revision
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
	Reconfigure OSG lcmaps on the named hosts.

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>

	<example cmd='sync host osg lcmaps compute-0-0'>
	Write and run script /root/lcmapsConfigurator on host compute-0-0
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
			attrs = self.db.getHostAttrs(host)
			cmd = '/opt/rocks/bin/rocks report host osg lcmaps config '
			cmd += '%s | ' % host
			cmd += '/opt/rocks/bin/rocks report script '
			if istest:
				cmd += 'attrs="%s"  ' % attrs
				cmd += '; echo \| ssh %s bash ' % host
			else:
				cmd += 'attrs="%s" | ' % attrs
				cmd += 'ssh %s bash > /dev/null 2>&1 ' % host

			if istest:
				cmd += '; echo \; '
			else:
				cmd += '; '
			cmd += 'ssh %s "/root/lcmapsConfigurator" ' % host
			if not istest:
				cmd += '> /dev/null 2>&1 '

			p = Parallel(cmd)
			threads.append(p)
			p.start()

		#
		# collect the threads
		#
		for thread in threads:
			thread.join(timeout)

		threads = []

