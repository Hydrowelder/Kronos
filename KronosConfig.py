from datetime import datetime
import configparser
import time

def General_Config(config):
    Morning = 6  # 6 AM
    Night   = 21 # 9 PM

    current_time_ep = time.time()
    current_time_dt = datetime.now()
        
    def_freq = 5 # min/pic
    # def_freq = def_freq*60/5 # pic/hour

    def_len = 1 # days
    # def_len = def_len*24*60*60 # s

    image_freq = float(input('Image frequency (in min/pic, default '+str(def_freq)+' min/pic):\n') or def_freq) # image frequency in pics/hour
    # image_freq = 1/image_freq # min/pic

    timelapse_length = float(input('\nTimelapse length (in days, default '+ str(def_len)+' day(s)):\n') or def_len) # timelapse length in days

    picture_folder = input('\nFolder to put images in (can be created here, default is current date):\n') or current_time_dt.strftime("%m_%d_%Y") # folder in working directory to take images from

    start_time = input('\nTime to begin timelapse (month/day/year hour:min, default no delay):\nExample: 02/29/2022, 13:05\n') or current_time_dt.strftime("%m/%d/%Y, %H:%M")

    start_time_dt = datetime.strptime(start_time,"%m/%d/%Y, %H:%M")
    start_time_ep = round(start_time_dt.timestamp())
    if start_time_ep < current_time_ep and start_time != current_time_dt.strftime("%m/%d/%Y, %H:%M"):
        print('WARNING: START TIME IN THE PAST!')
        
    # image_type = input('\nImage file extension (default .jpg):\n') or '.jpg'
    # if not '.' in image_type:
    #     image_type = '.'+image_type
    image_type = '.jpg'
    
    config.add_section('General')

    config['General']['Morning'] = str(Morning)
    config['General']['Night'] = str(Night)
    config['General']['image_freq'] = str(image_freq)
    config['General']['start_time'] = start_time
    config['General']['timelapse_length'] = str(timelapse_length)
    config['General']['picture_folder'] = picture_folder
    config['General']['image_type'] = image_type
    return config

def Camera_Config(config):
    # https://picamera.readthedocs.io/en/release-1.10/api_camera.html
    resolution = (1920,1080) # def (1280,720) | (pxl, pxl)
    shutter_speed = int(20000/2) # def 0 | microsec (US main 20000)
    iso = 100 # def 0 | can be 100, 200, 320, 400, 500, 640, 800, 1600
    rotation = 180 # def 0 | degrees
    config.add_section('Camera')
    config['Camera']['resolution'] = str(resolution)
    config['Camera']['shutter_speed'] = str(shutter_speed)
    config['Camera']['iso'] = str(iso)
    config['Camera']['rotation'] = str(rotation)
    return config
    
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config = General_Config(config)
    config = Camera_Config(config)

    with open('Kronos.config', 'w') as configfile:
        config.write(configfile)
