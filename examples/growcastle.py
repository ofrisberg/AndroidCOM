import sys,time
from datetime import datetime
sys.path.append('../src')
from androidcom import AndroidCOM

"""
Example of how to use AndroidCOM
The coordinates is specific for Samsung Galaxy S7 screen
"""

class GrowCastle:
	def __init__(self, ac):
		self.ac = ac
		self.mode = '' # battle,replay
		self.is_running = False
		self.turn_on_2x = True
		self.turned_on_2x = False
		
	
	def startBattle(self):
		self.mode = 'battle'
		self.start()
		
	def startReplay(self):
		self.mode = 'replay'
		self.start()
	
	def start(self):
		self.is_running = True
		self.starttime = datetime.now()
		self.loop(1)
		
	def stop(self):
		self.is_running = False
		diff_time = (datetime.now()-self.starttime).total_seconds()
		print("Playtime",diff_time/60,"minutes")
	
	def loop(self,i):
		if self.is_running is False: 
			print("Looped stopped")
			return
		print("--","Timestep",i,"--")
		if self.mode == 'battle':
			self.timestepBattle(i)
		elif self.mode == 'replay':
			self.timestepReplay(i)
		else: sys.exit("No such GrowCastle mode")
		self.loop(i+1)
		
	def timestepReplay(self,i):
		if self.turn_on_2x and i == 3 and self.turned_on_2x is False:
			self.press2x()
			self.turned_on_2x = True
		self.pressReplay()
		time.sleep(2)
		
	def timestepBattle(self,i):
		self.pressBattle()
		self.pressCloseSkipWave()
		time.sleep(50)
		
	def launch(self):
		self.ac.runShell("monkey -p com.raongames.growcastle -c android.intent.category.LAUNCHER 1")
		time.sleep(10)
		
	def save(self):
		#self.pressCloseMenuAd()
		self.pressSaveMenu()
		self.pressSavePopup()
		self.pressSavePopup2()
		self.pressSaveEmail()
		self.pressSaveOk()
		
	def close(self):
		self.ac.sendEvent("KEYCODE_APP_SWITCH")
		self.ac.sendSwipe("1200 500 500 500 100")
		
	def pressBattle(self): self.ac.sendTap(1760,1000)
	def pressCloseSkipWave(self): self.ac.sendTap(1340,360) #close 'skip wave'-popup if battle
	def pressReplay(self): self.ac.sendTap(1500,1000)
	def press2x(self): self.ac.sendTap(100,1000)
	def pressCloseMenuAd(self): self.ac.sendTap(1065,830)
	def pressSaveMenu(self): self.ac.sendTap(400,1000)
	def pressSavePopup(self): self.ac.sendTap(1230,660)
	def pressSavePopup2(self): self.ac.sendTap(1150,890)
	def pressSaveEmail(self): self.ac.sendTap(900,360)
	def pressSaveOk(self): self.ac.sendTap(1400,950)
	
if __name__ == '__main__':
	
	ac = AndroidCOM()
	#ac.unlockScreen()
	gc = GrowCastle(ac)
	#gc.launch()
	gc.startReplay()
	
	# will never run if start is called
	gc.close()

		
		
		
		
		
		
		