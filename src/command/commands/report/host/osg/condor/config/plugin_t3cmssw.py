
import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 't3grid-cmssw'

        def localt3cmsswdefault(self, host, kvstore): 
		#This defines new variables not defined by default in initializeDictionary 
		#but needed for cmssw t3 settings
		kvstore['PREEMPTION_REQUIREMENTS']        = 'False'
		kvstore['NEGOTIATOR_CONSIDER_PREEMPTION'] = 'False'
		kvstore['CLAIM_WORKLIFE']                 = '300'
		kvstore['STARTIDLETIME']                  = '0'
		#policy for cmssw jobs
		#CMSSW jobs cannot be evicted and resumed without loss of compute cycles
		kvstore['WANT_SUSPEND']                   = 'True'
		kvstore['SUSPEND']                        = '( (CpuBusyTime &gt; 2 * $(MINUTE)) &amp;&amp; $(ActivationTimer) &gt; 300 )'
		kvstore['CONTINUE']                       = '$(CPUIdle) &amp;&amp; ($(ActivityTimer) &gt; 10)'
		kvstore['PREEMPT']                        = 'False'
		#gratia from osg want job reported this directory
		kvstore['PER_JOB_HISTORY_DIR']            = '/var/lib/gratia/data'

	def run(self, argv):
		host, kvstore = argv
		# test if CMSSW is enabled for the host. If so, set up the
		# the correct config values in the key,value store
		t3cmssw_enabled = self.db.getHostAttr(host, 'OSG_Condor_EnableT3GRID_CMSSW')
		if t3cmssw_enabled is not None:
			if (t3cmssw_enabled.lower() == 'true' or t3cmssw_enabled.lower() == 'yes'):
				self.localt3cmsswdefault(host,kvstore)


