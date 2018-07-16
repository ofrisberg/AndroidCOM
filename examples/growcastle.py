import sys,time
sys.path.append('../src')
from androidcom import AndroidCOM

"""
Example of how to use AndroidCOM
The coordinates is specific for Samsung Galaxy S7 screen
"""

if __name__ == '__main__':
	
	ac = AndroidCOM()
	
	while True:
		#ac.sendTap(1760,1000) #battle
		ac.sendTap(1500,1000) #replay
		ac.sendTap(1340,360) #close 'skip wave'-popup if battle
		time.sleep(1)