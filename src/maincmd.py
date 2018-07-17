import sys,argparse
from androidcom import AndroidCOM
import configsetup

class Runner:
	def __init__(self):
		self.args = self.getArgs()
		self.commands = self.args.commands
		
	def getArgs(self):
		argparser = argparse.ArgumentParser()
		argparser.add_argument('commands', nargs='?', help="Commands to execute")
		argparser.add_argument('--configfile', action="store_true", help="Generate a config file")
		return argparser.parse_args()

	def executeCommand(self,cmd):
		if cmd == 'wifi1': self.ac.enableWifi()
		elif cmd == 'wifi0': self.ac.disableWifi()
		elif cmd == 'blue1': self.ac.enableBluetooth()
		elif cmd == 'blue0': self.ac.disableBluetooth()
		else: print("Command '"+cmd+"' was not found")
		
	def setup(self):
		self.ac = AndroidCOM()
		
	def execute(self):
		for cmd in self.commands:
			self.executeCommand(cmd)

if __name__ == '__main__':
	runner = Runner()
	if runner.args.configfile is not None:
		configsetup.generate()
	else:
		runner.setup()
		runner.execute()
	
	
	
	
	
	
	