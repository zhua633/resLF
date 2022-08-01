# Importing libraries
import numpy as np
import math
from PIL import Image    

filepath=r"C:\Users\Anvilly Huang\Documents\GitHub\resLF\Holograms"
samples=10
for n in range(1,samples):
    # Number of pixels
    S=4000
    I=np.zeros((S,S),dtype=np.float64)

    # Implement a function that randomises the size (width 1-2 pixels, length 3-5 pixels), rotation and relative position of the object of the centre by +- 10%
    # Size at the moment: 1x4
    for row in range(1000,1008):
        for col in range(2000,2004):
            I[row, col]=1

    I=np.float64(I)

    # Parameter setup
    M = len(I)
    deltax=3.7*10**(-6) #pixel pitch 0.001 cm (10 um)
    w=633*10**(-9); # wavelength 633 nm
    k0 = 2*math.pi/w

    # implement a function that adjust this value by +- 20%
    z=0.005*n; #25 cm, propagation distance

    # Step 1: simulation of propagation using the ASM
    deltaf=1/M/deltax

    x = list(range(1, M+1))
    C, R= np.meshgrid(x, x)

    # FORWARD PROPAGATION USING ASM
    Ref = 50*math.sqrt(np.mean(I))*np.exp(-1j*k0*z) #Reference wave 
    A01=np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(I))); #Spectrum first object

    p1=np.exp(-2j*math.pi*z*np.sqrt((1/w)**2-((R-M/2-1)*deltaf)**2-((C-M/2-1)*deltaf)**2))

    Az1=A01*p1#Propagating

    H1 = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(Az1)))

    # H1 = np.dot((abs(H1 + Ref)),(abs(H1 + Ref)))
    H1 = (abs(H1 + Ref))**2

    H1_=abs(H1)-np.amin(abs(H1))
    img1 = Image.fromarray(np.uint8((abs(H1_)/np.amax(abs(H1_))) * 255),'L')
    img1.save(f"{filepath}/H1_{n}.png")
    print('progressing, image',n+1,'/',samples)
    # width,height=H1.shape
    # img1.thumbnail((width/2,height/2), Image.ANTIALIAS)
    # img1.show()
    # img1.save(f"{filepath}/H2.png")




