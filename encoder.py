import sys
import math
from PIL import Image

# Load source
org_img = Image.open(sys.argv[1])

nPixels = org_img.size[0] * org_img.size[1]
MAX_CHAR = math.floor(nPixels*3/4)
nSize = math.ceil(math.log(MAX_CHAR + 1, 10))
MAX_MSG_LEN = MAX_CHAR - nSize
print("Max message length: {} characters".format(MAX_MSG_LEN))

# Get source pixel map
org_pixelMap = org_img.load()

# Creating carrier
enc_img = Image.new( org_img.mode, org_img.size)
enc_pixelsMap = enc_img.load()

# Get hidden message
msg=input("Enter the message: ")
msg_len=len(msg)


# Image size and message length check

if(msg_len > MAX_MSG_LEN):
    print("WARNING! Image size too small, the messenge will be truncated.")
    msg = msg[0:MAX_MSG_LEN]
    msg_len = MAX_MSG_LEN
print("Message length: {}".format(msg_len))

msg = str(msg_len).zfill(nSize) + msg
msg+="."

# Traverse pixel map
msg_index=0
msg_pos=0
for row in range(org_img.size[0]):
    for col in range(org_img.size[1]):
        rgb=org_pixelMap[row,col] 
        r=rgb[0]
        g=rgb[1]
        b=rgb[2]

        if msg_index < msg_len + nSize:
            c1=msg[msg_index]
            c2=msg[msg_index+1]
            c1_ascii=ord(c1)
            c2_ascii=ord(c2)
            if msg_pos==0:
                enc_pixelsMap[row,col] = (r & 0b11111100 | ((c1_ascii & 0b11000000) >> 6),
                                    g & 0b11111100 | ((c1_ascii & 0b00110000) >> 4),
                                    b & 0b11111100 | ((c1_ascii & 0b00001100) >> 2))
            elif msg_pos==1:
                enc_pixelsMap[row,col] = (r & 0b11111100 | (c1_ascii & 0b00000011),
                                    g & 0b11111100 | ((c2_ascii & 0b11000000) >> 6),
                                    b & 0b11111100 | ((c2_ascii & 0b00110000) >> 4))
            elif msg_pos==2:
                enc_pixelsMap[row,col] = (r & 0b11111100 | ((c1_ascii & 0b00001100) >> 2),
                                    g & 0b11111100 | (c1_ascii & 0b00000011),
                                    b & 0b11111100 | ((c2_ascii & 0b11000000) >> 6))
            else:
                enc_pixelsMap[row,col] = (r & 0b11111100 | ((c1_ascii & 0b00110000) >> 4),
                                    g & 0b11111100 | ((c1_ascii & 0b00001100) >> 2),
                                    b & 0b11111100 | (c1_ascii & 0b00000011))
            
            if msg_pos in [1,2,3]:
                msg_index += 1
            msg_pos = (msg_pos+1) % 4
        else:
            enc_pixelsMap[row,col] = (r,g,b)

org_img.close()
enc_img.show()  

# Save carrier        
enc_img.save("carrier.png") 
enc_img.close()
