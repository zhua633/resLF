
# Importing Image class from PIL module
from PIL import Image
import cv2
from os.path import isfile, join
from os import listdir
import numpy as np


def imgcrop():
    # Opens a image in RGB mode
    im = Image.open(r"C:\Users\Anvilly Huang\Documents\GitHub\resLF\img\croppedlong.png")
    # Setting the points for cropped image
    left = 25
    top = 25
    right = 289
    bottom = 132

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
    
    # Shows the image in image viewer
    im1.save(f"{filepath}\cropped.png") 
    im1.show()


def preprocessing():
    im = cv2.imread(r"C:\Users\Anvilly Huang\Documents\GitHub\resLF\img\orig.png")
    (height, width) = im.shape[:2]
    filepath=r"C:\Users\Anvilly Huang\Documents\GitHub\resLF\img"

    # Size of the image in pixels (size of original image)
    # im = Image.open(r"C:\Users\Anvilly Huang\Documents\GitHub\resLF\img\cropped.png")
    # width, height = im.size
    croplength=50

    # Adding padding so the image can be divided into 50x50 images 
    width_padding=croplength-(width%croplength)
    height_padding=croplength-(height%croplength)

    image = cv2.copyMakeBorder(im, 0,height_padding+1, 0, width_padding+1, cv2.BORDER_CONSTANT, None, value = 0)
    cv2.imwrite(f'{filepath}\padded.png',image)

    (new_height,new_width)=image.shape[:2]
    img_no=(new_width/croplength)*(new_height/croplength)

    print('There will be',img_no,'images')
    print('It will take approx',img_no*40/60,'minutes to process')

    for n in range(0, int(img_no)+1):
        # Setting the points for cropped image
        left = 0+(n%int((new_width/50)-1))*50
        top = int(n/(new_width/50))*50
        right = int(left+50)
        bottom = int(top+50)
        print(left,right,top,bottom)

        # Cropped image of above dimension
        # im1 = im.crop((left, top, right, bottom))
        
        crop_img = image[top:bottom,left:right]
        cv2.imwrite(f'{filepath}\cropped{n}.png',crop_img)
        # print('image',n,'out of',img_no)
        

def stitch2():
    filepath=r"C:\Users\Anvilly Huang\Documents\GitHub\resLF\results"
    imgfile=  [f for f in listdir(filepath) if (isfile(join(filepath,f)) and f.startswith("processed"))]

    im = cv2.imread(r"C:\Users\Anvilly Huang\Documents\GitHub\resLF\img\padded.png")
    (height, width) = im.shape[:2]
    new_width=(width-1)*4
    new_height=(height-1)*4

    # Creating 2D mesh that's 4 times the resolution
    # pic= Image.new('RGB', (new_width, new_height))
    
    # pic= Image.new('RGB', (400,200))
    img = np.empty(len(imgfile), dtype = object)
    for n in range(0, len(imgfile)):
        # img[n] = Image.open(join(filepath, imgfile[n]))
        img[n] = cv2.imread(join(filepath, imgfile[n]))
    
    row0=np.concatenate((img[0],img[1],img[2],img[3],img[4],img[5]), axis=1)
    row1=np.concatenate((img[6],img[7],img[8],img[9],img[10],img[11]), axis=1)
    row2=np.concatenate((img[12],img[13],img[14],img[15],img[16],img[17]), axis=1)
    pic=np.concatenate((row0,row1,row2),axis=0)
    print(pic.shape)
    cv2.imwrite('final.png',pic)
    # pic.save(f'{filepath}\final.png')
    cv2.imshow('image',pic)
    cv2.waitKey(0)
    


        

filepath=r"C:\Users\Anvilly Huang\Documents\GitHub\resLF\img"
# imglist=  [f for f in listdir(filepath) if (isfile(join(filepath,f)) and f.startswith("cropped"))]

# imgcrop()
# preprocessing()
stitch2()