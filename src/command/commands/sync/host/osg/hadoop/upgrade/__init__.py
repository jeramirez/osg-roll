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
	Upgrade hadoop to OSG3.2 on the named hosts.

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>


	<example cmd='sync host osg hadoop upgrade node-0-0'>
	add hdfs user, add hadoop group, and install hadoop rpms
        on host node-0-0 if attr OSG_HADOOP is set on host or OSG_CE is set to 'condor' on host.
	</example>

	<example cmd='sync host osg hadoop upgrade node-0-0 test=yes'>
	Show the bash script that will run to install/upgrade hadoop on host node-0-0
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
			osg_client  = self.db.getHostAttr(host,'OSG_Client')
			osg_se      = self.db.getHostAttr(host,'OSG_SE')
			osg_ce      = self.db.getHostAttr(host,'OSG_CE')
			osg_gftp    = self.db.getHostAttr(host,'OSG_GFTP_HDFS')
			osg_hadoop  = self.db.getHostAttr(host,'OSG_HADOOP')
			trigger_install = osg_client or osg_se or osg_gftp or osg_hadoop or osg_ce>0

			cmd = '/opt/rocks/bin/rocks report host osg hadoop upgrade '
			cmd += '%s | ' % host
			cmd += '/opt/rocks/bin/rocks report script '

			if istest:
				cmd += 'attrs="%s" ' % attrs
				cmd += ';echo " | ssh %s bash" ' % host
				cmd += ';echo " [OSG_Client =%s]" ' % (osg_client)
				cmd += ';echo " [OSG_SE =%s]" ' % (osg_se)
				cmd += ';echo " [OSG_CE =%s]" ' % (osg_ce)
				cmd += ';echo " [OSG_GFTP_HDFS =%s]" ' % (osg_gftp)
				if trigger_install :
					cmd += ';echo " [OSG_HADOOP =%s] will run on host %s" ' % (osg_hadoop,host)
				else:
					cmd += ';echo " [OSG_HADOOP =%s] will NOT run on host %s" ' % (osg_hadoop,host)
			else:
				cmd += 'attrs="%s" | ' % attrs
				cmd += 'ssh %s bash > /dev/null 2>&1 ' % host


			if trigger_install or istest:
				p = Parallel(cmd)
				threads.append(p)
				p.start()

		#
		# collect the threads
		#
		for thread in threads:
			thread.join(timeout)

		threads = []
