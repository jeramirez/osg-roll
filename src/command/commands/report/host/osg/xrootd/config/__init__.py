#$Id$
# 
# @Copyright@
#
# $Log$
# Revision 0.1  2014/02/13 05:48:54  eduardo
# Initial Version
#

import sys
import os
import pwd
import string
import types
import re
import rocks.commands
from syslog import syslog

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""

	Output the OSG xrootd Local Configuration Script 
	Uses Rocks Attributes: OSG_XRD,
	OSG_XROOTD_LOCAL_REDIRECTOR, OSG_XROOTD_REGIONAL_REDIRECTOR,
	OSG_CMS_LOCAL_SITE, OSG_XROOTD_STORAGE_XML

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /root/XrootdConfigurator
	</param>

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>

	<param type='string' name='ConfigXrootd'>
	Defaults to: /etc/xrootd/xrootd-clustered.cfg
	</param>

	<example cmd='report host osg xrootd config xrootd-0-0 ConfigXrootd="/etc/xrootd/xrootd.cfg.test"'>
	Set the OSG xrootd Configuration File for xrootd-0-0 as /etc/xrootd/xrootd.cfg.test 
	</example>
	"""

	def writeConfigXrootd(self, configFile):
		OSG_Manager        = self.db.getHostAttr(self.host,'OSG_XROOTD_LOCAL_REDIRECTOR')
		OSG_MetaManager    = self.db.getHostAttr(self.host,'OSG_XROOTD_REGIONAL_REDIRECTOR')
		OSG_Site           = self.db.getHostAttr(self.host,'OSG_CMS_LOCAL_SITE')
		OSG_Storagexml     = self.db.getHostAttr(self.host,'OSG_XROOTD_STORAGE_XML')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/xrootd/xrootd-clustered.cfg.template %s' % (configFile))
		if OSG_MetaManager > 0:
			self.addOutput(self.host, 'sed -i -e "s@all.role manager if xrootd.unl.edu@all.role manager if %s@" %s' % (OSG_Manager,configFile))
			self.addOutput(self.host, 'sed -i -e "s@all.manager xrootd.unl.edu:1213@all manager meta all %s 1213 \\nall.manager %s  1213@" %s' % (OSG_MetaManager,OSG_Manager,configFile))
		else:
			self.addOutput(self.host, 'sed -i -e "s@all.role manager if xrootd.unl.edu@#all.role manager if xrootd.unl.edu@" %s' % (configFile))
			self.addOutput(self.host, 'sed -i -e "s@all.manager xrootd.unl.edu:1213@all.manager %s  1213@" %s' % (OSG_Manager,configFile))
		self.addOutput(self.host, 'sed -i -e "s@if exec xrootd@#if exec xrootd@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@xrd.report xrootd.unl.edu:3333 every 300s all@xrd.report     xrootd.t2.ucsd.edu:9931 every 60s all sync@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@xrootd.monitor all flush 5s mbuff 1k window 1s dest files io info user xrootd.unl.edu:3334 dest files io info stage user brian-test.unl.edu:9930@xrootd.monitor all auth flush io 60s ident 5m mbuff 8k rbuff 4k rnums 3 window 10s dest files io info user redir xrootd.t2.ucsd.edu:9930@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@^fi@#fi@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@-crl:3@-crl:3 -authzfun:libXrdLcmaps.so -authzfunparms:--osg,--lcmapscfg,/etc/xrootd/lcmaps.cfg,--loglevel,0 -gmapopt:10 -gmapto:0@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@#oss.namelib@oss.namelib@" %s' % (configFile) )
		self.addOutput(self.host, 'sed -i -e "s@/usr/bin/XrdOlbMonPerf@/usr/share/xrootd/utils/XrdOlbMonPerf@" %s' % (configFile) )
		if OSG_Storagexml >0:
			self.addOutput(self.host, 'sed -i -e "s@/etc/xrootd/storage.xml@%s@" %s' % (OSG_Storagexml,configFile) )
		self.addOutput(self.host, 'echo "all.sitename %s" &gt;&gt; %s' % (OSG_Site,configFile) )
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigLcmaps(self, configFile):
		osg_gums   = self.db.getHostAttr(self.host,'OSG_GumsServer')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/xrootd/lcmaps.cfg.template %s' % (configFile))
		if osg_gums>0:
			self.addOutput(self.host, '#Set Gums')
			self.addOutput(self.host, 'sed -i -e "s#yourgums.yourdomain#%s#" %s' % (osg_gums,configFile) )
		else:
			self.addOutput(self.host, '#Set vomsmap')
			self.addOutput(self.host, 'sed -i -e "s@xrootd_policy:@#xrootd_policy:@" %s' % (configFile) )
			self.addOutput(self.host, 'sed -i -e "s@verifyproxy -&gt; scasclient@#verifyproxy -&gt; scasclient@" %s' % (configFile) )
			self.addOutput(self.host, 'sed -i -e "s@scasclient -&gt; good | bad@#scasclient -&gt; good | bad@" %s' % (configFile) )
			self.addOutput(self.host, 'echo "gridmapfile = \\\"lcmaps_localaccount.mod\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "              \\\"-gridmap /etc/grid-security/grid-mapfile\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "banfile = \\\"lcmaps_ban_dn.mod\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "          \\\"-banmapfile /etc/grid-security/ban-mapfile\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "banvomsfile = \\\"lcmaps_ban_fqan.mod\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "              \\\"-banmapfile /etc/grid-security/ban-voms-mapfile\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "vomsmapfile = \\\"lcmaps_voms_localaccount.mod\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "              \\\"-gridmap /etc/grid-security/voms-mapfile\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "defaultmapfile = \\\"lcmaps_voms_localaccount2.mod\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "                 \\\"-gridmap /usr/share/osg/voms-mapfile-default\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "verifyproxynokey = \\\"lcmaps_verify_proxy2.mod\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "          \\\"--discard_private_key_absence\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "          \\\" -certdir /etc/grid-security/certificates\\\"" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "xrootd_policy:" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "verifyproxynokey -&gt; banfile" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "banfile -&gt; banvomsfile | bad" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "banvomsfile -&gt; gridmapfile | bad" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "gridmapfile -&gt; good | vomsmapfile" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "vomsmapfile -&gt; good | defaultmapfile" &gt;&gt; %s' % (configFile) )
			self.addOutput(self.host, 'echo "defaultmapfile -&gt; good | bad" &gt;&gt; %s' % (configFile) )
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigFetchcrl(self, argv):
		# 1. Get the hostname and the config file to store
		host, addOutput, configs = argv 
		Fetchcrl           = configs['FetchCrl']
		certdir            = configs['Cacert']
		squid              = self.db.getHostAttr(host,'OSG_SquidServer')
		proxy              = self.db.getHostAttr(host,'OSG_CVMFS_HTTP_PROXY')

		addOutput(host, '#begin config %s' % (Fetchcrl))
		addOutput(host, '/bin/rm -f %s' % (Fetchcrl))
		addOutput(host, '/bin/touch -f %s' % (Fetchcrl))
		addOutput(host, 'echo "infodir = %s" &gt;&gt; %s' % (certdir,Fetchcrl))
		if squid>0:
			if ":" in squid:
				addOutput(host, 'echo "http_proxy = http://%s" &gt;&gt; %s' % (squid,Fetchcrl))
			else:
				addOutput(host, 'echo "http_proxy = http://%s:3128" &gt;&gt; %s' % (squid,Fetchcrl))
		elif proxy>0:
			addOutput(host, 'echo "http_proxy = %s" &gt;&gt; %s' % (proxy,Fetchcrl))

		addOutput(host, '#end config %s' % (Fetchcrl))
		addOutput(host, '')

	def run(self, params, args):
		Configs    = {}
		#input parameters keys and default values
		ParmKeys   = [
			('test','n'),
			('ConfigFile','/root/XrootdConfigurator'),
			('ConfigXrootd','/etc/xrootd/xrootd-clustered.cfg'),
			('ConfigCacert','/etc/grid-security/certificates'),
			('ConfigFetchCrl','/etc/fetch-crl.d/osg_roll_xrd.conf'),
			('ConfigLcmaps','/etc/xrootd/lcmaps.cfg')
		]

		#get running values (in case updated at cmd)
		ParmValues = self.fillParams(ParmKeys)

		#fill up Configs variables (will be passed to plugins)
		nparm=0
		for ParmKey in ParmKeys:
			name = ParmKey[0]
			parmvalue = ParmValues[nparm]
			if name == 'test' or name == 'ConfigFile':
				Configs[name]=parmvalue
			else :
				Configs[name[6:]]=parmvalue
			nparm+=1

		#in case of testing add '_test' to config files output
		istest = self.str2bool(Configs['test'])
		if istest:
			for config in Configs.items():
				key=config[0]
				if key != 'test' and key != 'ConfigFile':
					Configs[key]=Configs[key]+'_test'

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host     = host
			self.IsXrootd = self.db.getHostAttr(self.host,'OSG_XRD')

			if self.IsXrootd:
				self.addOutput(self.host, '<file name="%s" perms="755" >' % (Configs['ConfigFile']))
				self.addOutput(self.host, '#!/bin/bash')
				self.addOutput(self.host, '')
				self.writeConfigXrootd(Configs['Xrootd'])
				self.writeConfigLcmaps(Configs['Lcmaps'])
				self.writeConfigFetchcrl((host,self.addOutput,Configs))
				self.addOutput(self.host, '</file>')

		self.endOutput(padChar='')

