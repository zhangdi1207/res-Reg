from PIL import Image,ImageFilter
import numpy as np

total=0
def clearNoise(im,N,Z):
    #N,number of dot around it,below it define the dot is 1
    #Z,number of clearTime
    for x in range(0,im.size[0],1):
        im.putpixel((x,im.size[1]-1),255)
    for y in range(0,im.size[1],1):
        im.putpixel((im.size[0]-1,y),255) 
    for i in range(Z):
        for x in range(2,im.size[0]-2,1):
            for y in range(2,im.size[1]-2,1):
                nearDot=0
                if im.getpixel((x,y))==0:
                    for nearx in range(-2,3,1):
                        for neary in range(-2,3,1):
                            if(im.getpixel((x+nearx,y+neary))==0):
                                nearDot+=1
                    if nearDot<N:
                        im.putpixel((x,y),255)
def getAngle(im):
    left=[im.size[0]-1,im.size[1]-1]
    right=[0,0]
    for x in range(0,im.size[0],1):
        for y in range(0,im.size[1],1):
            if im.getpixel((x,y))==0:
                if x<left[0]:
                    left=[x,y]
                if x>right[0]:
                    right=[x,y]
    return np.arctan((right[1]-left[1])/(right[0]-left[0]))*180/np.pi


def myRotate(angle,im):
    im2=im.convert("RGBA")
    rot=im2.rotate(angle,expand=1)
    fff=Image.new('RGBA',rot.size,(255,)*4)
    out=Image.composite(rot,fff,rot)
    return out

def findColor(im):
    imB=im.filter(ImageFilter.CONTOUR).convert('1')
    #imB.show()
    print(imB.size)
    clearNoise(imB,4,1)
    angle1 = getAngle(imB)
    imB=myRotate(angle1,imB).convert('1')
    #imB.show()
    angle2 = getAngle(imB)
    imB=myRotate(angle2,imB)
    
    #clearNoise(imB,4,1)
    imTest = im.filter(ImageFilter.CONTOUR)
    imTest = myRotate(angle1+angle2,imTest)
    #imTest.show()

    im=im.rotate(angle1)
    im=im.rotate(angle2)
    imB.convert('1').save("1.jpg")
    im.save("2.jpg")

    
    #寻找最高点
    high=[im.size[0]-1,im.size[1]-1]
    for y in range(0,im.size[1],1):
        for x in range(0,im.size[0],1):
            if im.getpixel((x,y))==0:
                high=[x,y]
                break
        if high != [im.size[0]-1,im.size[1]-1]:
            break
    





im=Image.open("timg.jpg")
findColor(im)