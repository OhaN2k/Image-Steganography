import math
from PIL import Image

# Load image
enc_img = Image.open('carrier.png')

nPixels = enc_img.size[0] * enc_img.size[1]
MAX_CHAR = math.floor(nPixels*3/4)
nSize = math.ceil(math.log(MAX_CHAR + 1, 10))
MAX_MSG_LEN = MAX_CHAR - nSize

# Get pixel map
enc_pixelMap = enc_img.load()

msg = ""
msg_index = 0
msg_pos=0

# Traverse pixel map
for row in range(enc_img.size[0]):
    for col in range(enc_img.size[1]):
        rgb = enc_pixelMap[row,col]
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]

        if msg_pos==0:
            c = ((r & 0b00000011) << 6) + ((g & 0b00000011) << 4) + ((b & 0b00000011) << 2)
        elif msg_pos==1:
            c += r & 0b00000011
            msg += chr(c)
            c = ((g & 0b00000011) << 6) + ((b & 0b00000011) << 4)
        elif msg_pos==2:
            c += ((r & 0b00000011) << 2) + (g & 0b00000011)
            msg += chr(c)
            c = (b & 0b00000011) << 6
        else:
            c += ((r & 0b00000011) << 4) + ((g & 0b00000011) << 2) + (b & 0b00000011)
            msg += chr(c)
        
        if msg_pos in [1,2,3]:
            msg_index += 1
        msg_pos = (msg_pos+1) % 4       

enc_img.close()

msg_len = int(msg[0:nSize])
print("Message length:", msg_len)
msg = msg[nSize:msg_len+nSize]
print ("The hidden message is:", msg)