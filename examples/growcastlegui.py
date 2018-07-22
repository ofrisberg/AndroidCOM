import sys,time
import tkinter as tk
sys.path.append('../src')
from maingui import MainGUI
from androidcom import AndroidCOM
from growcastle import GrowCastle

"""
tkinter keycodes
http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
"""

class GrowCastleGUI(MainGUI):
	def __init__(self, master=None):
		super().__init__(master)
		self.gc = GrowCastle(self.ac)
		self.bindKeys()
		
	def bindKeys(self):
		for i in range(10):
			self.root.bind(str(i), self.onNumKey)
		self.root.bind('<Control-s>', lambda x:self.gcStatusAndExec(self.gc.save,"Save"))
		self.root.bind('<Return>', lambda x:self.gcStatusAndExec(self.gc.pressBattle,"Battle"))
		self.root.bind('<BackSpace>', lambda x:self.gcStatusAndExec(self.gc.quitwave,"Quit wave"))
		self.root.bind('<Escape>', lambda x:self.gcStatusAndExec(self.gc.pressCloseMenuAd,"Close popup"))
		self.root.bind('<Up>', lambda x:self.gcStatusAndExec(self.gc.pressUpgradeCastle,"Upgrade castle"))
		self.root.bind('<Down>', lambda x:self.gcStatusAndExec(self.gc.pressUpgradeArcher,"Upgrade archer"))
		self.root.bind('<F1>', lambda x:self.gcStatusAndExec(self.gc.pressHell,"Hell"))
		self.root.bind('<F2>', lambda x:self.gcStatusAndExec(self.gc.pressReplay,"Replay"))
		self.root.bind('<F3>', lambda x:self.gcStatusAndExec(self.gc.pressBattle,"Battle"))
		
	def onNumKey(self, event):
		if event.char == '1': self.gcStatusAndExec(self.gc.pressH1,"")
		elif event.char == '2': self.gcStatusAndExec(self.gc.pressH2,"")
		elif event.char == '3': self.gcStatusAndExec(self.gc.pressH3,"")
		elif event.char == '4': self.gcStatusAndExec(self.gc.pressH4,"")
		elif event.char == '5': self.gcStatusAndExec(self.gc.pressH5,"")
		elif event.char == '6': self.gcStatusAndExec(self.gc.pressH6,"")
		elif event.char == '7': self.gcStatusAndExec(self.gc.pressH7,"")
		elif event.char == '8': self.gcStatusAndExec(self.gc.pressH8,"")
		elif event.char == '9': self.gcStatusAndExec(self.gc.pressH9,"")
		
		
	def createGCSection(self):
		tk.Button(self.root, text="Launch", command=lambda:self.gcStatusAndExec(self.gc.launch,"Launch")).grid(row=2, column=1)
		tk.Button(self.root, text="Screencap", command=lambda:self.gcStatusAndExec(lambda:self.updateImage(False),"Screencap")).grid(row=3, column=1)
		
		tk.Button(self.root, text="Replay", command=lambda:self.gcStatusAndExec(self.gc.startReplay,"Replay loop")).grid(row=2, column=2)
		tk.Button(self.root, text="Battle", command=lambda:self.gcStatusAndExec(self.gc.startBattle,"Battle loop")).grid(row=3, column=2)
		tk.Button(self.root, text="Gold deck", command=lambda:self.gcStatusAndExec(self.gc.switch2golddeck,"Gold deck")).grid(row=4, column=2)
		tk.Button(self.root, text="2X", command=lambda:self.gcStatusAndExec(self.gc.press2x,"2X")).grid(row=5, column=2)
		tk.Button(self.root, text="Stop", command=lambda:self.gcStatusAndExec(self.gc.stop,"Stop")).grid(row=6, column=2)
		tk.Button(self.root, text="Stats", command=lambda:self.gcStatusAndExec(self.gc.stats,"Stats")).grid(row=7, column=2)
		
		tk.Button(self.root, text="Close", command=lambda:self.gcStatusAndExec(self.gc.close,"Close")).grid(row=2, column=3)
		#self.heroBtn = tk.Button(self.root, text="Hero")
		#self.heroBtn.grid(row=4, column=3)
		
		
		
	def gcStatusAndExec(self,func,status):
		self.updateMsg(status)
		self.cmd(func)
		#self.root.after(10000, lambda:self.cmd(lambda:self.updateImage(False)))
	
if __name__ == '__main__':
	root = tk.Tk()
	gcg = GrowCastleGUI(master=root)
	gcg.createGCSection()
	gcg.mainloop()
		