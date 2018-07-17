import os,sys,subprocess,time,re
import configsetup,devicestatus,sensorstats
"""
ADB REFERENCE
https://developer.android.com/studio/command-line/adb

KEYCODES
https://stackoverflow.com/questions/7789826/adb-shell-input-events
https://developer.android.com/reference/android/view/KeyEvent

INSPIRATION
https://grymoire.wordpress.com/2014/09/17/remote-input-shell-scripts-for-your-android-device/
"""

class AndroidCOM:
	def __init__(self):
		self.cfg = configsetup.get()
		self.ds = devicestatus.DeviceStatus()
		self.ss = sensorstats.SensorStats()
		if self.cfg['GENERAL'].getboolean('auto_auth'): 
			self.unlockScreen()
		
	def checkAdb(self, cmd, st=0):
		full_command = self.cfg['PATHS']['adb']+" "+cmd
		out = subprocess.check_output(full_command)
		if st > 0: time.sleep(st)
		resp = out.decode("utf-8")
		if self.cfg['MODES'].getboolean('quiet') is False:
			print(full_command)
		if self.cfg['MODES'].getboolean('verbose'):
			print(resp)
		return resp
		
	def checkShell(self, cmd, st=0): 
		return self.checkAdb("shell "+cmd, st)
		
	def runShell(self, cmd, st=0): 
		out = self.checkShell(cmd,st)
				
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
		if self.cfg['GENERAL']['code'] == 'XXXX':
			print("Error: Cannot unlock because code is not set")
			return
		self.sendText(self.cfg['GENERAL']['code'])
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

	def statusPower(self): return self.ds.getPower(self.checkShell("dumpsys power"))
	def statusNotifications(self): return self.ds.getNotifications(self.checkShell("dumpsys notification"))
	def statusConnections(self): return self.ds.getConnections(self.checkShell("settings list global"))
	def statusWindows(self): return self.ds.getWindows(self.checkShell("dumpsys window windows"))
	def statusIp(self): return self.ds.getIp(self.checkShell("ifconfig wlan0"))
		
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
		
	def setBrightnessLow(self): self.setBrightness(self.cfg['BRIGHTNESS']['low'])
	def setBrightnessMedium(self): self.setBrightness(self.cfg['BRIGHTNESS']['medium'])
	def setBrightnessHigh(self): self.setBrightness(self.cfg['BRIGHTNESS']['high'])
		
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
		pullRes = self.checkAdb("pull "+scrConf['remote_file']+" "+scrConf['local_path'])
		return os.path.join(scrConf['local_path'],scrConf['filename'])
		
	#0 & 2 - 0/180, 1 & 3 - +-90
	#adb shell dumpsys input | grep SurfaceOrientation |  awk '{ print $2 }'
	def getOrientation(self):
		out = self.checkShell("dumpsys input | grep SurfaceOrientation")
		return re.search("\sSurfaceOrientation:\s([0-9])\s", out).group(1)
		
	def __del__(self):
		if self.cfg['GENERAL'].getboolean('auto_auth'): self.lockScreen()
		
#./adb shell dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'
#./adb shell dumpsys package r | grep 'android.settings'

# adb shell dumpsys window | \
#sed -n '/mUnrestrictedScreen/ s/^.*) \([0-9][0-9]*\)x\([0-9][0-9]*\)/\1 \2/p'

if __name__ == '__main__':
	ac = AndroidCOM()
	#ac.getScreenshot()
	
	#ac.toggleVibration()
	#print(ac.getOrientation())
	
	#ac.unlockScreen()
	#ac.listApps()
	#ac.listSystems()
	
	#print(ac.statusPower())
	print(ac.statusIp())
	
	#ac.toggleBluetooth()
	#ac.volumeDown(7)
	
	#ac.setBrightness(200)
	
	#ac.lockScreen()
	
	
	
	
	
	
	
	
	
	
	