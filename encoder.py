import sys
from PIL import Image

MAX_MSG_LEN = 63

# Load source
org_img = Image.open(sys.argv[1])

# Get source pixel map
org_pixelMap = org_img.load()

# Creating carrier
enc_img = Image.new( org_img.mode, org_img.size)
enc_pixelsMap = enc_img.load()

# Get hidden message
msg=input("Enter the message: ")
msg_len=len(msg)
msg+="."

# Image size and message length check
print("image size: {}".format(org_img.size))
print("msg_len: {}".format(msg_len))
if(msg_len > MAX_MSG_LEN):
    print("Error: Max message length can not exceed 63 characters. Exceeded characters will be discarded.")
if(org_img.size[0]*org_img.size[1]*3 <= MAX_MSG_LEN*4):
    print("Error: Image carrier size too small.")

# Traverse pixel map
msg_index=0
msg_pos=0
for row in range(org_img.size[0]):
    for col in range(org_img.size[1]):
        rgb=org_pixelMap[row,col] 
        r=rgb[0]
        g=rgb[1]
        b=rgb[2]

        # Allocate size of the message in first pixel
        if row==0 and col==0:
            enc_pixelsMap[row,col] = (r & 0b11111100 | ((msg_len & 0b00110000) >> 4),
                                    g & 0b11111100 | ((msg_len & 0b00001100) >> 2),
                                    b & 0b11111100 | (msg_len & 0b00000011))
        elif msg_index < msg_len:
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
