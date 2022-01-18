# from calendar import month
from datetime import datetime
from multiprocessing.connection import wait
import time
import os
import math
from picamera import PiCamera
import configparser

def LoadConfig(config_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    
    Morning          = eval(config['General']['Morning'])
    Night            = eval(config['General']['Night'])
    image_freq       = eval(config['General']['image_freq'])
    start_time       =      config['General']['start_time']
    timelapse_length = eval(config['General']['timelapse_length'])
    picture_folder   =      config['General']['picture_folder']
    image_type       =      config['General']['image_type']
    
    camera = PiCamera()
    camera.resolution    = eval(config['Camera']['resolution'])
    camera.shutter_speed = eval(config['Camera']['shutter_speed'])
    camera.iso           = eval(config['Camera']['iso'])
    camera.rotation      = eval(config['Camera']['rotation'])
    
    return Morning, Night, image_freq, start_time, timelapse_length, picture_folder, image_type, camera

def Setup(Morning, Night, image_freq, start_time, timelapse_length, picture_folder):
    # SETUP
    image_freq = image_freq*60 #s/pic
    timelapse_length = timelapse_length*24*60*60 # s
    N = math.ceil(timelapse_length/image_freq*(Night-Morning)/24)
    main_directory = '/home/pi/Timelapses/' + picture_folder + '/'  # used for easier callback
    try:
        os.mkdir('/home/pi/Timelapses/')  # creates parent directory for all teams data
    except:
        pass

    try:
        os.mkdir(main_directory)  # creates a directory to save team data to
    except:
        print('Timelapse folder name has already been created. Continuing anyway.')
        pass

    # now_dt = datetime.now()
    # now_ep = round(now_dt.timestamp())
    
    start_time_dt = datetime.strptime(start_time,"%m/%d/%Y, %H:%M")
    start_time_ep = round(start_time_dt.timestamp())
    
    stop_time_ep = round(start_time_ep+timelapse_length)
    stop_time_dt = datetime.fromtimestamp(stop_time_ep)

    start_time_dt = start_time_dt.strftime("%m/%d/%Y, %H:%M:%S")
    # stop_time_dt = stop_time_dt.strftime("%m/%d/%Y, %H:%M:%S")

    current_time_ep = round(time.time())
    current_time_dt = datetime.fromtimestamp(current_time_ep)
    
    print('      Will take: '+str(N)+' photos (max)')
    print('Current time is: '+current_time_dt)
    print('  Completion at: '+stop_time_dt.strftime("%m/%d/%Y, %H:%M:%S"))
    time_remaining = stop_time_dt-current_time_dt
    print(' Time remaining: '+str(time_remaining))
    
    return image_freq, N, main_directory, start_time_ep, stop_time_ep, stop_time_dt

def Kronos(Morning, Night, image_freq, image_type, camera, N, main_directory, start_time_ep, stop_time_ep, stop_time_dt):
    try:
        current_time_ep = round(time.time())
        last_picture_ep = current_time_ep
        next_picture_ep = last_picture_ep+image_freq

        next_picture_dt = datetime.fromtimestamp(next_picture_ep)
        print('        Next at: '+next_picture_dt.strftime("%m/%d/%Y, %H:%M:%S"))
        count = 0
        Progress = open(main_directory+"Progress.txt",'w')
        L = ['Waiting to take first picture']
        Progress.writelines(L)
        Progress.close()
        
        while current_time_ep < start_time_ep:
            current_time_ep = round(time.time())
                    
        while current_time_ep < stop_time_ep:
            current_time_ep = round(time.time())
            current_time_dt = datetime.fromtimestamp(current_time_ep)
            today_dt = datetime.today()
            year = today_dt.year
            month = today_dt.month
            day = today_dt.day
            
            morning_cuttoff_dt = datetime(year,month,day,Morning,5)
            night_cuttoff_dt = datetime(year,month,day,Night-1,55)
            morning_cuttoff_ep = round(morning_cuttoff_dt.timestamp())
            night_cuttoff_ep = round(night_cuttoff_dt.timestamp())
            
            # check if lights are turned on
            if morning_cuttoff_ep < current_time_ep and night_cuttoff_ep > current_time_ep and current_time_ep > next_picture_ep:
                save_name = str(current_time_ep)+image_type
                camera.capture(main_directory+save_name)
                print(' ')
                print('Click!')

                count += 1
                last_picture_ep = current_time_ep
                next_picture_ep = last_picture_ep+image_freq
                next_picture_dt = datetime.fromtimestamp(next_picture_ep)
                
                print('Pictures taken: '+str(count)+'/'+str(N))
                print('       Time is: '+current_time_dt.strftime("%m/%d/%Y, %H:%M:%S"))
                print('       Next at: '+next_picture_dt.strftime("%m/%d/%Y, %H:%M:%S"))
                print(' Completion at: '+stop_time_dt.strftime("%m/%d/%Y, %H:%M:%S"))
                time_remaining = stop_time_dt-current_time_dt
                print('Time remaining: '+str(time_remaining))

                l1 = 'Pictures taken: '+str(count)+'/'+str(N)+'\n'
                l2 = '       Time is: '+current_time_dt.strftime("%m/%d/%Y, %H:%M:%S")+'\n'
                l3 = '       Next at: '+next_picture_dt.strftime("%m/%d/%Y, %H:%M:%S")+'\n'
                l4 = '   Stopping at: '+stop_time_dt.strftime("%m/%d/%Y, %H:%M:%S")+'\n'
                l5 = 'Time remaining: '+str(time_remaining)+'\n'
                
                Progress = open(main_directory+"Progress.txt",'w')
                L = [l1, l2, l3, l4, l5]
                Progress.writelines(L)
                Progress.close()

        Progress = open(main_directory+"Progress.txt",'w')
        L = ['Timelapse Completed at: '+current_time_dt.strftime("%m/%d/%Y, %H:%M:%S")]
        Progress.writelines(L)
        Progress.close()
        print('Timelapse Complete')
    except:
        Progress = open(main_directory+"Progress.txt",'w')
        L = ['An error ocurred at: '+current_time_dt.strftime("%m/%d/%Y, %H:%M:%S")]
        Progress.writelines(L)
        Progress.close()
        print('Error ocurred')

if __name__ == "__main__":
    config_name = 'Kronos.config'
    Morning, Night, image_freq, start_time, timelapse_length, picture_folder, image_type, camera = LoadConfig(config_name)
    image_freq, N, main_directory, start_time_ep, stop_time_ep, stop_time_dt = Setup(Morning, Night, image_freq, start_time, timelapse_length, picture_folder)
    Kronos(Morning, Night, image_freq, image_type, camera, N, main_directory, start_time_ep, stop_time_ep, stop_time_dt)
    