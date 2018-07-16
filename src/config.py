import os,sys,configparser

"""
Generate a default config file
https://docs.python.org/3/library/configparser.html
"""
def genConfig():
	cfg = configparser.ConfigParser()
	
	cfg['GENERAL'] = {
		'code' : '',
		'auto_auth' : 'on',
		'strict_mode' : 'off',
		'quiet_mode' : 'off',
		'check_display' : 'on'
	}
	
	cfg['PATHS'] = {
		'project_dir' : os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')),
		'tmp_dir' : '${project_dir}/tmp',
		'adb' : 'adb'
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
	
	return cfg

def saveConfig(cfg, filename="config.ini"):
	with open(filename, 'w') as configfile:
		cfg.write(configfile)
	
def init():
	cfg = genConfig()
	saveConfig(cfg)
	
if __name__ == '__main__':
	init()