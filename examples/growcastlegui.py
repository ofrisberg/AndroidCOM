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
		tk.Button(self.root, text="Gold deck", command=lambda:self.gcStatusAndExec(self.gc.switch2golddeck,"Gold deck")).grid(row=4, column=2)
		tk.Button(self.root, text="2X", command=lambda:self.gcStatusAndExec(self.gc.press2x,"2X")).grid(row=5, column=2)
		tk.Button(self.root, text="Stop", command=lambda:self.gcStatusAndExec(self.gc.stop,"Stop")).grid(row=6, column=2)
		tk.Button(self.root, text="Quit wave", command=lambda:self.gcStatusAndExec(self.gc.quitwave,"Quit wave")).grid(row=7, column=2)
		tk.Button(self.root, text="Stats", command=lambda:self.gcStatusAndExec(self.gc.stats,"Stats")).grid(row=8, column=2)
		
		tk.Button(self.root, text="Save", command=lambda:self.gcStatusAndExec(self.gc.save,"Save")).grid(row=2, column=3)
		tk.Button(self.root, text="Close", command=lambda:self.gcStatusAndExec(self.gc.close,"Close")).grid(row=3, column=3)
		
	def gcStatusAndExec(self,func,status):
		self.updateMsg(status)
		self.cmd(func)
		self.root.after(3000, lambda:self.cmd(lambda:self.updateImage(False)))
	
if __name__ == '__main__':
	root = tk.Tk()
	gcg = GrowCastleGUI(master=root)
	gcg.createGCSection()
	gcg.mainloop()
		