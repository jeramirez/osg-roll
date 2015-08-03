import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'rank'

	def defaultprovisioning(self, host, kvstore):
                #Default setting
		kvstore['RANK'] = '0'

	def run(self, argv):
		# 1. Get the hostname and the key-value store, which
		#    is a python dictionary 
		host, kvstore = argv 

		rank = self.db.getHostAttr(host, 'OSG_Condor_RANK')

		#default setting (to executable nodes)
		if "STARTD" in kvstore['DAEMON_LIST']:
			self.defaultprovisioning(host, kvstore)

		#customized setting (to any daemon)
		if rank>0:
			kvstore['RANK'] = rank

