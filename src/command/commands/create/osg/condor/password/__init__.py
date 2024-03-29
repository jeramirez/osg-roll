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
# Revision 1.4  2012/05/06 05:48:53  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:30:55  phil
# Viper Copyright
#
# Revision 1.2  2010/10/22 20:43:55  phil
# Updated to 7.4.4 (released Oct 18, 2010).
# Keep 7.4.3 Tarballs in tree.
# Support pool password creation.
# Adjust graph to properly respect Condor_Client attribute
#
# Revision 1.1  2010/10/22 05:11:50  phil
# A rocks helper function to create a condor pool password.
# Useful of you want password-based security.
#
#

import rocks.commands
import os

class command(rocks.commands.create.command):
	MustBeRoot = 1


class Command(command):
	"""
	Create a pool password for Condor. Requires Condor Credd to be
	up and running. 

	<param type='string' name='keyfile'>
	The filename that will be used to store the password.
	Default: /etc/condor/passwords.d/POOL
	</param>

	<param type='bool' name='add'>
	add the newly created key to the condor credential daemon.
	Default: yes
	</param>
	"""

	def run(self, params, args):
		(keyfile,add)  = self.fillParams([
			('keyfile','/etc/condor/passwords.d/POOL'),
			('add','yes')])

		if self.str2bool(add):
			addit="add"
		else:
			addit=""
		if os.path.exists(keyfile):
			self.abort("the key file '%s' already exists. Please remove first" % keyfile)

		#
		# generate the key using a random string 
		#
		cmd = '/usr/bin/uuidgen -r | '
		cmd += '/usr/sbin/condor_store_cred %s -f %s' % (addit,keyfile)

		status = os.system(cmd)
		if status != 0:
			os.remove(keyfile)

