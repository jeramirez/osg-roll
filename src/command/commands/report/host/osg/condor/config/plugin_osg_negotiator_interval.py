import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'osg_negotiator_interval'

	def run(self, argv):
		# 1. Get the hostname and the key-value store, which
		#    is a python dictionary 
		host, kvstore = argv 

		interval = self.db.getHostAttr(host, 'OSG_NEGOTIATOR_INTERVAL')
		if interval>0:
			kvstore['NEGOTIATOR_INTERVAL'] = interval


