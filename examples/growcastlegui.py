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
		tk.Button(self.root, text="Launch", command=lambda:self.gcStatusAndExec(self.gc.launch,"Launch")).grid(row=2, column=1)
		
		tk.Button(self.root, text="Replay", command=lambda:self.gcStatusAndExec(self.gc.startReplay,"Replay loop")).grid(row=2, column=2)
		tk.Button(self.root, text="Battle", command=lambda:self.gcStatusAndExec(self.gc.startBattle,"Battle loop")).grid(row=3, column=2)
		tk.Button(self.root, text="Stop", command=lambda:self.gcStatusAndExec(self.gc.stop,"Stop")).grid(row=4, column=2)
		
		tk.Button(self.root, text="Save", command=lambda:self.gcStatusAndExec(self.gc.save,"Save")).grid(row=2, column=3)
		tk.Button(self.root, text="Close", command=lambda:self.gcStatusAndExec(self.gc.close,"Close")).grid(row=3, column=3)
		
	def gcStatusAndExec(self,func,status):
		self.updateMsg(status)
		self.cmd(func)
	
if __name__ == '__main__':
	root = tk.Tk()
	gcg = GrowCastleGUI(master=root)
	gcg.createGCSection()
	gcg.mainloop()
		