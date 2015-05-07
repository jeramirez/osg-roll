#import rocks.clusterdb
import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Gip'

#[sorting to] run after 'ManagedFork' plugin 
	def requires(self):
		return ['ManagedFork','Pbs','SGE']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Gip']
		count                    = configs['nodes']

		CEtype                   = self.db.getHostAttr(host,'OSG_CE')
		CEserv                   = self.db.getHostAttr(host,'OSG_CEServer')
		OSG_GFTPServer           = self.db.getHostAttr(host,'OSG_GFTPServer')
		OSG_multicluster         = self.db.getHostAttr(host,'OSG_CE_gip_multicluster')
		Info_ClusterName         = self.db.getHostAttr(host,'Info_ClusterName')
		OSG_NmultiSE             = self.db.getHostAttr(host,'OSG_CE_gip_NmultiSE')
		OSG_SEServer             = self.db.getHostAttr(host,'OSG_SEServer')
		OSG_SRMPort              = self.db.getHostAttr(host,'OSG_SRMPort')
		OSG_ClusterName          = {}
		OSG_SEs                  = {}


		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/30-gip.ini.template %s' % (configFile))
		addOutput(host, 'sed -i -e "s@batch = DEFAULT@batch = %s@" %s' % (CEtype,configFile))

                
		if OSG_GFTPServer > 0:
			addOutput(host, 'sed -i -e "s@gsiftp_host = DEFAULT@gsiftp_host = %s@" %s' % (OSG_GFTPServer,configFile))
		else:
			addOutput(host, '#attr OSG_GFTPServer not defined for CE server')

		if OSG_multicluster > 0:
			ncluster = int(OSG_multicluster)
			if ncluster < 1:
				ncluster = 1
		else:
			ncluster = 1
			addOutput(host, '#attr OSG_CE_gip_multicluster not defined for CE server, assuming one cluster')

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

			OSG_ClusterName[OSG_cluster]      = self.db.getHostAttr(host,OSG_cluster)
			OSG_ClusterName[OSG_name]         = self.db.getHostAttr(host,OSG_name)
			OSG_ClusterName[OSG_nodes]        = self.db.getHostAttr(host,OSG_nodes)
			OSG_ClusterName[OSG_Ram]          = self.db.getHostAttr(host,OSG_Ram)
			OSG_ClusterName[OSG_cpu_model]    = self.db.getHostAttr(host,OSG_cpu_model)
			OSG_ClusterName[OSG_cpu_vendor]   = self.db.getHostAttr(host,OSG_cpu_vendor)
			OSG_ClusterName[OSG_cpu_speed]    = self.db.getHostAttr(host,OSG_cpu_speed)
			OSG_ClusterName[OSG_arch]         = self.db.getHostAttr(host,OSG_arch)
			OSG_ClusterName[OSG_CpusPerNode]  = self.db.getHostAttr(host,OSG_CpusPerNode)
			OSG_ClusterName[OSG_CoresPerNode] = self.db.getHostAttr(host,OSG_CoresPerNode)
			OSG_ClusterName[OSG_inbound]      = self.db.getHostAttr(host,OSG_inbound)
			OSG_ClusterName[OSG_outbound]     = self.db.getHostAttr(host,OSG_outbound)

			if OSG_ClusterName[OSG_cluster] > 0:
				addOutput(host, 'echo "[Subcluster %s]" &gt;&gt; %s' %  (OSG_ClusterName[OSG_cluster],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server using attr "Info_ClusterName" + %s' %  (OSG_cluster,iclus))
				addOutput(host, 'echo "[Subcluster %s_%s]" &gt;&gt; %s' %  (Info_ClusterName,iclus,configFile))

			if OSG_ClusterName[OSG_name] > 0:
				addOutput(host, 'echo "name = %s" &gt;&gt; %s' %  (OSG_ClusterName[OSG_name],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server using attr "Info_ClusterName" + _CE_%s' %  (OSG_name,iclus))
				addOutput(host, 'echo "name = %s_CE_%s" &gt;&gt; %s' %  (Info_ClusterName,iclus,configFile))

			if OSG_ClusterName[OSG_nodes] > 0:
				addOutput(host, 'echo "node_count = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_nodes],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server using number of compute nodes or 1' % (OSG_nodes))
				addOutput(host, 'echo "node_count = %s" &gt;&gt; %s' % (count,configFile))

			if OSG_ClusterName[OSG_Ram] > 0:
				addOutput(host, 'echo "ram_mb = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_Ram],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server, using RAM from CE' % (OSG_Ram))
				if iclus == 1:
					addOutput(host, "export localmem=`/usr/bin/free -m | awk '/^Mem:/{print $2}'`")
				addOutput(host, 'echo "ram_mb = $localmem" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_cpu_model] > 0:
				addOutput(host, 'echo "cpu_model = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_cpu_model],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server, using cpu model from CE' % (OSG_cpu_model))
				if iclus == 1:
					addOutput(host, "export localcpuinfo=`cat /proc/cpuinfo | grep model | grep name | tail -1 | cut -d: -f2`")
				addOutput(host, 'echo "cpu_model = $localcpuinfo" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_cpu_vendor] > 0:
				addOutput(host, 'echo "cpu_vendor = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_cpu_vendor],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server, using cpu vendor from CE' % (OSG_cpu_vendor))
				if iclus == 1:
					addOutput(host, "export localcpuvendor=`cat /proc/cpuinfo | grep vendor_id | tail -1 | cut -d: -f2`")
				addOutput(host, 'echo "cpu_vendor = $localcpuvendor" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_cpu_speed] > 0:
				addOutput(host, 'echo "cpu_speed_mhz = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_cpu_speed],configFile))
			else:
				addOutput(host, '#attr %s  not defined for CE server, using cpu speed from CE' % (OSG_cpu_speed))
				if iclus == 1:
					addOutput(host, "export localcpuspeed=`cat /proc/cpuinfo | grep MHz| tail -1 | cut -d: -f2 | cut -d. -f1`")
				addOutput(host, 'echo "cpu_speed_mhz = $localcpuspeed" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_arch] > 0:
				addOutput(host, 'echo "cpu_platform = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_arch],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server, using arch from roll base' % (OSG_arch))
				self.db.execute("""select arch from rolls where name='base'""")
				arch, = self.db.fetchone()
				addOutput(host, 'echo "cpu_platform = %s" &gt;&gt; %s' % (arch,configFile))

			if OSG_ClusterName[OSG_CpusPerNode] > 0:
				addOutput(host, 'echo "cpus_per_node = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_CpusPerNode],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server, using cpus from CE' % (OSG_CpusPerNode))
				if iclus == 1:
					addOutput(host, "export localcpunode=`cat /proc/cpuinfo | grep 'processor' | sort | uniq | wc -l`")
				addOutput(host, 'echo "cpus_per_node = $localcpunode" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_CoresPerNode] > 0:
				addOutput(host, 'echo "cores_per_node = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_CoresPerNode],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server, using cores from CE' % (OSG_CoresPerNode))
				self.db.execute("""select n.cpus from nodes n where n.name='%s'""" % host)
				temp_cores, =self.db.fetchone()
				addOutput(host, 'echo "cores_per_node = %s" &gt;&gt; %s' % (temp_cores,configFile))

			if OSG_ClusterName[OSG_inbound] > 0:
				addOutput(host, 'echo "inbound_network = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_inbound],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server' % (OSG_inbound))
				if iclus == 1:
					addOutput(host, '#      using inbound_network = FALSE' )
					addOutput(host, 'echo "inbound_network = FALSE" &gt;&gt; %s' % (configFile))

			if OSG_ClusterName[OSG_outbound] > 0:
				addOutput(host, 'echo "outbound_network = %s" &gt;&gt; %s' % (OSG_ClusterName[OSG_outbound],configFile))
			else:
				addOutput(host, '#attr %s not defined for CE server' % (OSG_outbound))
				if iclus == 1:
					addOutput(host, '#      using outbound_network = TRUE' )
					addOutput(host, 'echo "outbound_network = TRUE" &gt;&gt; %s' % (configFile))
			addOutput(host, 'echo " " &gt;&gt; %s' % (configFile))

		if OSG_NmultiSE > 0:
			nSE = int(OSG_NmultiSE)
			if nSE < 0:
				nSE = 0
			for iclus in range(1,nSE+1):
				OSG_SE_cluster       = 'OSG_CE_gip_SE' + str(iclus)
				OSG_SE_OIM_Name      = 'OSG_CE_gip_SE_OIM_Name' + str(iclus)
				OSG_SE_Server        = 'OSG_CE_gip_SEServer' + str(iclus)
				OSG_SE_Port          = 'OSG_CE_gip_SEPort' + str(iclus)
				OSG_SE_provider      = 'OSG_CE_gip_SEprovider' + str(iclus)
				OSG_SE_implementation= 'OSG_CE_gip_SEimplementation' + str(iclus)
				OSG_SE_version       = 'OSG_CE_gip_SEversion' + str(iclus)
				OSG_SE_path          = 'OSG_CE_gip_SEpath' + str(iclus)
				OSG_SE_use_df        = 'OSG_CE_gip_SE_use_df' + str(iclus)

				OSG_SEs[OSG_SE_cluster]        = self.db.getHostAttr(host,OSG_SE_cluster)
				OSG_SEs[OSG_SE_OIM_Name]       = self.db.getHostAttr(host,OSG_SE_OIM_Name)
				OSG_SEs[OSG_SE_Server]         = self.db.getHostAttr(host,OSG_SE_Server)
				OSG_SEs[OSG_SE_Port]           = self.db.getHostAttr(host,OSG_SE_Port)
				OSG_SEs[OSG_SE_provider]       = self.db.getHostAttr(host,OSG_SE_provider)
				OSG_SEs[OSG_SE_implementation] = self.db.getHostAttr(host,OSG_SE_implementation)
				OSG_SEs[OSG_SE_version]        = self.db.getHostAttr(host,OSG_SE_version)
				OSG_SEs[OSG_SE_path]           = self.db.getHostAttr(host,OSG_SE_path)
				OSG_SEs[OSG_SE_use_df]         = self.db.getHostAttr(host,OSG_SE_use_df)

				if OSG_SEs[OSG_SE_cluster] > 0:
					addOutput(host, 'echo "[SE %s]" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_cluster],configFile))
					addOutput(host, 'echo "enabled = True" &gt;&gt; %s'  % (configFile))
					if OSG_SEs[OSG_SE_OIM_Name] >0:
						addOutput(host, 'echo "name = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_OIM_Name],configFile))
					else:
						addOutput(host, '#attr %s not defined for SE server' % (OSG_SE_OIM_Name))
					if OSG_SEs[OSG_SE_Server] > 0:
						if OSG_SEs[OSG_SE_Port] > 0:
							addOutput(host, 'echo "srm_endpoint = httpg://%s:%s/srm/v2/server" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_Server],OSG_SEs[OSG_SE_Port],configFile))
						else:
							addOutput(host, 'echo "srm_endpoint = httpg://%s:8443/srm/v2/server" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_Server],configFile))
					else:
						addOutput(host, '#attr %s not defined for SE server' % (OSG_SE_Server))
						if iclus == 1:
							addOutput(host, '#### USING attr OSG_SEServer')
							if OSG_SRMPort > 0:
								addOutput(host, '#### USING attr OSG_SRMPort')
								addOutput(host, 'echo "srm_endpoint = httpg://%s:%s/srm/v2/server" &gt;&gt; %s'  % (OSG_SEServer,OSG_SRMPort,configFile))
							else:
								addOutput(host, 'echo "srm_endpoint = httpg://%s:8443/srm/v2/server" &gt;&gt; %s'  % (OSG_SEServer,configFile))
					if OSG_SEs[OSG_SE_provider] > 0:
						addOutput(host, 'echo "provider_implementation = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_provider],configFile))
					else:
						addOutput(host, '#attr %s not defined for SE server' % (OSG_SE_provider))
						if iclus == 1:
							addOutput(host, '#### USING provider "bestman"')
							addOutput(host, 'echo "provider_implementation = bestman" &gt;&gt; %s'  % (configFile))
					if OSG_SEs[OSG_SE_implementation] > 0:
						addOutput(host, 'echo "implementation = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_implementation],configFile))
					else:
						addOutput(host, '#attr %s not defined for SE server' % (OSG_SE_implementation))
						if iclus == 1:
							addOutput(host, '#### USING implementation "bestman"')
							addOutput(host, 'echo "implementation = bestman" &gt;&gt; %s'  % (configFile))
					if OSG_SEs[OSG_SE_version] > 0:
						addOutput(host, 'echo "version = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_version],configFile))
					else:
						addOutput(host, '#attr %s not defined for SE server' % (OSG_SE_version))
					if OSG_SEs[OSG_SE_path] > 0:
						addOutput(host, 'echo "default_path  = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_path],configFile))
					else:
						addOutput(host, '#attr %s not defined for SE server' % (OSG_SE_path))
					if OSG_SEs[OSG_SE_use_df] > 0:
						addOutput(host, 'echo "use_df = %s" &gt;&gt; %s'  % (OSG_SEs[OSG_SE_use_df],configFile))
					else:
						addOutput(host, '#attr %s not defined for SE server' % (OSG_SE_use_df))
						if iclus == 1:
							addOutput(host, '#### USING use_df True"')
							addOutput(host, 'echo "use_df = True" &gt;&gt; %s'  % (configFile))
				else:
					addOutput(host, '#attr %s not defined for CE server' % (OSG_SE_cluster))
					addOutput(host, '#####Set %s to the section name [SE CHANGEME] you need in %s' % (OSG_SE_cluster,configFile))
		else:
			addOutput(host, '#attr OSG_CE_gip_NmultiSE not defined for CE server')
			addOutput(host, '#####Set OSG_CE_gip_NmultiSE to the number of SEs you need to configure in %s' % (configFile))

		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')

