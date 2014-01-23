# $Id: __init__.py,v 1.5 2014/01/09 05:48:26 eduardo Exp $
#
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 0.0  2014/01/09 05:48:26  eduardo
# Copyright Storm for Mamba
#
#

import sys
import socket
import rocks.commands
import string

class Command(rocks.commands.report.host.command):
	"""
	Report the current boot installaction for hosts. 
	For each host supplied on the command line, this command prints 
	the hostname, boot action and installaction for that host. 
	The boot action describes what the host will do the next
	time it is booted. 
	The installaction describes which installaction will be used.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, info about
	all the known hosts is listed.
	</arg>

	<example cmd='report host osg installaction compute-0-0'>
	List the current boot action and installaction for compute-0-0.
	</example>

	<example cmd='report host osg installaction'>
	List the current boot action and installaction for all known hosts.
	</example>
	"""

	def run(self, params, args):

		self.beginOutput()

		for host in self.getHostnames(args):
			boot=self.db.execute("""select b.action from 
				nodes n, boot b where n.id = b.node and
				n.name = '%s' """ % host)
			if boot == 1:			
				bootaction, = self.db.fetchone()
			else:
				bootaction = '------'

			install = self.db.execute("""select installaction from 
				nodes where name = '%s' """ % host)
			
			if install == 1:			
				installaction, = self.db.fetchone()
			else:
				installaction = '----------'
			self.addOutput(host, (bootaction, installaction))
		self.endOutput(header=['host', 'action', 'installaction'])


