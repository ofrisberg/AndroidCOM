import sys,argparse
from androidcom import AndroidCOM

class Runner:
	def __init__(self):
		self.args = self.getArgs()
		self.code = self.args.code
		self.adbpath = self.args.adbpath
		self.autolock = ("yes" in self.args.autolock)
		self.printconfigs = ("yes" in self.args.printconfigs)
		self.commands = self.args.commands
		
	def getArgs(self):
		argparser = argparse.ArgumentParser()
		argparser.add_argument('commands', nargs='+', help="Commands to execute")
		argparser.add_argument('--code', default=None, help="Code used to unlock device, default='None'")
		argparser.add_argument('--adbpath', default="adb", help="Path to ADB bin, default='adb'")
		argparser.add_argument('--autolock', default="no", help="yes/no to unlock/lock on start/finish, default='no'")
		argparser.add_argument('--printconfigs', default="no", help="yes/no to print configs and exit, default='no'")
		return argparser.parse_args()
		
	def printConfigs(self):
		print("Code:",self.code)
		print("ADB-path:",self.adbpath)
		print("Autolock:",self.autolock)
		print("Commands:")
		print(self.args.commands)

	def executeCommand(self,cmd):
		if cmd == 'wifi1': self.ac.enableWifi()
		elif cmd == 'wifi0': self.ac.disableWifi()
		elif cmd == 'blue1': self.ac.enableBluetooth()
		elif cmd == 'blue0': self.ac.disableBluetooth()
		else: print("Command '"+cmd+"' was not found")
		
	def setup(self):
		self.ac = AndroidCOM(self.code,self.adbpath,self.autolock)
		
	def execute(self):
		for cmd in self.commands:
			self.executeCommand(cmd)

if __name__ == '__main__':
	runner = Runner()
	if runner.printconfigs:
		runner.printConfigs()
		sys.exit()

	runner.setup()
	runner.execute()
	
	
	
	
	
	
	