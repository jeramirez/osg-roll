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

	Output the OSG CE Local Configuration Script 
	Uses Rocks Attributes: OSG_CE, OSG_CEServer, OSG_SEServer, OSG_SquidServer, OSG_GumsServer,
	OSG_GlobusTcpSourceRange, OSG_GlobusTcpPortRange,
	OSG_CE_Mount_ShareDir, OSG_CE_DataDir, OSG_WN_TmpDir,
	OSG_GFTPServer, Info_ClusterName,
	OSG_CE_gip_multicluster, OSG_CE_gip_NmultiSE,
	OSG_CE_gip_SubCluster1,OSG_CE_gip_ClusterName1,OSG_CE_gip_NumberOfNodes1,OSG_CE_gip_mb_of_Ram1,OSG_CE_gip_cpu_model1,OSG_CE_gip_cpu_vendor1,
	OSG_CE_gip_cpu_speed1,OSG_CE_gip_arch1,OSG_CE_gip_CpusPerNode1,OSG_CE_gip_CoresPerNode1,
	OSG_CE_gip_inbound1,OSG_CE_gip_outbound1,
	OSG_CE_gip_SE1,OSG_CE_gip_SE_OIM_Name1,OSG_CE_gip_SEServer1,
	OSG_CE_gip_SEprovider1,OSG_CE_gip_SEimplementation1,OSG_CE_gip_SEversion1,OSG_CE_gip_SEpath1,OSG_CE_gip_SE_use_df,
	OSG_CE_siteinfo_group, OSG_CE_siteinfo_OIM_name, OSG_CE_siteinfo_OIM_group,
	OSG_CE_siteinfo_sponsor, OSG_CE_siteinfo_policy, OSG_CE_siteinfo_contact,
	OSG_CE_siteinfo_email, OSG_CE_siteinfo_city, OSG_CE_siteinfo_country, 
	OSG_CE_siteinfo_longitude, OSG_CE_siteinfo_latitude, Info_ClusterLatlong

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /root/CE_ini_filesConfigurator
	</param>

	<param type="bool" name="test">
	If want to test output set this parameter.
	Default is no.
	</param>

	<param type='string' name='ConfigLcmaps'>
	Defaults to: /etc/lcmaps.db
	</param>

	<param type='string' name='ConfigSquid'>
	Defaults to: /etc/osg/config.d/01-squid.ini
	</param>

	<param type='string' name='ConfigMisc'>
	Defaults to: /etc/osg/config.d/10-misc.ini
	</param>

	<param type='string' name='ConfigStorage'>
	Defaults to: /etc/osg/config.d/10-storage.ini
	</param>

	<param type='string' name='ConfigManagedFork'>
	Defaults to: /etc/osg/config.d/15-managedfork.ini
	</param>

	<param type='string' name='ConfigBosco'>
	Defaults to: /etc/osg/config.d/20-bosco.ini
	</param>

	<param type='string' name='ConfigCondor'>
	Defaults to: /etc/osg/config.d/20-condor.ini
	</param>

	<param type='string' name='ConfigPBS'>
	Defaults to: /etc/osg/config.d/20-pbs.ini
	</param>

	<param type='string' name='ConfigSGE'>
	Defaults to: /etc/osg/config.d/20-sge.ini
	</param>

	<param type='string' name='ConfigSlurm'>
	Defaults to: /etc/osg/config.d/20-slurm.ini
	</param>

	<param type='string' name='ConfigGip'>
	Defaults to: /etc/osg/config.d/30-gip.ini
	</param>

	<param type='string' name='ConfigNetwork'>
	Defaults to: /etc/osg/config.d/40-network.ini
	</param>

	<param type='string' name='ConfigSiteInfo'>
	Defaults to: /etc/osg/config.d/40-siteinfo.ini
	</param>

	<example cmd='report host osg CE config ce-0-0 ConfigGip="/etc/osg/config.d/30-gip.ini.test"'>
	Set the OSG Gip Configuration File for ce-0-0 as /etc/osg/config.d/30-gip.ini.test 
	</example>
	"""

	def CountComputeNodes(self):
		###Output is number of compute nodes 
		###will be passed to plugins.
		nodes=self.command('list.host')
		count=start=0
		for line in nodes.split('\n'):
			start=line.find('compute',start)+1
			if start>0:
				count+=1
		if count == 0:
			count=1
		return count

	def run(self, params, args):

		Configs    = {}
		#input parameters keys and default values
		ParmKeys   = [
				('test','n'),
				('ConfigFile','/root/CE_ini_filesConfigurator'),
				('ConfigLcmaps','/etc/lcmaps.db'),
				('ConfigFetchCrl','/etc/fetch-crl.d/osg_roll.conf'),
				('ConfigSquid','/etc/osg/config.d/01-squid.ini'),
				('ConfigMisc','/etc/osg/config.d/10-misc.ini'),
				('ConfigGateway','/etc/osg/config.d/10-gateway.ini'),
				('ConfigStorage','/etc/osg/config.d/10-storage.ini'),
				('ConfigManagedFork','/etc/osg/config.d/15-managedfork.ini'),
				('ConfigPBS','/etc/osg/config.d/20-pbs.ini'), 
				('ConfigSGE','/etc/osg/config.d/20-sge.ini'), 
				('ConfigSlurm','/etc/osg/config.d/20-slurm.ini'), 
				('ConfigBosco','/etc/osg/config.d/20-bosco.ini'), 
				('ConfigCondor','/etc/osg/config.d/20-condor.ini'), 
				('ConfigGip','/etc/osg/config.d/30-gip.ini'),
				('ConfigNetwork','/etc/osg/config.d/40-network.ini'),
				('ConfigSiteInfo','/etc/osg/config.d/40-siteinfo.ini')
			]
		#get running values
		ParmValues = self.fillParams(ParmKeys)

		#fill up Configs variables (will be passed to plugins)
		nparm=0
		for ParmKey in ParmKeys:
			name = ParmKey[0]
			if name == 'test' or name == 'ConfigFile':
				Configs[name]=ParmValues[nparm]
			else :
				Configs[name[6:]]=ParmValues[nparm]
			nparm+=1

		#in case of testing add '_test' to config files output
		istest = self.str2bool(Configs['test'])
		if istest:
			for config in Configs.items():
				key=config[0]
				if key != 'test' and key != 'ConfigFile':
					Configs[key]=Configs[key]+'_test'

		Configs['nodes']        = self.CountComputeNodes() #helper for 'Gip' plugin

		self.beginOutput()

		for host in self.getHostnames(args):
			if self.db.getHostAttr(host,'OSG_CE') > 0:
				self.addOutput(host, '<file name="%s" perms="755" >' % (Configs['ConfigFile']))
				self.addOutput(host, '#!/bin/bash')
				self.addOutput(host, '')
				self.runPlugins((host,self.addOutput,Configs))
				self.addOutput(host, '</file>')

		self.endOutput(padChar='')

