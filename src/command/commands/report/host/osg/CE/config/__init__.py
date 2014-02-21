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
 	Uses Rocks Attributes: OSG_CE, OSG_Condor_MasterNetwork, 
        OSG_Condor_ClientNetwork, Kickstart_PrivateDNSDomain

	<arg type='string' name='host'>
	One host name.
	</arg>

	<param type='string' name='ConfigFile'>
	Defaults to: /tmp/Reconfigure_CE_ini_files
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

	def writeConfigMisc(self, configFile):
		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/10-misc.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@glexec_location = UNAVAILABLE@glexec_location = /usr/sbin/glexec@" %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@gums_host = DEFAULT@gums_host = %s@" %s' % (self.OSG_GumsServer,configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigStorage(self, configFile):
		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/10-storage.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@se_available = FALSE@se_available = TRUE@" %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@default_se = UNAVAILABLE@default_se = %s@" %s' % (self.OSG_SEServer,configFile))
		self.addOutput(self.host, 'sed -i -e "s@app_dir = UNAVAILABLE@app_dir = %s/app@" %s' % (self.OSG_CE_nfs,configFile))
		self.addOutput(self.host, 'sed -i -e "s@data_dir = UNAVAILABLE@data_dir = %s@" %s' % (self.OSG_CE_DataDir,configFile))
		self.addOutput(self.host, 'sed -i -e "s@worker_node_temp = UNAVAILABLE@worker_node_temp = %s@" %s' % (self.OSG_WN_TmpDir,configFile))
		self.addOutput(self.host, 'sed -i -e "s@site_read = UNAVAILABLE@site_read = srm://%s:8443/srm/v2/server@" %s' % (self.OSG_SEServer,configFile))
		self.addOutput(self.host, 'sed -i -e "s@write_read = UNAVAILABLE@write_read = srm://%s:8443/srm/v2/server@" %s' % (self.OSG_SEServer,configFile))
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

	def writeConfigGip(self, configFile):
		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, '/bin/cp -f /etc/osg/config.d/30-gip.ini.template %s' % (configFile))
		self.addOutput(self.host, 'sed -i -e "s@batch = DEFAULT@batch = %s@" %s' % (self.CEtype,configFile))
		if self.OSG_GFTPServer > 0:
			self.addOutput(self.host, 'sed -i -e "s@gsiftp_host = DEFAULT@gsiftp_host = %s@" %s' % (self.OSG_GFTPServer,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_GFTPServer not defined for CE server')

#			self.addOutput(self.host, 'sed -i -e "s@;node_count = NUMBER_OF_NODE@node_count = %s@" %s' % (self.OSG_NumberOfNodes,configFile))
#			self.addOutput(self.host, '#attr OSG_NumberOfNodes not defined for CE server using number of compute nodes or 1')
#			self.addOutput(self.host, 'sed -i -e "s@;node_count = NUMBER_OF_NODE@node_count = %s@" %s' % (count,configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;ram_mb = MB_OF_RAM@ram_mb = %s@" %s' % (self.OSG_mb_of_Ram,configFile))
#			self.addOutput(self.host, '#attr OSG_mb_of_Ram not defined for CE server, using RAM from CE')
#			self.addOutput(self.host, "export localmem=`/usr/bin/free -m | awk '/^Mem:/{print $2}'`")
#			self.addOutput(self.host, 'sed -i -e "s@;ram_mb = MB_OF_RAM@ram_mb = $localmem@" %s' % (configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;cpu_model = CPU_MODEL_FROM_/proc/cpuinfo@cpu_model = %s@" %s' % (self.OSG_cpu_model,configFile))
#			self.addOutput(self.host, '#attr OSG_cpu_model not defined for CE server, using cpu model from CE')
#			self.addOutput(self.host, "export localcpuinfo=`cat /proc/cpuinfo | grep model | grep name | tail -1 | cut -d: -f2`")
#			self.addOutput(self.host, 'sed -i -e "s@;cpu_model = CPU_MODEL_FROM_/proc/cpuinfo@cpu_model = $localcpuinfo@" %s' % (configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;cpu_vendor = VENDOR_AMD_OR_INTEL@cpu_vendor = %s@" %s' % (self.OSG_cpu_vendor,configFile))
#			self.addOutput(self.host, '#attr OSG_cpu_vendor not defined for CE server, using cpu vendor from CE')
#			self.addOutput(self.host, "export localcpuvendor=`cat /proc/cpuinfo | grep vendor_id | tail -1 | cut -d: -f2`")
#			self.addOutput(self.host, 'sed -i -e "s@;cpu_vendor = VENDOR_AMD_OR_INTEL@cpu_vendor = $localcpuvendor@" %s' % (configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;cpu_speed_mhz = CLOCK_SPEED_MHZ@cpu_speed_mhz = %s@" %s' % (self.OSG_cpu_speed,configFile))
#			self.addOutput(self.host, '#attr OSG_cpu_speed not defined for CE server, using cpu speed from CE')
#			self.addOutput(self.host, "export localcpuspeed=`cat /proc/cpuinfo | grep MHz| tail -1 | cut -d: -f2 | cut -d. -f1`")
#			self.addOutput(self.host, 'sed -i -e "s@;cpu_speed_mhz = CLOCK_SPEED_MHZ@cpu_speed_mhz = $localcpuspeed@" %s' % (configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;cpu_platform = x86_64_OR_i686@cpu_platform = %s@" %s' % (self.OSG_arch,configFile))
#			self.addOutput(self.host, '#attr OSG_arch not defined for CE server, using arch from roll base')
#			self.addOutput(self.host, 'sed -i -e "s@;cpu_platform = x86_64_OR_i686@cpu_platform = %s@" %s' % (arch,configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;cpus_per_node = #_PHYSICAL_CHIPS_PER_NODE@cpus_per_node = %s@" %s' % (self.OSG_CpusPerNode,configFile))
#			self.addOutput(self.host, '#attr OSG_CpusPerNode not defined for CE server, using cpus from CE')
#			self.addOutput(self.host, "export localcpunode=`cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l`")
#			self.addOutput(self.host, 'sed -i -e "s@;cpus_per_node = #_PHYSICAL_CHIPS_PER_NODE@cpus_per_node = $localcpunode@" %s' % (configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;cores_per_node = #_CORES_PER_NODE@cores_per_node = %s@" %s' % (self.OSG_CoresPerNode,configFile))
#			self.addOutput(self.host, '#attr OSG_CoresPerNode not defined for CE server, using cores from CE')
#			self.addOutput(self.host, 'sed -i -e "s@;cores_per_node = #_CORES_PER_NODE@cores_per_node = %s@" %s' % (temp_cores,configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;inbound_network = FALSE@inbound_network = %s@" %s' % (self.OSG_inbound,configFile))
#			self.addOutput(self.host, '#attr OSG_inbound not defined for CE server')
#			self.addOutput(self.host, 'sed -i -e "s@;outbound_network = TRUE@outbound_network = %s@" %s' % (self.OSG_outbound,configFile))
#			self.addOutput(self.host, '#attr OSG_outbound not defined for CE server')
		if self.OSG_multicluster > 0:
			ncluster = self.OSG_multicluster
		else:
			ncluster = 1

		for iclus in range(1,ncluster+1):
			OSG_cluster     = 'OSG_SubCluster' + str(iclus)
			OSG_name        = 'OSG_ClusterName' + str(iclus)
			OSG_nodes       = 'OSG_NumberOfNodes' + str(iclus)
			OSG_Ram         = 'OSG_mb_of_Ram' + str(iclus)
			OSG_cpu_model   = 'OSG_cpu_model'+ str(iclus)
			OSG_cpu_vendor  = 'OSG_cpu_vendor' + str(iclus)
			OSG_cpu_speed   = 'OSG_cpu_speed' + str(iclus)
			OSG_arch        = 'OSG_arch' + str(iclus)
			OSG_CpusPerNode = 'OSG_CpusPerNode' + str(iclus)
			OSG_CoresPerNode= 'OSG_CoresPerNode' + str(iclus)
			OSG_inbound     = 'OSG_inbound' + str(iclus)
			OSG_outbound    = 'OSG_outbound' + str(iclus)

			if self.OSG_ClusterName[OSG_cluster] > 0:
				self.addOutput(self.host, 'echo "[Subcluster %s]" &gt;&gt; %s' %  (self.OSG_ClusterName[OSG_cluster],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server using attr "Info_ClusterName" + %s' %  (OSG_cluster,iclus))
				self.addOutput(self.host, 'echo "[Subcluster %s_%s]" &gt;&gt; %s' %  (self.Info_ClusterName,iclus,configFile))

			if self.OSG_ClusterName[OSG_name] > 0:
				self.addOutput(self.host, 'echo "name = %s" &gt;&gt; %s' %  (self.OSG_ClusterName[OSG_name],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server using attr "Info_ClusterName" + _CE_%s' %  (OSG_name,iclus))
				self.addOutput(self.host, 'echo "name = %s_CE_%s" &gt;&gt; %s' %  (self.Info_ClusterName,iclus,configFile))

			if self.OSG_ClusterName[OSG_nodes] > 0:
				self.addOutput(self.host, 'echo "node_count = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_nodes],configFile))
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

			if self.OSG_ClusterName[OSG_Ram] > 0:
				self.addOutput(self.host, 'echo "ram_mb = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_Ram],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using RAM from CE' % (OSG_Ram))
				if iclus == 1:
					self.addOutput(self.host, "export localmem=`/usr/bin/free -m | awk '/^Mem:/{print $2}'`")
				self.addOutput(self.host, 'echo "ram_mb = $localmem" &gt;&gt; %s' % (configFile))

			if self.OSG_ClusterName[OSG_cpu_model] > 0:
				self.addOutput(self.host, 'echo "cpu_model = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_cpu_model],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using cpu model from CE' % (OSG_cpu_model))
				if iclus == 1:
					self.addOutput(self.host, "export localcpuinfo=`cat /proc/cpuinfo | grep model | grep name | tail -1 | cut -d: -f2`")
				self.addOutput(self.host, 'echo "cpu_model = $localcpuinfo" &gt;&gt; %s' % (configFile))

			if self.OSG_ClusterName[OSG_cpu_vendor] > 0:
				self.addOutput(self.host, 'echo "cpu_vendor = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_cpu_vendor],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using cpu vendor from CE' % (OSG_cpu_vendor))
				if iclus == 1:
					self.addOutput(self.host, "export localcpuvendor=`cat /proc/cpuinfo | grep vendor_id | tail -1 | cut -d: -f2`")
				self.addOutput(self.host, 'echo "cpu_vendor = $localcpuvendor" &gt;&gt; %s' % (configFile))

			if self.OSG_ClusterName[OSG_cpu_speed] > 0:
				self.addOutput(self.host, 'echo "cpu_speed_mhz = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_cpu_speed],configFile))
			else:
				self.addOutput(self.host, '#attr %s  not defined for CE server, using cpu speed from CE' % (OSG_cpu_speed))
				if iclus == 1:
					self.addOutput(self.host, "export localcpuspeed=`cat /proc/cpuinfo | grep MHz| tail -1 | cut -d: -f2 | cut -d. -f1`")
				self.addOutput(self.host, 'echo "cpu_speed_mhz = $localcpuspeed" &gt;&gt; %s' % (configFile))

			if self.OSG_ClusterName[OSG_arch] > 0:
				self.addOutput(self.host, 'echo "cpu_platform = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_arch],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using arch from roll base' % (OSG_arch))
				self.db.execute("""select arch from rolls where name='base'""")
				arch, = self.db.fetchone()
				self.addOutput(self.host, 'echo "cpu_platform = %s" &gt;&gt; %s' % (arch,configFile))

			if self.OSG_ClusterName[OSG_CpusPerNode] > 0:
				self.addOutput(self.host, 'echo "cpus_per_node = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_CpusPerNode],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using cpus from CE' % (OSG_CpusPerNode))
				if iclus == 1:
					self.addOutput(self.host, "export localcpunode=`cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l`")
				self.addOutput(self.host, 'echo "cpus_per_node = $localcpunode" &gt;&gt; %s' % (configFile))

			if self.OSG_ClusterName[OSG_CoresPerNode] > 0:
				self.addOutput(self.host, 'echo "cores_per_node = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_CoresPerNode],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server, using cores from CE' % (OSG_CoresPerNode))
				self.db.execute("""select n.cpus from nodes n where n.name='%s'""" % self.host)
				temp_cores, =self.db.fetchone()
				self.addOutput(self.host, 'echo "cores_per_node = %s" &gt;&gt; %s' % (temp_cores,configFile))

			if self.OSG_ClusterName[OSG_inbound] > 0:
				self.addOutput(self.host, 'echo "inbound_network = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_inbound],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server' % (OSG_inbound))
				if iclus == 1:
					self.addOutput(self.host, 'echo "inbound_network = FALSE" &gt;&gt; %s' % (configFile))

			if self.OSG_ClusterName[OSG_outbound] > 0:
				self.addOutput(self.host, 'echo "outbound_network = %s" &gt;&gt; %s' % (self.OSG_ClusterName[OSG_outbound],configFile))
			else:
				self.addOutput(self.host, '#attr %s not defined for CE server' % (OSG_outbound))
				if iclus == 1:
					self.addOutput(self.host, 'echo "outbound_network = TRUE" &gt;&gt; %s' % (configFile))

		if self.OSG_NmultiSE > 0:
			nSE = self.OSG_NmultiSE
			for iclus in range(1,nSE+1):
				OSG_SE_cluster       = 'OSG_SE' + str(iclus)
				OSG_SE_OIM_Name      = 'OSG_SE_OIM_Name' + str(iclus)
				OSG_SE_Server        = 'OSG_SEServer' + str(iclus)
				OSG_SE_provider      = 'OSG_SEprovider' + str(iclus)
				OSG_SE_implementation= 'OSG_SEimplementation' + str(iclus)
				OSG_SE_version       = 'OSG_SEversion' + str(iclus)
				OSG_SE_path          = 'OSG_SEpath' + str(iclus)
				OSG_SE_use_df         = 'OSG_SE_use_df' + str(iclus)

				if self.OSG_SEs[OSG_SE_cluster] > 0:
					self.addOutput(self.host, 'echo "[SE %s-1]" &gt;&gt; %s'  % (self.OSG_SEs[OSG_SE_cluster],configFile))
					self.addOutput(self.host, 'echo "enabled = True" &gt;&gt; %s'  % (configFile))
					if self.OSG_SEs[OSG_SE_OIM_Name] >0:
						self.addOutput(self.host, 'echo "name = %s" &gt;&gt; %s'  % (self.OSG_SEs[OSG_SE_OIM_Name],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_OIM_Name))
					if self.OSG_SEs[OSG_SE_Server] > 0:
						self.addOutput(self.host, 'echo "srm_endpoint = httpg://%s:8443/srm/v2/server" &gt;&gt; %s'  % (self.OSG_SEs[OSG_SE_Server],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_Server))
						if iclus == 1:
							self.addOutput(self.host, '#### USING attr OSG_SEServer')
							self.addOutput(self.host, 'echo "srm_endpoint = httpg://%s:8443/srm/v2/server" &gt;&gt; %s'  % (self.OSG_SEServer,configFile))
					if self.OSG_SEs[OSG_SE_provider] > 0:
						self.addOutput(self.host, 'echo "provider_implementation = %s" &gt;&gt; %s'  % (self.OSG_SEs[OSG_SE_provider],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_provider))
						if iclus == 1:
							self.addOutput(self.host, '#### USING provider "bestman"')
							self.addOutput(self.host, 'echo "provider_implementation = bestman" &gt;&gt; %s'  % (configFile))
					if self.OSG_SEs[OSG_SE_implementation] > 0:
						self.addOutput(self.host, 'echo "implementation = %s" &gt;&gt; %s'  % (self.OSG_SEs[OSG_SE_implementation],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_implementation))
						if iclus == 1:
							self.addOutput(self.host, '#### USING implementation "bestman"')
							self.addOutput(self.host, 'echo "implementation = bestman" &gt;&gt; %s'  % (configFile))
					if self.OSG_SEs[OSG_SE_version] > 0:
						self.addOutput(self.host, 'echo "version = %s" &gt;&gt; %s'  % (self.OSG_SEs[OSG_SE_version],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_version))
					if self.OSG_SEs[OSG_SE_path] > 0:
						self.addOutput(self.host, 'echo "default_path  = %s" &gt;&gt; %s'  % (self.OSG_SEs[OSG_SE_path],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_path))
					if self.OSG_SEs[OSG_SE_use_df] > 0:
						self.addOutput(self.host, 'echo "use_df = %s" &gt;&gt; %s'  % (self.OSG_SEs[OSG_SE_use_df],configFile))
					else:
						self.addOutput(self.host, '#attr %s not defined for SE server' % (OSG_SE_use_df))
						if iclus == 1:
							self.addOutput(self.host, '#### USING use_df True"')
							self.addOutput(self.host, 'echo "use_df = True" &gt;&gt; %s'  % (configFile))
				else:
					self.addOutput(self.host, '#attr %s not defined for CE server' % (OSG_SE_cluster))
					self.addOutput(self.host, '#####Set %s to the section name [SE CHANGEME] you need in %s' % (OSG_SE_cluster,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_NmultiSE not defined for CE server')
			self.addOutput(self.host, '#####Set OSG_NmultiSE to the number of SEs you need to configure in %s' % (configFile))

#		if self.OSG_SE_OIM_Name > 0:
#			self.addOutput(self.host, 'sed -i -e "s@;[SE CHANGEME]@[SE %s-1]@" %s' % (self.OSG_SE_OIM_Name,configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;enabled = True@enabled = True@" %s' % (configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;name = SE_CHANGEME@name = %s@" %s' % (self.OSG_SE_OIM_Name,configFile))
#			self.addOutput(self.host, 'sed -i -e "s@;srm_endpoint = httpg://srm.example.com:8443/srm/v2/server@srm_endpoint = httpg://%s:8443/srm/v2/server' % (self.OSG_SEServer,configFile))

#			self.addOutput(self.host, 'echo "[SE %s-1]" &gt;&gt; %s'  % (self.OSG_SE_OIM_Name,configFile))
#			self.addOutput(self.host, 'echo "enabled = True" &gt;&gt; %s'  % (configFile))
#			self.addOutput(self.host, 'echo "name = %s" &gt;&gt; %s'  % (self.OSG_SE_OIM_Name,configFile))
#			self.addOutput(self.host, 'echo "srm_endpoint = httpg://%s:8443/srm/v2/server" &gt;&gt; %s'  % (self.OSG_SEServer,configFile))
#		else:
#			self.addOutput(self.host, '#attr OSG_SE_OIM_Name not defined for CE server')

		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')

	def writeConfigNetwork(self, configFile):
		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, 'cp -f /etc/osg/config.d/40-network.ini.template %s' % (configFile))
		if self.OSG_GlobusTcpSourceRange > 0:
			self.addOutput(self.host, 'sed -i -e "s@source_range = UNAVAILABLE@source_range = %s@" %s' % (self.OSG_GlobusTcpSourceRange,configFile))
		if self.OSG_GlobusTcpPortRange > 0:
			self.addOutput(self.host, 'sed -i -e "s@port_range = UNAVAILABLE@port_range = %s@" %s' % (self.OSG_GlobusTcpPortRange,configFile))
			self.addOutput(self.host, 'sed -i -e "s@port_state_file = UNAVAILABLE@port_state_file = /var/tmp/globus-port-state.log@" %s' % (configFile))
		self.addOutput(self.host, '#end config %s' % (configFile))
		self.addOutput(self.host, '')


	def writeConfigSiteInfo(self, configFile):
		self.addOutput(self.host, '#begin config %s' % (configFile))
		self.addOutput(self.host, 'cp -f /etc/osg/config.d/40-siteinfo.ini.template %s' % (configFile))
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
			self.addOutput(self.host, '#### default is contact = UNAVAILABLE in %s' % (configFile))
		if email > 0:
			self.addOutput(self.host, 'sed -i -e "s/email = UNAVAILABLE/email = %s/" %s' % (email,configFile))
		else:
			self.addOutput(self.host, '#attr OSG_CE_siteinfo_email not defined for CE server')
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
		self.OSG_ClusterName = {}
		if self.db.getHostAttr(self.host,'OSG_CE') > 0:
			self.IsCE= True
			self.CEtype = self.db.getHostAttr(self.host,'OSG_CE')
			self.CEserv = self.db.getHostAttr(self.host,'OSG_CEServer')
			self.OSG_SEServer            = self.db.getHostAttr(self.host,'OSG_SEServer')
			self.OSG_GumsServer          = self.db.getHostAttr(self.host,'OSG_GumsServer')
#storage
			self.OSG_CE_nfs              = self.db.getHostAttr(self.host,'OSG_CE_Mount_ShareDir')
			self.OSG_CE_DataDir          = self.db.getHostAttr(self.host,'OSG_CE_DataDir')
			self.OSG_WN_TmpDir           = self.db.getHostAttr(self.host,'OSG_WN_TmpDir')
#gip
			self.OSG_GFTPServer          = self.db.getHostAttr(self.host,'OSG_GFTPServer')
			self.OSG_multicluster        = self.db.getHostAttr(self.host,'OSG_multicluster')
			if self.OSG_multicluster>0:
				ncluster = self.OSG_multicluster
			else:
				ncluster = 1
			for iclus in range(1,ncluster+1):
				OSG_cluster     = 'OSG_SubCluster' + str(iclus)
				OSG_name        = 'OSG_ClusterName' + str(iclus)
				OSG_nodes       = 'OSG_NumberOfNodes' + str(iclus)
				OSG_Ram         = 'OSG_mb_of_Ram' + str(iclus)
				OSG_cpu_model   = 'OSG_cpu_model'+ str(iclus)
				OSG_cpu_vendor  = 'OSG_cpu_vendor' + str(iclus)
				OSG_cpu_speed   = 'OSG_cpu_speed' + str(iclus)
				OSG_arch        = 'OSG_arch' + str(iclus)
				OSG_CpusPerNode = 'OSG_CpusPerNode' + str(iclus)
				OSG_CoresPerNode= 'OSG_CoresPerNode' + str(iclus)
				OSG_inbound     = 'OSG_inbound' + str(iclus)
				OSG_outbound    = 'OSG_outbound' + str(iclus)
				self.OSG_ClusterName[OSG_cluster]      = self.db.getHostAttr(self.host,OSG_cluster)
				self.OSG_ClusterName[OSG_name]         = self.db.getHostAttr(self.host,OSG_name)
				self.OSG_ClusterName[OSG_nodes]        = self.db.getHostAttr(self.host,OSG_nodes)
				self.OSG_ClusterName[OSG_Ram]          = self.db.getHostAttr(self.host,OSG_Ram)
				self.OSG_ClusterName[OSG_cpu_model]    = self.db.getHostAttr(self.host,OSG_cpu_model)
				self.OSG_ClusterName[OSG_cpu_vendor]   = self.db.getHostAttr(self.host,OSG_cpu_vendor)
				self.OSG_ClusterName[OSG_cpu_speed]    = self.db.getHostAttr(self.host,OSG_cpu_speed)
				self.OSG_ClusterName[OSG_arch]         = self.db.getHostAttr(self.host,OSG_arch)
				self.OSG_ClusterName[OSG_CpusPerNode]  = self.db.getHostAttr(self.host,OSG_CpusPerNode)
				self.OSG_ClusterName[OSG_CoresPerNode] = self.db.getHostAttr(self.host,OSG_CoresPerNode)
				self.OSG_ClusterName[OSG_inbound]      = self.db.getHostAttr(self.host,OSG_inbound)
				self.OSG_ClusterName[OSG_outbound]     = self.db.getHostAttr(self.host,OSG_outbound)
			self.Info_ClusterName        = self.db.getHostAttr(self.host,'Info_ClusterName')
#			self.OSG_NumberOfNodes       = self.db.getHostAttr(self.host,'OSG_NumberOfNodes')
#			self.OSG_mb_of_Ram           = self.db.getHostAttr(self.host,'OSG_mb_of_Ram')
#			self.OSG_cpu_model           = self.db.getHostAttr(self.host,'OSG_cpu_model')
#			self.OSG_cpu_vendor          = self.db.getHostAttr(self.host,'OSG_cpu_vendor')
#			self.OSG_cpu_speed           = self.db.getHostAttr(self.host,'OSG_cpu_speed')
#			self.OSG_arch	             = self.db.getHostAttr(self.host,'OSG_arch')
#			self.OSG_CpusPerNode         = self.db.getHostAttr(self.host,'OSG_CpusPerNode')
#			self.OSG_CoresPerNode        = self.db.getHostAttr(self.host,'OSG_CoresPerNode')
#			self.OSG_inbound             = self.db.getHostAttr(self.host,'OSG_inbound')
#			self.OSG_outbound            = self.db.getHostAttr(self.host,'OSG_outbound')
			self.OSG_NmultiSE            = self.db.getHostAttr(self.host,'OSG_NmultiSE')
			if self.OSG_NmultiSE>0:
				nSE = self.OSG_NmultiSE
				for iclus in range(1,nSE+1):
					OSG_SE_cluster       = 'OSG_SE' + str(iclus)
					OSG_SE_OIM_Name      = 'OSG_SE_OIM_Name' + str(iclus)
					OSG_SE_Server        = 'OSG_SEServer' + str(iclus)
					OSG_SE_provider      = 'OSG_SEprovider' + str(iclus)
					OSG_SE_implementation= 'OSG_SEimplementation' + str(iclus)
					OSG_SE_version       = 'OSG_SEversion' + str(iclus)
					OSG_SE_path          = 'OSG_SEpath' + str(iclus)
					OSG_SE_use_df        = 'OSG_SE_use_df' + str(iclus)
					self.OSG_SEs[OSG_SE_cluster]        = self.db.getHostAttr(self.host,OSG_SE_cluster)
					self.OSG_SEs[OSG_SE_OIM_Name]       = self.db.getHostAttr(self.host,OSG_SE_OIM_Name)
					self.OSG_SEs[OSG_SE_Server]         = self.db.getHostAttr(self.host,OSG_SE_Server)
					self.OSG_SEs[OSG_SE_provider]       = self.db.getHostAttr(self.host,OSG_SE_provider)
					self.OSG_SEs[OSG_SE_implementation] = self.db.getHostAttr(self.host,OSG_SE_implementation)
					self.OSG_SEs[OSG_SE_version]        = self.db.getHostAttr(self.host,OSG_SE_version)
					self.OSG_SEs[OSG_SE_path]           = self.db.getHostAttr(self.host,OSG_SE_path)
					self.OSG_SEs[OSG_SE_use_df]         = self.db.getHostAttr(self.host,OSG_SE_use_df)
#network
			self.OSG_GlobusTcpSourceRange= self.db.getHostAttr(self.host,'OSG_GlobusTcpSourceRange')
			self.OSG_GlobusTcpPortRange  = self.db.getHostAttr(self.host,'OSG_GlobusTcpPortRange')

	def run(self, params, args):

		self.ConfigFile, self.ConfigMisc, self.ConfigStorage, self.ConfigManagedFork, self.ConfigCondor, self.ConfigGip, self.ConfigNetwork, self.ConfigSiteInfo = self.fillParams([
				('ConfigFile','/tmp/Reconfigure_CE_ini_files'),
				('ConfigMisc','/etc/osg/config.d/10-misc.ini'),
				('ConfigStorage','/etc/osg/config.d/10-storage.ini'),
				('ConfigManagedFork','/etc/osg/config.d/15-managedfork.ini'),
				('ConfigCondor','/etc/osg/config.d/20-condor.ini'), 
				('ConfigGip','/etc/osg/config.d/30-gip.ini'),
				('ConfigNetwork','/etc/osg/config.d/40-network.ini'),
				('ConfigSiteInfo','/etc/osg/config.d/40-siteinfo.ini')
			])

		self.beginOutput()

                for host in self.getHostnames(args):
			self.host = host
			self.CheckIsCE()
			if self.IsCE:
				self.addOutput(self.host, '<file name="%s">' % (self.ConfigFile))
				self.addOutput(self.host, '#!/bin/bash')
				self.addOutput(self.host, '')
				self.writeConfigMisc(self.ConfigMisc)
				self.writeConfigStorage(self.ConfigStorage)
				self.writeConfigManagedFork(self.ConfigManagedFork)
				if self.CEtype=="condor":
					self.writeConfigCondor(self.ConfigCondor)
				self.writeConfigGip(self.ConfigGip)
				self.writeConfigNetwork(self.ConfigNetwork)
				self.writeConfigSiteInfo(self.ConfigSiteInfo)
				self.addOutput(self.host, '</file>')

		self.endOutput(padChar='')

