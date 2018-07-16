import sys, threading, time
import tkinter as tk
from PIL import Image, ImageTk
sys.path.append('../src')
from androidcom import AndroidCOM

""" 
Example of how to use AndroidCOM with tkinter
Run with "$ python gui.py code"
"""

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		
		code = None
		if len(sys.argv) > 1: code = sys.argv[1]
		self.ac = AndroidCOM(code)
		
		self.total_width = 250
		self.interval_image = 10000
		self.interval_status = 4000
		root.title("AndroidCOM")
		
		print("Starting GUI")
		self.grid()
		self.createMsg()
		self.createImage()
		self.createMenu()
		#self.createRadioButtons()
		
	def createMsg(self):
		self.msgBox = tk.Message(root, width=self.total_width, text="GUI started")
		self.msgBox.grid(row=0,column=1,columnspan=3)
		
	def updateMsg(self,msg):
		self.msgBox.configure(text=msg)
		
	def getImageTk(self):
		im = Image.open(self.ac.getScreenshot())
		wpercent = (self.total_width/float(im.size[0]))
		hsize = int((float(im.size[1])*float(wpercent)))
		im = im.resize((self.total_width, hsize), Image.ANTIALIAS)
		return ImageTk.PhotoImage(im)
		
	def createImage(self):
		self.ph = self.getImageTk()
		self.imageLbl = tk.Label(root,image=self.ph)
		self.imageLbl.image = self.ph
		self.imageLbl.grid(row=1,column=1,columnspan=3)
		root.after(self.interval_image, self.updateImage)
	
	def updateImage(self):
		self.updateMsg("Updating image...")
		self.ph = self.getImageTk()
		self.imageLbl.configure(image=self.ph)
		root.after(self.interval_image, lambda:self.cmd(self.updateImage))
		self.updateMsg("Image updated")
	
	def cmd(self,cmdtext):
		t = threading.Thread(target=cmdtext,name="blabla_tkinter")
		t.daemon = True
		t.start()
		
	def onClickWifi(self):
		if self.wifiVal: self.cmd(self.ac.enableWifi)
		else: self.cmd(self.ac.disableWifi)
	
	def createMenu(self):
		self.menubar = tk.Menu(root)
		settingsmenu = tk.Menu(self.menubar, tearoff = 0)
		self.createSettingsOptions(settingsmenu)
		self.menubar.add_cascade(label="Settings", menu=settingsmenu)
		root.config(menu=self.menubar)
	
	def toggleBrightness(self):
		if self.brightVal.get(): self.cmd(self.ac.setBrightnessLow)
		else: self.cmd(self.ac.setBrightnessMedium)
	
	def createSettingsOptions(self,settingsmenu):
		connStatus = self.ac.statusConnections()
		powerStatus = self.ac.statusPower()
		
		# Wifi-row
		self.wifiVal = tk.BooleanVar()
		self.wifiVal.set(connStatus['wifi_enabled'])
		settingsmenu.add_checkbutton(label="Wifi", variable=self.wifiVal, command=lambda:self.cmd(self.ac.toggleWifi), onvalue=True, offvalue=False)
		
		# Bluetooth-row
		self.blueVal = tk.BooleanVar()
		self.blueVal.set(connStatus['bluetooth_enabled'])
		settingsmenu.add_checkbutton(label="Bluetooth", variable=self.blueVal, command=lambda:self.cmd(self.ac.toggleBluetooth), onvalue=True, offvalue=False)

		# Lock/Unlock-row
		self.lockVal = tk.BooleanVar()
		self.lockVal.set(powerStatus['display_off'])
		settingsmenu.add_checkbutton(label="Locker", variable=self.lockVal, command=lambda:self.cmd(self.ac.toggleScreen), onvalue=True, offvalue=False)
		
		# Brightness-row
		self.brightVal = tk.BooleanVar()
		self.brightVal.set(True)
		settingsmenu.add_checkbutton(label="Brightness", variable=self.brightVal, command=self.toggleBrightness, onvalue=True, offvalue=False)
		
		root.after(self.interval_status, self.updateValues)
	
		
	def updateValues(self):
		self.updateMsg("Updating values...")
		connStatus = self.ac.statusConnections()
		powerStatus = self.ac.statusPower()
		
		self.wifiVal.set(connStatus['wifi_enabled'])
		self.blueVal.set(connStatus['bluetooth_enabled'])
		self.lockVal.set(powerStatus['display_off'])
		self.updateMsg("Values updated")
		root.after(self.interval_status, lambda:self.cmd(self.updateValues))
		

root = tk.Tk()
app = Application(master=root)
app.mainloop()