import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'dynamic_provisioning'

	def defaultprovisioning(self, host, kvstore, is_executable, is_negotiator):
		#Default setting
		#This defines new variables not defined by default in initializeDictionary
		if is_executable:
			kvstore['NUM_SLOTS'] = 1
			kvstore['NUM_SLOTS_TYPE_1'] = 1
			kvstore['SLOT_TYPE_1'] = '100%'
			kvstore['SLOT_TYPE_1_PARTITIONABLE'] = 'True'
			kvstore['STARTD_ATTRS'] = '$(STARTD_ATTRS), SLOT_TYPE_1_PARTITIONABLE'
		if is_negotiator:
			kvstore['SLOT_TYPE_1_CONSUMPTION_POLICY'] = 'True'
			kvstore['SLOT_TYPE_1_CONSUMPTION_CPUS'] = 'TARGET.RequestCpus'
		kvstore['ASSIGN_CPU_AFFINITY'] = 'True'

	def run(self, argv):
		# 1. Get the hostname and the key-value store, which
		#    is a python dictionary 
		host, kvstore = argv 

		multicore = self.db.getHostAttr(host, 'OSG_Condor_Multicore')
		num_slots = self.db.getHostAttr(host, 'OSG_Condor_NUM_SLOTS')
		executable= False
		negotiator= False
		if "STARTD" in kvstore['DAEMON_LIST']:
			executable = True
		if "NEGOTIATOR" in kvstore['DAEMON_LIST']:
			negotiator = True

		if multicore is not None and (multicore.lower() == 'true' or multicore.lower() == 'yes'):
			self.defaultprovisioning(host, kvstore, executable, negotiator)

			#customized setting
			if num_slots>0:
				nslot= int(num_slots)
				if nslot < 0:
					nslot = 1
				if executable:
					kvstore['NUM_SLOTS'] = nslot
				for i in range(1,nslot+1):
					islot = 'NUM_SLOTS_TYPE_' + str(i)
					itype = 'SLOT_TYPE_' + str(i)
					ipart = itype + '_PARTITIONABLE'
					icons = itype + '_CONSUMPTION_POLICY'
					icpus = itype + '_CONSUMPTION_CPUS'
					igpus = itype + '_CONSUMPTION_gpus'
					#attr OSG_Condor_NUM_SLOTS_TYPE_1
					osgslot = self.db.getHostAttr(host, 'OSG_Condor_'+ islot)
					#attr OSG_Condor_SLOT_TYPE_1
					osgtype = self.db.getHostAttr(host, 'OSG_Condor_'+ itype)
					#attr OSG_Condor_SLOT_TYPE_1_PARTITIONABLE
					osgpart = self.db.getHostAttr(host, 'OSG_Condor_'+ ipart)
					#attr OSG_Condor_SLOT_TYPE_1_CONSUMPTION_CPUS
					osgcpus = self.db.getHostAttr(host, 'OSG_Condor_'+ icpus)
					#attr OSG_Condor_SLOT_TYPE_1_CONSUMPTION_gpus
					osggpus = self.db.getHostAttr(host, 'OSG_Condor_'+ igpus)
					if osgslot > 0 and executable:
						kvstore[islot] = osgslot
					if osgtype > 0 and executable:
						kvstore[itype] = osgtype
					if osgpart > 0 and executable:
						kvstore[ipart] = osgpart
						if not ipart in kvstore['STARTD_ATTRS']:
							kvstore['STARTD_ATTRS'] = kvstore['STARTD_ATTRS'] + ", ipart"
					if negotiator:
						kvstore[icons] = 'True'
					if negotiator and osgcpus>0:
						kvstore[icpus] = osgcpus
					if negotiator and osggpus>0:
						kvstore[igpus] = osggpus

