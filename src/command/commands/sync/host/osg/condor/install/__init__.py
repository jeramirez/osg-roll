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
	Install condor on the named hosts.

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>


	<example cmd='sync host osg condor install node-0-0'>
	add condor user, add condor group, and install condor rpms
        on host node-0-0 if attr OSG_Condor_Client is set on host or OSG_CE is set to 'condor' on host.
	</example>

	<example cmd='sync host osg condor install node-0-0 test=yes'>
	Show the bash script that will run to install condor on host node-0-0
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
			is_condor = self.db.getHostAttr(host,'OSG_Condor_Client')
			is_ce     = self.db.getHostAttr(host,'OSG_CE')
			cmd = '/opt/rocks/bin/rocks report host osg condor install '
			cmd += '%s | ' % host
			cmd += '/opt/rocks/bin/rocks report script '

			if istest:
				cmd += 'attrs="%s" ' % attrs
				cmd += ';echo " | ssh %s bash" ' % host
				if is_condor>0 :
					cmd += ';echo " [OSG_Condor_Client =%s] will run on host %s" ' % (is_condor,host)
				else:
					cmd += ';echo " OSG_Condor_Client NOT set on host %s" ' % host
					if is_ce>0 and is_ce == 'condor':
						cmd += ';echo " [OSG_CE =%s] will run on host %s" ' % (is_ce,host)
					else:
						cmd += ';echo " OSG_CE NOT set on host %s" ' % host
						cmd += ';echo " \twill not run (%s)" ' % host
			else:
				cmd += 'attrs="%s" | ' % attrs
				cmd += 'ssh %s bash > /dev/null 2>&1 ' % host


			if is_condor or is_ce == 'condor' or istest:
				p = Parallel(cmd)
				threads.append(p)
				p.start()

		#
		# collect the threads
		#
		for thread in threads:
			thread.join(timeout)

		threads = []
