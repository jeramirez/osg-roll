
import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 't3grid_submit'

        def localt3griddefault(self, host, kvstore): 
		#This defines new variables not defined by default in initializeDictionary 
		#but needed for tier3 submitter node settings
		kvstore['GRIDMANAGER_MAX_PENDING_SUBMITS_PER_RESOURCE'] = '20'
		kvstore['ENABLE_GRID_MONITOR']                          = 'True'
		kvstore['GRIDMANAGER_MAX_SUBMITTED_JOBS_PER_RESOURCE']  = '1000'

	def run(self, argv):
		host, kvstore = argv
		# test if GRID SUBMITTER is enabled for the host. If so, set up the
		# the correct config values in the key,value store
		t3grid_enabled = self.db.getHostAttr(host, 'OSG_Condor_EnableT3GRID_SUBMIT')
		if t3grid_enabled is not None:
			if (t3grid_enabled.lower() == 'true' or t3grid_enabled.lower() == 'yes'):
				self.localt3griddefault(host,kvstore)


