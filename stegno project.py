from base64 import decode
from PIL import Image
import numpy as np
import cv2

def to_binary(data):
    if type(data) == str:
        p= ''.join([format(ord(x),'08b') for x in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(x,'08b') for x in data]
    return p


def hide_data(image , msg):
    msg+= '$$'
    b_msg = to_binary(msg)
    length = len(b_msg)
    index = 0

    for value in image:
        for pix in value:
            r,b,g = to_binary(pix)
            if index < length:
                pix[0] = int(r[:-1] + b_msg[index])
                index += 1
            if index < length:
                pix[1] = int(b[:-1] + b_msg[index])
                index += 1
            if index < length:
                pix[2] = int(g[:-1] + b_msg[index])
                index += 1
            if(index >= length):
                break
    return image



def encode():
    print("\nEnter Image name :")
    img_name = input()
    image = cv2.imread(img_name)
    img = Image.open(img_name,'r')

    w , h = img.size
    print("\nEnter message to hide :")
    msg = input()
    if(len(msg) == 0):
        raise ValueError("empty data to be hidden...")
    encoded_img = input("\nEnter encode image name :")
    encoded_data = hide_data(image,msg)

    cv2.imwrite(encoded_img , encoded_data)
    img1 = Image.open(encoded_img,'r')
    img1 = img1.resize((w,h) , Image.Resampling.LANCZOS)


def find_data(img):
    msg_bit=""
    for value in img:
        for pix in value:
            r,b,g= to_binary(pix)
            msg_bit += r[-1]
            msg_bit += b[-1]
            msg_bit += g[-1]
    all_msg_bit = [msg_bit[i:i+8] for i in range(0,len(msg_bit),8)]
    msg=""
    for i in all_msg_bit:
        msg += chr(int(i,2))
        if msg[-2:] == '$$':
            break
    return msg[:-2]



def decode():
    print("Enter name of the Image: ")
    img_name = input()
    img = cv2.imread(img_name)
    massage = find_data(img)
    return massage


def stegno():
    x = 1
    while x != 0:
       print('''\nImage stegnography
       1.encode
       2.decode''')
       u_in = int(input("\n enter your choice:"))
       if u_in == 1:
           encode()
       else:
           ans = decode()
           print("\n your message:"+ans)
       x = int(input("\nenter 1 for continue otherwise 0:"))

stegno()