import sys,time
import tkinter as tk
sys.path.append('../src')
from maingui import MainGUI
from androidcom import AndroidCOM
from growcastle import GrowCastle

class GrowCastleGUI(MainGUI):
	def __init__(self, master=None):
		super().__init__(master)
		self.gc = GrowCastle(self.ac)
		
	def createGCSection(self):
		tk.Button(self.root, text="Launch", command=self.gcLaunch).grid(row=2, column=1)
		
		tk.Button(self.root, text="Replay", command=self.gcReplay).grid(row=2, column=2)
		tk.Button(self.root, text="Battle", command=self.gcBattle).grid(row=3, column=2)
		tk.Button(self.root, text="Stop", command=self.gcStop).grid(row=4, column=2)
		
		tk.Button(self.root, text="Save", command=self.gcSave).grid(row=2, column=3)
		tk.Button(self.root, text="Close", command=self.gcClose).grid(row=3, column=3)
		
	def gcLaunch(self):
		print("Launching...")
		self.cmd(self.gc.launch)
		
	def gcSave(self):
		print("Saving...")
		self.cmd(self.gc.save)
		
	def gcClose(self):
		print("Closing...")
		self.cmd(self.gc.close)
		
	def gcReplay(self):
		print("Starting replay...")
		self.cmd(self.gc.startReplay)
		
	def gcBattle(self):
		print("Starting battle...")
		self.cmd(self.gc.startBattle)
		
	def gcStop(self):
		print("Stopping...")
		self.cmd(self.gc.stop)
		
		
	
if __name__ == '__main__':
	root = tk.Tk()
	gcg = GrowCastleGUI(master=root)
	gcg.createGCSection()
	gcg.mainloop()
		