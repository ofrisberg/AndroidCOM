import re

class DeviceStatus:
	def __init__(self):
		pass
		
	def getPower(self, text):
		power = {}
		power['display_off'] = ("mHoldingDisplaySuspendBlocker=false" in text)
		power['is_powered'] = ("mIsPowered=true" in text)
		power['battery_level'] = re.search("mBatteryLevel=([0-9]+)",text).group(1)
		return power
		
	def getNotifications(self, text):
		#./adb shell dumpsys notification | egrep NotificationRecord | awk -F\| '{print $0}'
		tmps = text.split("\n")
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
		
	def getConnections(self, text):
		return {
			'wifi_enabled': ("wifi_on=1" in text),
			'bluetooth_enabled': ("bluetooth_on=1" in text),
			'airplane_enabled' : ("airplane_mode_on=1" in text)
		}