import os,sys,configparser

"""
Generate and get config file
https://docs.python.org/3/library/configparser.html
"""
def generate():
	cfg = configparser.ConfigParser()
	
	cfg['GENERAL'] = {
		'code' : 'XXXX',
		'auto_auth' : 'off',
		'check_display' : 'on'
	}
	
	cfg['PATHS'] = {
		'project_dir' : os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')),
		'tmp_dir' : '${project_dir}/tmp',
		'adb' : 'adb'
	}
	
	cfg['MODES'] = {
		'strict' : 'off',
		'quiet' : 'off',
		'verbose' : 'on'
	}
	
	cfg['SCREEN_LIMITS'] = {
		'x_min' : '0',
		'y_min' : '0',
		'x_max' : '1080',
		'y_max' : '1920'
	}
	
	cfg['SCREEN_CAPTURE'] = {
		'filename' : 'tmp_androidcom_screen',
		'remote_dir' : '/sdcard/Download/',
		'local_dir' : '${PATHS:tmp_dir}',
	}
	
	cfg['BRIGHTNESS'] = {
		'low' : '0',
		'medium' : '125',
		'high' : '255',
		'startup_low' : 'on'
	}
	
	cfg['GUI'] = {
		'window_width' : '250',
		'interval_image' : '10000',
		'interval_status' : '4000',
	}
	
	cfg['APPS'] = {
		'settings_wireless' : 'android.settings.WIRELESS_SETTINGS',
	}
	
	filename = getFilename()
	with open(filename, 'w') as configfile:
		cfg.write(configfile)
	
def get():
	cfg = configparser.ConfigParser()
	filename = getFilename()
	if os.path.isfile(filename): 
		cfg.read(filename)
		return cfg
	print("Error: Could not find config file '"+ filename +"'")
	sys.exit()

def getFilename():
	return os.path.join(os.path.dirname( __file__ ), '..', 'config.ini')
	
if __name__ == '__main__':
	print("This script is not runnable")
	
	
	
	
	