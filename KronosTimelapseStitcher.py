from datetime import datetime
from email.mime import image
import cv2
import glob
import os
import sys
import math
from skimage import exposure

# INPUTS

def_fps = 1
# source_folder = input('    Folder to collect images from (default cwd): ') or '01_14_2022'
source_folder_name = input('\nFolder to collect images from:\n') or '01_17_2022'
# image_type    = input('            Image file extension (default .jpg): ') or '.jpg'
# if not '.' in image_type:
#     image_type = '.'+image_type
image_type = '.jpg'

cwd = os.getcwd() # get current working directory
if source_folder_name != cwd: # checks if the source folder is the cwd (so it wont double write cwd)
    source_folder = cwd+'\\Timelapses\\'+source_folder_name+'\\'

count = 0
for filename in sorted(glob.glob(source_folder+'\\*'+image_type)):
    if not 'reference' in filename:
        count += 1
total = count
print('\nPhotos identified:\n'+str(total))
video_name    = input('\nName of timelapse file (default name of folder):\n') or source_folder_name
# video_type    = input('      Video file extension type (default .mp4v): ') or '.mp4v'
# if not '.' in video_type:
#     video_type = '.'+video_type
video_type = '.mp4v'
fps           = float(input('\nTimelapse frames per second (default '+str(def_fps)+ '):\n') or def_fps)

# color_correct = input('\nApply color correction? Y/n or 1/0\n') or 1
# if color_correct == 'Y' or color_correct == 'y':
#     color_correct = 1
# else:
#     color_correct = 0
# print(' ')

# SETUP
video_name += video_type

save_name = source_folder+video_name

# IMAGE PROCESSING
count = 0
img_array = []
print('Making video')
for filename in sorted(glob.glob(source_folder+'\\*'+image_type)):
    if not 'reference' in filename: 
        # get time that image was taken
        start = filename.rfind('\\')+1
        end = filename.rfind(image_type)
        image_epoch = int(filename[start:end])
        image_datetime = datetime.fromtimestamp(image_epoch)
        image_datetime = image_datetime.strftime("%m/%d/%Y, %H:%M:%S") # string to add to image

        img = cv2.imread(filename) # read image
        height, width, layers = img.shape # get image size
        size = (width,height)
        
        margin = 0.05
        font = cv2.FONT_HERSHEY_SIMPLEX # font
        # org = (round(margin*height), round(margin*height)) # org of bottom left corner of text box from top left corner
        org = (30,50)
        fontScale = 1 # fontScale
        color = (255, 255, 255) # font color in BGR
        thickness = 3 # Line thickness in px
        
        tl = (0, 0) # top left background corner
        br = (440, 80)
        cv2.rectangle(img, tl, br, (0,0,0), -1)
        img = cv2.putText(img, image_datetime, org, font, fontScale, color, thickness, cv2.LINE_AA) # Using cv2.putText() method
        
        img_array.append(img) # add image to array for video creation
        
        load_length = 30
        prog = load_length*count/total
        to_print = '█'*math.floor(prog)+' '*math.floor(load_length-prog)
        print('|'+to_print+'| '+str(count)+'/'+str(total)+' photos processed')
        sys.stdout.write("\033[F") # Cursor up one line
        count += 1

print('|'+to_print+'| '+str(count)+'/'+str(total))
# cv2.imshow('Image', img) # DELETE
# cv2.waitKey(0) # DELETE

# length = count # DELETE
# fps = count/length # DELETE
out = cv2.VideoWriter(save_name,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

print('Done!')
