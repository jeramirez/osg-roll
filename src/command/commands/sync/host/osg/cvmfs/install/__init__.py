# $Id$
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
	Install OSG cvmfs on the named hosts.

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>


	<example cmd='sync host osg cvmfs install compute-0-0'>
	add cvmfs user, add cvmfs group, add fuse group and install cvmfs 
        on host compute-0-0 if attr OSG_CVMFS is set in this host.
	</example>

	<example cmd='sync host osg cvmfs compute-0-0 test=yes'>
	Show the bash script that will run to install cvmfs on host compute-0-0
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
			cmd = '/opt/rocks/bin/rocks report host osg cvmfs install '
			cmd += '%s | ' % host
			cmd += '/opt/rocks/bin/rocks report script '

			is_osg_cvmfs = self.db.getHostAttr(host,'OSG_CVMFS')
			if istest:
				cmd += 'attrs="%s" ' % attrs
				cmd += ';echo " | ssh %s bash" ' % host
				if is_osg_cvmfs == 'true':
					cmd += ';echo " OSG_CVMFS set on %s will run" ' % host
				else:
					cmd += ';echo " OSG_CVMFS not set or false on %s will not run" ' % host
					cmd += ';echo " OSG_CVMFS = %s " ' % is_osg_cvmfs
			else:
				cmd += 'attrs="%s" | ' % attrs
				cmd += 'ssh %s bash > /dev/null 2>&1 ' % host

			if is_osg_cvmfs or istest:
				p = Parallel(cmd)
				threads.append(p)
				p.start()

		#
		# collect the threads
		#
		for thread in threads:
			thread.join(timeout)

		threads = []
