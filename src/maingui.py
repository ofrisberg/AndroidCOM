import sys, threading, time
import tkinter as tk
from PIL import Image, ImageTk
from androidcom import AndroidCOM

""" 
GUI for AndroidCOM with tkinter
"""

class MainGUI(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		
		self.root = master
		self.ac = AndroidCOM()
		
		self.total_width = self.ac.cfg['GUI'].getint('window_width')
		self.interval_image = self.ac.cfg['GUI'].getint('interval_image')
		self.interval_status = self.ac.cfg['GUI'].getint('interval_status')
		self.root.title("AndroidCOM")
		
		self.grid()
		self.createMsg()
		self.createImage()
		self.createMenu()
		
	def createMsg(self):
		self.msgBox = tk.Message(self.root, width=self.total_width, text="")
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
		self.imageLbl = tk.Label(self.root,image=self.ph)
		self.imageLbl.image = self.ph
		self.imageLbl.grid(row=1,column=1,columnspan=3)
		self.root.after(self.interval_image, self.updateImage)
	
	def updateImage(self):
		#self.updateMsg("Updating image...")
		self.ph = self.getImageTk()
		self.imageLbl.configure(image=self.ph)
		self.root.after(self.interval_image, lambda:self.cmd(self.updateImage))
		#self.updateMsg("Image updated")
	
	def cmd(self,cmdtext):
		t = threading.Thread(target=cmdtext,name="androidcom_thread")
		t.daemon = True
		t.start()
		
	def onClickWifi(self):
		if self.wifiVal: self.cmd(self.ac.enableWifi)
		else: self.cmd(self.ac.disableWifi)
	
	def createMenu(self):
		self.menubar = tk.Menu(self.root)
		
		settingsmenu = tk.Menu(self.menubar, tearoff = 0)
		self.createSettingsOptions(settingsmenu)
		
		statusmenu = tk.Menu(self.menubar, tearoff = 0)
		self.createStatusOptions(statusmenu)
		
		self.menubar.add_cascade(label="Settings", menu=settingsmenu)
		self.menubar.add_cascade(label="Status", menu=statusmenu)
		
		self.root.config(menu=self.menubar)
	
	def toggleBrightness(self):
		if self.brightVal.get(): self.cmd(self.ac.setBrightnessMedium)
		else: self.cmd(self.ac.setBrightnessLow)
	
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
		self.brightVal.set(False)
		settingsmenu.add_checkbutton(label="Brightness", variable=self.brightVal, command=self.toggleBrightness, onvalue=True, offvalue=False)
		
		self.root.after(self.interval_status, self.updateValues)
	
	def createStatusOptions(self,statusmenu):
		statusmenu.add_command(label="Power", command=self.printPower)
		statusmenu.add_command(label="Connections", command=self.printConnections)
		statusmenu.add_command(label="Notifications", command=self.printNotifications)
		statusmenu.add_command(label="Windows", command=self.printWindows)
		
	def printPower(self):
		print(self.ac.statusPower())
		
	def printConnections(self):
		print(self.ac.statusConnections())
		
	def printNotifications(self):
		print(self.ac.statusNotifications())
		
	def printWindows(self):
		print(self.ac.statusWindows())
		
	def updateValues(self):
		#self.updateMsg("Updating values...")
		connStatus = self.ac.statusConnections()
		powerStatus = self.ac.statusPower()
		
		self.wifiVal.set(connStatus['wifi_enabled'])
		self.blueVal.set(connStatus['bluetooth_enabled'])
		self.lockVal.set(powerStatus['display_off'])
		#self.updateMsg("Values updated")
		self.root.after(self.interval_status, lambda:self.cmd(self.updateValues))
		

if __name__ == '__main__':
	root = tk.Tk()
	app = MainGUI(master=root)
	app.mainloop()
		
		
		
		
		