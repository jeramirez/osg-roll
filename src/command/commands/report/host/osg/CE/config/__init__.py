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
	OSG_CE_gip_cpu_speed1,OSG_CE_gip_arch1,OSG_CE_gip_CpusPerNode1,OSG_CE_gip_CoresPerNode1,OSG_CE_gip_CoresPerNode1,
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

	<param type='string' name='ConfigCondor'>
	Defaults to: /etc/osg/config.d/20-condor.ini
	</param>

	<param type='string' name='ConfigSGE'>
	Defaults to: /etc/osg/config.d/20-sge.ini
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

	def writeConfigSquid(self, configFile):
		OSG_SquidServer          = self.db.getHostAttr(self.host,'OSG_SquidServer')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/01-squid.ini.template %s' % (configFile))
		if OSG_SquidServer > 0:
			self.addOutput(self.host, 'sed -i -e "s@location = @location = %s@" %s' % (OSG_SquidServer,configFile))
		else:
			self.addOutput(self.host, 'sed -i -e "s@enabled = True@enabled = False@"' )
			self.addOutput(self.host, 'sed -i -e "s@location = @location = UNAVAILABLE@" %s' % (configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigMisc(self, configFile):
		OSG_GumsServer          = self.db.getHostAttr(self.host,'OSG_GumsServer')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/10-misc.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@glexec_location = UNAVAILABLE@glexec_location = /usr/sbin/glexec@" %s' % (configFile))
		if OSG_GumsServer > 0:
			self.addOutput(self.host, 'sed -i -e "s@gums_host = DEFAULT@gums_host = %s@" %s' % (OSG_GumsServer,configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigStorage(self, configFile):
		OSG_CE_nfs              = self.db.getHostAttr(self.host,'OSG_CE_Mount_ShareDir')
		OSG_CE_DataDir          = self.db.getHostAttr(self.host,'OSG_CE_DataDir')
		OSG_WN_TmpDir           = self.db.getHostAttr(self.host,'OSG_WN_TmpDir')
		OSG_SEServer            = self.db.getHostAttr(self.host,'OSG_SEServer')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/10-storage.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@se_available = FALSE@se_available = TRUE@" %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@default_se = UNAVAILABLE@default_se = %s@" %s' % (OSG_SEServer,configFile))
		self.addOutput(self.host, 'sed -i -e "s@app_dir = UNAVAILABLE@app_dir = %s/app@" %s' % (OSG_CE_nfs,configFile))
		self.addOutput(self.host, 'sed -i -e "s@data_dir = UNAVAILABLE@data_dir = %s@" %s' % (OSG_CE_DataDir,configFile))
		self.addOutput(self.host, 'sed -i -e "s@worker_node_temp = UNAVAILABLE@worker_node_temp = %s@" %s' % (OSG_WN_TmpDir,configFile))
		self.addOutput(self.host, 'sed -i -e "s@site_read = UNAVAILABLE@site_read = srm://%s:8443/srm/v2/server@" %s' % (OSG_SEServer,configFile))
		self.addOutput(self.host, 'sed -i -e "s@site_write = UNAVAILABLE@site_write = srm://%s:8443/srm/v2/server@" %s' % (OSG_SEServer,configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigManagedFork(self, configFile):
		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/15-managedfork.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@enabled = FALSE@enabled = TRUE@" %s' % (configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigCondor(self, configFile):
		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/20-condor.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@enabled = FALSE@enabled = TRUE@" %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@job_contact = host.name/jobmanager-condor@job_contact = %s/jobmanager-condor@" %s' % (self.CEserv, configFile))
		self.addOutput(self.host, 'sed -i -e "s@util_contact = host.name/jobmanager@util_contact = %s/jobmanager@" %s' % (self.CEserv,configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigSGE(self, configFile):
		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/20-sge.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@enabled = FALSE@enabled = TRUE@" %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@job_contact = host.name/jobmanager-sge@job_contact = %s/jobmanager-sge@" %s' % (self.CEserv, configFile))
		self.addOutput(self.host, 'sed -i -e "s@util_contact = host.name/jobmanager@util_contact = %s/jobmanager@" %s' % (self.CEserv,configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigGip(self, configFile):
		OSG_GFTPServer          = self.db.getHostAttr(self.host,'OSG_GFTPServer')
		OSG_multicluster        = self.db.getHostAttr(self.host,'OSG_CE_gip_multicluster')
		Info_ClusterName        = self.db.getHostAttr(self.host,'Info_ClusterName')
		OSG_NmultiSE            = self.db.getHostAttr(self.host,'OSG_CE_gip_NmultiSE')
		OSG_SEServer            = self.db.getHostAttr(self.host,'OSG_SEServer')
		OSG_ClusterName = {}
		OSG_SEs = {}


		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/30-gip.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@batch = DEFAULT@batch = %s@" %s' % (self.CEtype,configFile))

		if OSG_GFTPServer > 0:
			self.addOutput(self.host, 'sed -i -e "s@gsiftp_host = DEFAULT@gsiftp_host = %s@" %s' % (OSG_GFTPServer,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_GFTPServer not defined for CE server')

		if OSG_multicluster > 0:
			ncluster = OSG_multicluster
		else:
			ncluster = 1
			self.addOutput(self.host, '#attr OSG_CE_gip_multicluster not defined for CE server, assuming one cluster')

		for iclus in range(1,ncluster+1):
			OSG_cluster     = 'OSG_CE_gip_SubCluster' + str(iclus)
			OSG_name        = 'OSG_CE_gip_ClusterName' + str(iclus)
			OSG_nodes       = 'OSG_CE_gip_NumberOfNodes' + str(iclus)
			OSG_Ram         = 'OSG_CE_gip_mb_of_Ram' + str(iclus)
			OSG_cpu_model   = 'OSG_CE_gip_cpu_model'+ str(iclus)
			OSG_cpu_vendor  = 'OSG_CE_gip_cpu_vendor' + str(iclus)
			OSG_cpu_speed   = 'OSG_CE_gip_cpu_speed' + str(iclus)
			OSG_arch        = 'OSG_CE_gip_arch' + str(iclus)
			OSG_CpusPerNode = 'OSG_CE_gip_CpusPerNode' + str(iclus)
			OSG_CoresPerNode= 'OSG_CE_gip_CoresPerNode' + str(iclus)
			OSG_inbound     = 'OSG_CE_gip_inbound' + str(iclus)
			OSG_outbound    = 'OSG_CE_gip_outbound' + str(iclus)

			OSG_ClusterName[OSG_cluster]      = self.db.getHostAttr(self.host,OSG_cluster)
			OSG_ClusterName[OSG_name]         = self.db.getHostAttr(self.host,OSG_name)
			OSG_ClusterName[OSG_nodes]        = self.db.getHostAttr(self.host,OSG_nodes)
			OSG_ClusterName[OSG_Ram]          = self.db.getHostAttr(self.host,OSG_Ram)
			OSG_ClusterName[OSG_cpu_model]    = self.db.getHostAttr(self.host,OSG_cpu_model)
			OSG_ClusterName[OSG_cpu_vendor]   = self.db.getHostAttr(self.host,OSG_cpu_vendor)
			OSG_ClusterName[OSG_cpu_speed]    = self.db.getHostAttr(self.host,OSG_cpu_speed)
			OSG_ClusterName[OSG_arch]         = self.db.getHostAttr(self.host,OSG_arch)
			OSG_ClusterName[OSG_CpusPerNode]  = self.db.getHostAttr(self.host,OSG_CpusPerNode)
			OSG_ClusterName[OSG_CoresPerNode] = self.db.getHostAttr(self.host,OSG_CoresPerNode)
			OSG_ClusterName[OSG_inbound]      = self.db.getHostAttr(self.host,OSG_inbound)
			OSG_ClusterName[OSG_outbound]     = self.db.getHostAttr(self.host,OSG_outbound)

			if OSG_ClusterName[OSG_cluster] > 0:
				self.addOutput(self.host, 'echo "[Subcluster %s]" &gt;&gt; %s' %  (OSG_ClusterName[OSG_cluster],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server using attr "Info_ClusterName" + %s' %  (OSG_cluster,iclus))
				self.addOutput(self.host, 'echo "[Subcluster %s_%s]" &gt;&gt; %s' %  (Info_ClusterName,iclus,configFile))

			if OSG_ClusterName[OSG_name] > 0:
				self.addOutput(self.host, 'echo "name = %s" &gt;&gt; %s' %  (OSG_ClusterName[OSG_name],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server using attr "Info_ClusterName" + _CE_%s' %  (OSG_name,iclus))
				self.addOutput(self.host, 'echo "name = %s_CE_%s" &gt;&gt; %s' %  (Info_ClusterName,iclus,configFile))

			if OSG_ClusterName[OSG_nodes] > 0:
				self.addOutput(self.host, 'echo "node_count = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_nodes],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server using number of compute nodes or 1' % (OSG_nodes))
				nodes=self.command('list.host')
				count=start=0
				for line in nodes.split('\n'):
					start=line.find('compute',start)+1
					if start>0:
						count+=1
				if count == 0:
					count=1
				self.addOutput(self.host, 'echo "node_count = %s" &gt;&gt; %s' % (count,configFile))

			if OSG_ClusterName[OSG_Ram] > 0:
				self.addOutput(self.host, 'echo "ram_mb = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_Ram],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using RAM from CE' % (OSG_Ram))
				if iclus == 1:
					self.addOutput(self.host, "export localmem=`/usr/bin/free -m | awk '/^Mem:/{print $2}'`")
				self.addOutput(self.host, 'echo "ram_mb = $localmem" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_cpu_model] > 0:
				self.addOutput(self.host, 'echo "cpu_model = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_cpu_model],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using cpu model from CE' % (OSG_cpu_model))
				if iclus == 1:
					self.addOutput(self.host, "export localcpuinfo=`cat /proc/cpuinfo | grep model | grep name | tail -1 | cut -d: -f2`")
				self.addOutput(self.host, 'echo "cpu_model = $localcpuinfo" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_cpu_vendor] > 0:
				self.addOutput(self.host, 'echo "cpu_vendor = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_cpu_vendor],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using cpu vendor from CE' % (OSG_cpu_vendor))
				if iclus == 1:
					self.addOutput(self.host, "export localcpuvendor=`cat /proc/cpuinfo | grep vendor_id | tail -1 | cut -d: -f2`")
				self.addOutput(self.host, 'echo "cpu_vendor = $localcpuvendor" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_cpu_speed] > 0:
				self.addOutput(self.host, 'echo "cpu_speed_mhz = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_cpu_speed],configFile))
			else:
				self.addOutput(self.host, '#attr %s  not defined for CE server, using cpu speed from CE' % (OSG_cpu_speed))
				if iclus == 1:
					self.addOutput(self.host, "export localcpuspeed=`cat /proc/cpuinfo | grep MHz| tail -1 | cut -d: -f2 | cut -d. -f1`")
				self.addOutput(self.host, 'echo "cpu_speed_mhz = $localcpuspeed" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_arch] > 0:
				self.addOutput(self.host, 'echo "cpu_platform = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_arch],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using arch from roll base' % (OSG_arch))
				self.db.execute("""select arch from rolls where name='base'""")
				arch, = self.db.fetchone()
				self.addOutput(self.host, 'echo "cpu_platform = %s" &gt;&gt; %s' % (arch,configFile))

			if OSG_ClusterName[OSG_CpusPerNode] > 0:
				self.addOutput(self.host, 'echo "cpus_per_node = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_CpusPerNode],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using cpus from CE' % (OSG_CpusPerNode))
				if iclus == 1:
					self.addOutput(self.host, "export localcpunode=`cat /proc/cpuinfo | grep 'processor' | sort | uniq | wc -l`")
				self.addOutput(self.host, 'echo "cpus_per_node = $localcpunode" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_CoresPerNode] > 0:
				self.addOutput(self.host, 'echo "cores_per_node = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_CoresPerNode],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using cores from CE' % (OSG_CoresPerNode))
				self.db.execute("""select n.cpus from nodes n where n.name='%s'""" % self.host)
				temp_cores, =self.db.fetchone()
				self.addOutput(self.host, 'echo "cores_per_node = %s" &gt;&gt; %s' % (temp_cores,configFile))

			if OSG_ClusterName[OSG_inbound] > 0:
				self.addOutput(self.host, 'echo "inbound_network = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_inbound],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server' % (OSG_inbound))
				if iclus == 1:
					self.addOutput(self.host, '#      using inbound_network = FALSE' )
					self.addOutput(self.host, 'echo "inbound_network = FALSE" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_outbound] > 0:
				self.addOutput(self.host, 'echo "outbound_network = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_outbound],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server' % (OSG_outbound))
				if iclus == 1:
					self.addOutput(self.host, '#      using outbound_network = TRUE' )
					self.addOutput(self.host, 'echo "outbound_network = TRUE" &gt;&gt; %s' % (configFile))

		if OSG_NmultiSE > 0:
			nSE = OSG_NmultiSE
			for iclus in range(1,nSE+1):
				OSG_SE_cluster       = 'OSG_CE_gip_SE' + str(iclus)
				OSG_SE_OIM_Name      = 'OSG_CE_gip_SE_OIM_Name' + str(iclus)
				OSG_SE_Server        = 'OSG_CE_gip_SEServer' + str(iclus)
				OSG_SE_provider      = 'OSG_CE_gip_SEprovider' + str(iclus)
				OSG_SE_implementation= 'OSG_CE_gip_SEimplementation' + str(iclus)
				OSG_SE_version       = 'OSG_CE_gip_SEversion' + str(iclus)
				OSG_SE_path          = 'OSG_CE_gip_SEpath' + str(iclus)
				OSG_SE_use_df        = 'OSG_CE_gip_SE_use_df' + str(iclus)

				OSG_SEs[OSG_SE_cluster]        = self.db.getHostAttr(self.host,OSG_SE_cluster)
				OSG_SEs[OSG_SE_OIM_Name]       = self.db.getHostAttr(self.host,OSG_SE_OIM_Name)
				OSG_SEs[OSG_SE_Server]         = self.db.getHostAttr(self.host,OSG_SE_Server)
				OSG_SEs[OSG_SE_provider]       = self.db.getHostAttr(self.host,OSG_SE_provider)
				OSG_SEs[OSG_SE_implementation] = self.db.getHostAttr(self.host,OSG_SE_implementation)
				OSG_SEs[OSG_SE_version]        = self.db.getHostAttr(self.host,OSG_SE_version)
				OSG_SEs[OSG_SE_path]           = self.db.getHostAttr(self.host,OSG_SE_path)
				OSG_SEs[OSG_SE_use_df]         = self.db.getHostAttr(self.host,OSG_SE_use_df)

				if OSG_SEs[OSG_SE_cluster] > 0:
					self.addOutput(self.host, 'echo "[SE %s-1]" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_cluster],configFile))
					self.addOutput(self.host, 'echo "enabled = True" &gt;&gt; %s'  % (configFile))
					if OSG_SEs[OSG_SE_OIM_Name] >0:
						self.addOutput(self.host, 'echo "name = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_OIM_Name],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_OIM_Name))
					if OSG_SEs[OSG_SE_Server] > 0:
						self.addOutput(self.host, 'echo "srm_endpoint = httpg://%s:8443/srm/v2/server" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_Server],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_Server))
						if iclus == 1:
							self.addOutput(self.host, '#### USING attr OSG_SEServer')
							self.addOutput(self.host, 'echo "srm_endpoint = httpg://%s:8443/srm/v2/server" &gt;&gt; %s'  % (OSG_SEServer,configFile))
					if OSG_SEs[OSG_SE_provider] > 0:
						self.addOutput(self.host, 'echo "provider_implementation = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_provider],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_provider))
						if iclus == 1:
							self.addOutput(self.host, '#### USING provider "bestman"')
							self.addOutput(self.host, 'echo "provider_implementation = bestman" &gt;&gt; %s'  % (configFile))
					if OSG_SEs[OSG_SE_implementation] > 0:
						self.addOutput(self.host, 'echo "implementation = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_implementation],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_implementation))
						if iclus == 1:
							self.addOutput(self.host, '#### USING implementation "bestman"')
							self.addOutput(self.host, 'echo "implementation = bestman" &gt;&gt; %s'  % (configFile))
					if OSG_SEs[OSG_SE_version] > 0:
						self.addOutput(self.host, 'echo "version = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_version],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_version))
					if OSG_SEs[OSG_SE_path] > 0:
						self.addOutput(self.host, 'echo "default_path  = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_path],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_path))
					if OSG_SEs[OSG_SE_use_df] > 0:
						self.addOutput(self.host, 'echo "use_df = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_use_df],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_use_df))
						if iclus == 1:
							self.addOutput(self.host, '#### USING use_df True"')
							self.addOutput(self.host, 'echo "use_df = True" &gt;&gt; %s'  % (configFile))
				else:
					self.addOutput(self.host, '#attr %s not defined for CE server' % (OSG_SE_cluster))
					self.addOutput(self.host, '#####Set %s to the section name [SE CHANGEME] you need in %s' % (OSG_SE_cluster,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_gip_NmultiSE not defined for CE server')
			self.addOutput(self.host, '#####Set OSG_CE_gip_NmultiSE to the number of SEs you need to configure in %s' % (configFile))

		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigNetwork(self, configFile):
		OSG_GlobusTcpSourceRange= self.db.getHostAttr(self.host,'OSG_GlobusTcpSourceRange')
		OSG_GlobusTcpPortRange  = self.db.getHostAttr(self.host,'OSG_GlobusTcpPortRange')

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/40-network.ini.template %s' % (configFile))
		if OSG_GlobusTcpSourceRange > 0:
			self.addOutput(self.host, 'sed -i -e "s@source_range = UNAVAILABLE@source_range = %s@" %s' % (OSG_GlobusTcpSourceRange,configFile))
		if OSG_GlobusTcpPortRange > 0:
			self.addOutput(self.host, 'sed -i -e "s@port_range = UNAVAILABLE@port_range = %s@" %s' % (OSG_GlobusTcpPortRange,configFile))
			self.addOutput(self.host, 'sed -i -e "s@port_state_file = UNAVAILABLE@port_state_file = /var/tmp/globus-port-state.log@" %s' % (configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')


	def writeConfigSiteInfo(self, configFile):
		group     = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_group')
		OIM_name  = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_OIM_name')
		OIM_group = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_OIM_group')
		sponsor   = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_sponsor')
		policy    = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_policy')
		contact   = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_contact')
		email     = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_email')
		city      = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_city')
		country   = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_country')
		longitude = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_longitude')
		latitude  = self.db.getHostAttr(self.host,'OSG_CE_siteinfo_latitude')
		latlong   = self.db.getHostAttr(self.host,'Info_ClusterLatlong')
		latitude2,longitude2 = latlong.split(' ',1)

		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/40-siteinfo.ini.template %s' % (configFile))
		if group > 0:
			self.addOutput(self.host, 'sed -i -e "s@group = OSG@group = %s@" %s' % (group,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_group not defined for CE server')
			self.addOutput(self.host, '#### default is group = OSG in %s' % (configFile))
		if self.CEserv > 0:
			self.addOutput(self.host, 'sed -i -e "s@host_name = UNAVAILABLE@host_name = %s@" %s' % (self.CEserv,configFile))
		if OIM_name > 0:
			self.addOutput(self.host, 'sed -i -e "s@resource = UNAVAILABLE@resource = %s@" %s' % (OIM_name,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_OIM_name not defined for CE server')
			self.addOutput(self.host, '#### default is resource = UNAVAILABLE in %s' % (configFile))
		if OIM_group > 0:
			self.addOutput(self.host, 'sed -i -e "s@resource_group = UNAVAILABLE@resource_group = %s@" %s' % (OIM_group,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_OIM_group not defined for CE server')
			self.addOutput(self.host, '#### default is resource_group = UNAVAILABLE in %s' % (configFile))
		if sponsor > 0:
			self.addOutput(self.host, 'sed -i -e "s@sponsor = UNAVAILABLE@sponsor = %s@" %s' % (sponsor,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_sponsor not defined for CE server')
			self.addOutput(self.host, 'echo "attr OSG_CE_siteinfo_sponsor not defined for CE server"')
			self.addOutput(self.host, '#### default is sponsor = UNAVAILABLE in %s' % (configFile))
		if policy > 0:
			self.addOutput(self.host, 'sed -i -e "s@site_policy = UNAVAILABLE@site_policy = %s@" %s' % (policy,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_policy not defined for CE server')
			self.addOutput(self.host, '#### default is site_policy = UNAVAILABLE in %s' % (configFile))
		if contact > 0:
			self.addOutput(self.host, 'sed -i -e "s@contact = UNAVAILABLE@contact = %s@" %s' % (contact,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_contact not defined for CE server')
			self.addOutput(self.host, 'echo "attr OSG_CE_siteinfo_contact not defined for CE server"')
			self.addOutput(self.host, '#### default is contact = UNAVAILABLE in %s' % (configFile))
		if email > 0:
			self.addOutput(self.host, 'sed -i -e "s/email = UNAVAILABLE/email = %s/" %s' % (email,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_email not defined for CE server')
			self.addOutput(self.host, 'echo "attr OSG_CE_siteinfo_email not defined for CE server"')
			self.addOutput(self.host, '#### default is email = UNAVAILABLE in %s' % (configFile))
		if city > 0:
			self.addOutput(self.host, 'sed -i -e "s@city = UNAVAILABLE@city = %s@" %s' % (city,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_city not defined for CE server')
			self.addOutput(self.host, '#### USING attr "Info_CertificateLocality" as city in %s' % (configFile))
			city2      = self.db.getHostAttr(self.host,'Info_CertificateLocality')
			if city2 > 0:
				self.addOutput(self.host, 'sed -i -e "s@city = UNAVAILABLE@city = %s@" %s' % (city2,configFile))
			else:
				self.addOutput(self.host, '####### attr "Info_CertificateLocality" not defined!!!!!')

		if country > 0:
			self.addOutput(self.host, 'sed -i -e "s@country = UNAVAILABLE@country = %s@" %s' % (country,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_country not defined for CE server')
			self.addOutput(self.host, '#### USING attr "Info_CertificateCountry" as country in %s' % (configFile))
			country2      = self.db.getHostAttr(self.host,'Info_CertificateCountry')
			if country2 > 0:
				self.addOutput(self.host, 'sed -i -e "s@country = UNAVAILABLE@country = %s@" %s' % (country2,configFile))
			else:
				self.addOutput(self.host, '####### attr "Info_CertificateCountry" not defined!!!!')

		if longitude > 0:
			self.addOutput(self.host, 'sed -i -e "s@longitude = UNAVAILABLE@longitude = %s@" %s' % (longitude,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_longitude not defined for CE server')
			self.addOutput(self.host, '#### USING attr "Info_ClusterLatlong" to retrive longitude in %s' % (configFile))
			if longitude2 > 0:
				lon2 = longitude2.replace('E','')
				lon2 = lon2.replace('e','')
				lon2 = lon2.replace('w','-')
				lon2 = lon2.replace('W','-')
				self.addOutput(self.host, 'sed -i -e "s@longitude = UNAVAILABLE@longitude = %s@" %s' % (lon2,configFile))
			else:
				self.addOutput(self.host, '####### attr "Info_ClusterLatlong" not defined!!!!')
		if latitude > 0:
			self.addOutput(self.host, 'sed -i -e "s@latitude = UNAVAILABLE@latitude = %s@" %s' % (latitude,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_latitude not defined for CE server')
			self.addOutput(self.host, '#### USING attr "Info_ClusterLatlong" to retrive latitude in %s' % (configFile))
			if latitude2 > 0:
				lat2 = latitude2.replace('N','')
				lat2 = lat2.replace('n','')
				lat2 = lat2.replace('s','-')
				lat2 = lat2.replace('S','-')
				self.addOutput(self.host, 'sed -i -e "s@latitude = UNAVAILABLE@latitude = %s@" %s' % (lat2,configFile))
			else:
				self.addOutput(self.host, '####### attr "Info_ClusterLatlong" not well defined!!!!')

		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def CheckIsCE(self):
		###Make sure OSG_CE attr is defined first
		self.IsCE=None
		if self.db.getHostAttr(self.host,'OSG_CE') > 0:
			self.IsCE= True
			self.CEtype = self.db.getHostAttr(self.host,'OSG_CE')
			self.CEserv = self.db.getHostAttr(self.host,'OSG_CEServer')

	def run(self, params, args):

		test, ConfigFile, ConfigSquid, ConfigMisc, ConfigStorage, ConfigManagedFork, ConfigSGE, ConfigCondor, ConfigGip, ConfigNetwork, ConfigSiteInfo = self.fillParams([
				('test','n'),
				('ConfigFile','/root/CE_ini_filesConfigurator'),
				('ConfigSquid','/etc/osg/config.d/01-squid.ini'),
				('ConfigMisc','/etc/osg/config.d/10-misc.ini'),
				('ConfigStorage','/etc/osg/config.d/10-storage.ini'),
				('ConfigManagedFork','/etc/osg/config.d/15-managedfork.ini'),
				('ConfigSGE','/etc/osg/config.d/20-sge.ini'), 
				('ConfigCondor','/etc/osg/config.d/20-condor.ini'), 
				('ConfigGip','/etc/osg/config.d/30-gip.ini'),
				('ConfigNetwork','/etc/osg/config.d/40-network.ini'),
				('ConfigSiteInfo','/etc/osg/config.d/40-siteinfo.ini')
			])

		istest = self.str2bool(test)
		if istest:
			ConfigSquid       = ConfigSquid + '_test'
			ConfigMisc        = ConfigMisc + '_test'
			ConfigStorage     = ConfigStorage + '_test'
			ConfigManagedFork = ConfigManagedFork  + '_test'
			ConfigSGE         = ConfigSGE + '_test'
			ConfigCondor      = ConfigCondor + '_test'
			ConfigGip         = ConfigGip + '_test'
			ConfigNetwork     = ConfigNetwork + '_test'
			ConfigSiteInfo    = ConfigSiteInfo + '_test'
		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			self.CheckIsCE()
			if self.IsCE:
				self.addOutput(self.host, '<file name="%s" perms="755" >' % (ConfigFile))
				self.addOutput(self.host, '#!/bin/bash')
				self.addOutput(self.host, '')
				self.writeConfigSquid(ConfigSquid)
				self.writeConfigMisc(ConfigMisc)
				self.writeConfigStorage(ConfigStorage)
				self.writeConfigManagedFork(ConfigManagedFork)
				if self.CEtype=="condor":
					self.writeConfigCondor(ConfigCondor)
				if self.CEtype=="sge":
					self.writeConfigSGE(ConfigSGE)
				self.writeConfigGip(ConfigGip)
				self.writeConfigNetwork(ConfigNetwork)
				self.writeConfigSiteInfo(ConfigSiteInfo)
				self.addOutput(self.host, '</file>')

		self.endOutput(padChar='')

