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
		self.createRadioButtons()
		
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
	
	def createRadioButtons(self):
		connStatus = self.ac.statusConnections()
		powerStatus = self.ac.statusPower()
		
		# Wifi-row
		self.wifiVal = tk.BooleanVar()
		self.wifiVal.set(connStatus['wifi_enabled'])
		tk.Label(root, text="Wifi").grid(row=2,column=1)
		tk.Radiobutton(root, text="On", variable=self.wifiVal, command=lambda:self.cmd(self.ac.enableWifi), value=True).grid(row=2,column=2)
		tk.Radiobutton(root, text="Off", variable=self.wifiVal, command=lambda:self.cmd(self.ac.disableWifi), value=False).grid(row=2,column=3)
		
		# Bluetooth-row
		self.blueVal = tk.BooleanVar()
		self.blueVal.set(connStatus['bluetooth_enabled'])
		tk.Label(root, text="Bluetooth").grid(row=3,column=1)
		tk.Radiobutton(root, text="On", variable=self.blueVal, command=lambda:self.cmd(self.ac.enableBluetooth), value=True).grid(row=3,column=2)
		tk.Radiobutton(root, text="Off", variable=self.blueVal, command=lambda:self.cmd(self.ac.disableBluetooth), value=False).grid(row=3,column=3)

		# Lock/Unlock-row
		self.lockVal = tk.BooleanVar()
		self.lockVal.set(powerStatus['display_off'])
		tk.Label(root, text="Locker").grid(row=4,column=1)
		tk.Radiobutton(root, text="Locked", variable=self.lockVal, command=lambda:self.cmd(self.ac.lockScreen), value=True).grid(row=4,column=2)
		tk.Radiobutton(root, text="Unlocked", variable=self.lockVal, command=lambda:self.cmd(self.ac.unlockScreen), value=False).grid(row=4,column=3)
		
		# Brightness-row
		self.brightVal = tk.BooleanVar()
		self.brightVal.set(True)
		root.after(self.interval_status, self.updateValues)
		tk.Label(root, text="Brightness").grid(row=5,column=1)
		tk.Radiobutton(root, text="Low", variable=self.brightVal, command=lambda:self.cmd(self.ac.setBrightnessLow), value=False).grid(row=5,column=2)
		tk.Radiobutton(root, text="Mid", variable=self.brightVal, command=lambda:self.cmd(self.ac.setBrightnessMedium), value=True).grid(row=5,column=3)
		
	
		
	def updateValues(self):
		self.updateMsg("Updating values...")
		connStatus = self.ac.statusConnections()
		powerStatus = self.ac.statusPower()
		
		self.wifiVal.set(connStatus['wifi_enabled'])
		self.blueVal.set(connStatus['bluetooth_enabled'])
		self.lockVal.set(powerStatus['display_off'])
		self.updateMsg("Values updated")
		root.after(self.interval_status, lambda:self.cmd(self.updateValues))
		
	def say_hi(self):
		print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()