from datetime import datetime
import cv2
import glob
import os

# INPUTS

def_fps = 1
# source_folder = input('    Folder to collect images from (default cwd): ') or '01_14_2022'
source_folder_name = input('Folder to collect images from (default cwd):\n') or '01_15_2022'
# image_type    = input('            Image file extension (default .jpg): ') or '.jpg'
# if not '.' in image_type:
#     image_type = '.'+image_type
image_type = '.jpg'

cwd = os.getcwd() # get current working directory
if source_folder_name != cwd: # checks if the source folder is the cwd (so it wont double write cwd)
    source_folder = cwd+'\\Timelapses\\'+source_folder_name+'\\'

count = 0
for filename in sorted(glob.glob(source_folder+'\\*'+image_type)):
    count += 1
print('Photos identified:\n'+str(count))
video_name    = input('Name of timelapse file (default name of folder):\n') or source_folder_name
# video_type    = input('      Video file extension type (default .mp4v): ') or '.mp4v'
# if not '.' in video_type:
#     video_type = '.'+video_type
video_type = '.mp4v'
fps           = float(input('Timelapse frames per second (default '+str(def_fps)+ '):\n') or def_fps)

# SETUP
video_name += video_type

save_name = source_folder+video_name

# IMAGE PROCESSING
# count = 0 # DELETE
img_array = []
print('Making video')
for filename in sorted(glob.glob(source_folder+'\\*'+image_type)):
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
    color = (255, 255, 255) # Blue color in BGR
    thickness = 3 # Line thickness in px
    
    tl = (0, 0) # top left background corner
    br = (440, 80)
    cv2.rectangle(img, tl, br, (0,0,0), -1)
    img = cv2.putText(img, image_datetime, org, font, fontScale,
                      color, thickness, cv2.LINE_AA) # Using cv2.putText() method
    
    # count += 1 # DELETE
    img_array.append(img) # add image to array for video creation
    
# cv2.imshow('Image', img) # DELETE
# cv2.waitKey(0) # DELETE

# length = count # DELETE
# fps = count/length # DELETE
out = cv2.VideoWriter(save_name,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
print('Done!')
