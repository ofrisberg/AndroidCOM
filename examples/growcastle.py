import os,sys,time,pytesseract,cv2,re
from datetime import datetime
sys.path.append('../src')
from androidcom import AndroidCOM
from PIL import Image

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
		
	def msg(self,text):
		print(text)
	
	def isFocused(self):
		windows = self.ac.statusWindows()
		return 'com.raongames.growcastle' in windows['current']
	
	def startBattle(self):
		self.msg("Starting battle...")
		self.mode = 'battle'
		self.start()
		
	def startReplay(self):
		self.msg("Starting replay...")
		self.mode = 'replay'
		self.start()
		
	def startRedDragon(self):
		self.msg("Starting red dragon...")
		self.mode = 'reddragon'
		self.start()
	
	def start(self):
		if self.is_running:
			self.msg("Error: Already started")
			return
		if self.isFocused() is False:
			self.msg("Error: Window not focused")
			return
		self.is_running = True
		self.starttime = datetime.now()
		self.loop(1)
		
	def stop(self):
		self.msg("Stopping...")
		if self.is_running is False:
			self.msg("Error: Already stopped")
			return
		self.is_running = False
		diff_time = (datetime.now()-self.starttime).total_seconds()
		minutes = diff_time/60
		self.msg("Playtime "+str(minutes)+" minutes")
	
	def loop(self,i):
		if self.is_running is False: 
			self.msg("Loop stopped")
			return
		self.msg("-- Timestep "+str(i)+" --")
		if self.mode == 'battle':
			self.timestepBattle(i)
		elif self.mode == 'replay':
			self.timestepReplay(i)
		elif self.mode == 'reddragon':
			self.timestepRedDragon(i)
		else: sys.exit("No such GrowCastle mode")
		self.loop(i+1)
		
	def timestepReplay(self,i):
		self.pressReplay()
		time.sleep(2)
		
	def timestepBattle(self,i):
		self.pressBattle()
		self.pressCloseSkipWave()
		for i in range(2):
			time.sleep(10)
			self.burst()
		time.sleep(33)
		
	def timestepRedDragon(self,i):
		self.pressDragonMenu()
		self.pressRedDragon()
		self.pressRedDragon2()
		time.sleep(1)
		self.burst()
		time.sleep(10)
		self.burst()
		time.sleep(18)
		self.pressDragonGet()
		
	def launch(self):
		self.msg("Launching game...")
		if self.isFocused():
			self.msg("Error: Window already focused")
			return
		self.ac.runShell("monkey -p com.raongames.growcastle -c android.intent.category.LAUNCHER 1")
		time.sleep(10)
		
	def save(self):
		self.msg("Saving game...")
		if self.isFocused() is False:
			self.msg("Error: Window not focused")
			return
		#self.pressCloseMenuAd()
		self.pressSaveMenu()
		self.pressSavePopup()
		self.pressSavePopup2()
		self.pressSaveEmail()
		self.pressSaveOk()
		
	def close(self):
		self.msg("Closing game...")
		if self.isFocused() is False:
			self.msg("Error: Window not focused")
			return
		self.ac.sendEvent("KEYCODE_APP_SWITCH")
		self.ac.sendSwipe("1200 500 500 500 100")
		
	def stats(self):
		if self.isFocused() is False:
			self.msg("Error: Window not focused")
			return
		
		self.pressAchieveMenu()
		time.sleep(2)
		imgurl = self.ac.getScreenshot()
		
		img = Image.open(imgurl)
		area = (1200, 532,1823, 647) #left,upper,right,lower
		cropped_img = img.crop(area)
		filename_achieve = os.path.join(self.ac.cfg['SCREEN_CAPTURE']['local_dir'],'achieve.png')
		cropped_img.save(filename_achieve)
		text = self.image2text(filename_achieve,True,True)
		
		reres = re.search("([0-9]+)\s([0-9]+)",text)
		if reres:
			score = reres.group(1)
			wave = reres.group(2)
			print('Wave',wave)
			print('Score',score)
		else: print("Regex failed")
		
		self.pressCloseAchieve()
		
	def image2text(self,url,doGray=True,doBlur=True):
		gray = cv2.imread(url)
		if doGray:
			gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
		if doBlur:
			gray = cv2.medianBlur(gray, 3)
		filename = str(os.getpid())+".png"
		cv2.imwrite(filename, gray)
		text = pytesseract.image_to_string(Image.open(filename))
		os.remove(filename)
		return text
		
	def switch2golddeck(self):
		if self.isFocused() is False:
			self.msg("Error: Window not focused")
			return
		self.pressDeckMenu()
		self.pressGoldDeck()
		
	def quitwave(self):
		if self.isFocused() is False:
			self.msg("Error: Window not focused")
			return
		self.pressQuitWave()
		self.pressConfirmQuitWave()
		
	def burst(self):
		#btime = datetime.now()
		self.pressH1()
		self.pressH2()
		self.pressH3()
		self.pressH4()
		self.pressH5()
		self.pressH9()
		#diff_time = (datetime.now()-btime).total_seconds()
		#print(diff_time,"seconds")
		
	
		
	def pressHell(self): self.ac.sendTap(1230,1000)
	def pressBattle(self): self.ac.sendTap(1760,1000)
	def pressCloseSkipWave(self): self.ac.sendTap(1340,360) #close 'skip wave'-popup if battle
	def pressReplay(self): self.ac.sendTap(1500,1000)
	def press2x(self): self.ac.sendTap(100,1000)
	def pressCloseMenuAd(self): self.ac.sendTap(1065,830)
	def pressDeckMenu(self): self.ac.sendTap(700,1000)
	def pressGoldDeck(self): self.ac.sendTap(700,400)
	def pressSaveMenu(self): self.ac.sendTap(400,1000)
	def pressSavePopup(self): self.ac.sendTap(1230,660)
	def pressSavePopup2(self): self.ac.sendTap(1150,890)
	def pressSaveEmail(self): self.ac.sendTap(900,360)
	def pressSaveOk(self): self.ac.sendTap(1400,950)
	def pressQuitWave(self): self.ac.sendTap(250,1000)
	def pressConfirmQuitWave(self): self.ac.sendTap(1200,950)
	def pressAchieveMenu(self): self.ac.sendTap(230,1000)
	def pressCloseAchieve(self): self.ac.sendTap(1840,110)
	def pressUpgradeCastle(self): self.ac.sendTap(1600,200)
	def pressUpgradeArcher(self): self.ac.sendTap(1600,350)
	def pressH1(self): self.tap(450,550)
	def pressH2(self): self.tap(570,550)
	def pressH3(self): self.tap(680,550)
	def pressH4(self): self.tap(450,420)
	def pressH5(self): self.tap(570,420)
	def pressH6(self): self.tap(680,420)
	def pressH7(self): self.tap(450,280)
	def pressH8(self): self.tap(570,280)
	def pressH9(self): self.tap(680,280)
	def pressDragonMenu(self): self.ac.sendTap(930,340)
	def pressRedDragon(self): self.ac.sendTap(1500,560)
	def pressRedDragon2(self): self.ac.sendTap(1720,580)
	def pressDragonGet(self): self.ac.sendTap(1125,800)
	
	def tap(self,x,y):
		self.ac.sendTap(x,y,0)
	
if __name__ == '__main__':
	
	ac = AndroidCOM()
	#ac.unlockScreen()
	gc = GrowCastle(ac)
	#gc.launch()
	#gc.stats()
	gc.startRedDragon()
	
	# will never run if start is called
	#gc.close()

		
		
		
		
		
		
		