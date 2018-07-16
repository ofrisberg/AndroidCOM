import os,sys,subprocess,time,re

"""
KEYCODES
https://stackoverflow.com/questions/7789826/adb-shell-input-events
https://developer.android.com/reference/android/view/KeyEvent
"""

class AndroidCOM:
	def __init__(self, code=None, adbpath="adb", autoUnlockLock=False):
		self.adbpath = adbpath
		self.code = code
		self.autoUnlockLock = autoUnlockLock
		if self.autoUnlockLock: self.unlockScreen()
		
		
	def __del__(self):
		if self.autoUnlockLock: self.lockScreen()

	def runShell(self, cmd, st=0):
		subprocess.run(self.adbpath+" shell "+cmd)
		time.sleep(st)
		
	def checkShell(self, cmd, st=0):
		out = subprocess.check_output(self.adbpath+" shell "+cmd)
		time.sleep(st)
		return out.decode("utf-8")
		
	def listApps(self): self.runShell("pm list packages")
	def listSystems(self): self.runShell('dumpsys | grep "DUMP OF SERVICE"')
		
	def sendEvent(self, nr, st=0.4):
		self.runShell("input keyevent "+ str(nr), st)
		
	def sendText(self,text, st=0.4):
		t = text.replace(" ","%s")
		self.runShell("input text " + t, st)
		
	def sendSwipe(self, args, st=0.4):
		self.runShell("input swipe " + args, st)
	def swipeLeft(self): self.sendSwipe("800 1000 200 1000 100")
		
	def sendTap(self, x, y=None, st=0.4):
		if y is None: self.runShell("input tap "+str(x), st)
		else: self.runShell("input tap "+str(x)+" "+str(y), st)
		
	def pressTab(self,nrTimes=1):
		for i in range(nrTimes): self.sendEvent(61,0)
		
	def toggleScreen(self):
		power = self.statusPower()
		if power['display_off']: self.unlockScreen()
		else: self.lockScreen()
		
	def unlockScreen(self):
		self.sendEvent("KEYCODE_WAKEUP")
		self.sendEvent(82)
		if self.code is None:
			print("Error: Cannot unlock because code is not set")
			return
		self.sendText(self.code)
		self.sendEvent(66,0.7)
		
	def lockScreen(self):
		self.sendEvent(26)
		
		

	def startApp(self, appname, flag="-n"):
		#self.runShell("monkey -p "+appname+" -c android.intent.category.LAUNCHER 1")
		self.runShell("am start -W "+flag+" "+appname+"")
		
	def stopApp(self):
		self.sendEvent("KEYCODE_APP_SWITCH")
		self.swipeLeft()
		#self.runShell("am kill "+appname+"")

	def statusPower(self):
		out = self.checkShell("dumpsys power")
		power = {}
		power['display_off'] = ("mHoldingDisplaySuspendBlocker=false" in out)
		power['is_powered'] = ("mIsPowered=true" in out)
		power['battery_level'] = re.search("mBatteryLevel=([0-9]+)",out).group(1)
		return power
		
	def statusNotifications(self):
		#./adb shell dumpsys notification | egrep NotificationRecord | awk -F\| '{print $0}'
		tmps = self.checkShell("dumpsys notification").split("\n")
		notTexts = []
		for tmp in tmps: 
			if "NotificationRecord(" in tmp: notTexts.append(tmp.strip())
		notifications = []
		for notText in notTexts:
			notification = {'app':'','tag':'','importance':'-1'}
			notification['app'] = re.search("\spkg=([^\s]+)\s",notText).group(1)
			notification['tag'] = re.search("\stag=([^\s]+)\s",notText).group(1)
			notification['importance'] = re.search("\simportance=([^\s]+)\s",notText).group(1)
			#print(notText)
			#print(notification)
			notifications.append(notification)
		return notifications
		
	def statusWifi(self):
		dump = self.checkShell("dumpsys wifi")
		wifi = {'wifi_enabled': ("Wi-Fi is enabled" in dump)}
		return wifi
		
	def statusBluetooth(self):
		dump = self.checkShell("dumpsys bluetooth_manager")
		blue = {'bluetooth_enabled': ("enabled: true" in dump)}
		return blue
		
	def statusConnections(self):
		dump = self.checkShell("settings list global")
		return {
			'wifi_enabled': ("wifi_on=1" in dump),
			'bluetooth_enabled': ("bluetooth_on=1" in dump),
			'airplane_enabled' : ("airplane_mode_on=1" in dump)
		}
		
	def toggleConnection(self,nrTabs):
		self.startApp("android.settings.WIRELESS_SETTINGS", "-a")
		self.pressTab(nrTabs)
		self.sendEvent(66)
		self.sendEvent(66)
		self.stopApp()
		
	def toggleTopMenuSetting(self, xy):
		self.sendSwipe("500 0 500 400")
		self.sendTap(xy)
		self.sendSwipe("500 400 500 0")
		
	def toggleWifi(self): self.toggleTopMenuSetting("135 180")
	def toggleBluetooth(self): self.toggleTopMenuSetting("300 180")
		
		
	def enableWifi(self):
		if self.statusConnections()['wifi_enabled']:
			print("Wifi already enabled")
			return
		self.toggleWifi()
		
	def enableBluetooth(self):
		if self.statusConnections()['bluetooth_enabled']:
			print("Bluetooth already enabled")
			return
		self.toggleBluetooth()
	
	def disableWifi(self):
		if self.statusConnections()['wifi_enabled']:
			self.toggleWifi()
			return
		print("Wifi already disabled")
		
	def disableBluetooth(self):
		if self.statusConnections()['bluetooth_enabled']:
			self.toggleBluetooth()
			return
		print("Bluetooth already disabled")
		
	def toggleVibration(self):
		self.sendSwipe("500 0 500 400")
		self.sendTap("637 218")
		self.sendSwipe("500 400 500 0")
		
	#! @param value ranges from 0-255
	def setBrightness(self,value):
		self.runShell("settings put system screen_brightness_mode 0")
		self.runShell("settings put system screen_brightness "+str(value)+"")
		
	def setBrightnessLow(self): self.setBrightness(0)
	def setBrightnessMedium(self): self.setBrightness(125)
		
	def volumeUp(self,steps):
		for i in range(steps): self.sendEvent("KEYCODE_VOLUME_UP")
	def volumeDown(self,steps):
		for i in range(steps): self.sendEvent("KEYCODE_VOLUME_DOWN")
		
	def mediaPlay(self): self.sendEvent("KEYCODE_MEDIA_PLAY")
	def mediaPause(self): self.sendEvent("KEYCODE_MEDIA_PAUSE")
	def mediaPlayPause(self): self.sendEvent("KEYCODE_MEDIA_PLAY_PAUSE")
	def mediaNext(self): self.sendEvent("KEYCODE_MEDIA_NEXT")
	def mediaPrevious(self): self.sendEvent("KEYCODE_MEDIA_PREVIOUS")
	
	def getScreenshotConfig(self):
		filename = "tmp_androidcom_screen.png"
		return {
			'remote_file' : "/sdcard/Download/"+filename,
			'local_path' : os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tmp')),
			'filename' : filename
		}
	
	def getScreenshot(self):
		scrConf = self.getScreenshotConfig()
		self.runShell("screencap "+scrConf['remote_file'])
		subprocess.run(self.adbpath+" pull "+scrConf['remote_file']+" "+scrConf['local_path'])
		return os.path.join(scrConf['local_path'],scrConf['filename'])
		
#./adb shell dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'
#./adb shell dumpsys package r | grep 'android.settings'
if __name__ == '__main__':
	ac = AndroidCOM()
	#ac.getScreenshot()
	
	ac.toggleVibration()
	
	#ac.unlockScreen()
	#ac.listApps()
	#ac.listSystems()
	
	#conn = ac.statusConnections()
	#print(conn)
	
	#ac.toggleBluetooth()
	#ac.volumeDown(7)
	
	#ac.setBrightness(200)
	
	#ac.lockScreen()
	
	
	
	
	
	
	
	
	
	
	