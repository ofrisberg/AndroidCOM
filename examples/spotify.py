import sys,time
sys.path.append('../src')
from androidcom import AndroidCOM

"""
Example of how to use AndroidCOM to open Spotify, 
search for a song and play it.
"""

if __name__ == '__main__':
	
	ac = AndroidCOM()
	
	query = "times they are a changing"
	
	ac.startApp("com.spotify.music/.MainActivity")
	ac.sendEvent("KEYCODE_SEARCH")
	ac.pressTab()
	ac.sendEvent("KEYCODE_ENTER")
	ac.sendText(query)
	ac.sendEvent("KEYCODE_ENTER")
	ac.pressTab(4)
	ac.sendEvent("KEYCODE_ENTER")