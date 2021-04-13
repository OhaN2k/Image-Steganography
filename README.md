# Assignment	on	Steganography
Write	a	program	for	encryption	and	decryption	in	steganography.
The	message:	student	name	1 - student	name	2 - student	name	3
Choose	a	file from	your	computer:	mp3	song,	png	picture,	…
Extract	the	message	to	appropriate	format,	insert	this	message	into	the	chosen	file.
Make	sure,	after	insert	the	message	into	the	file,	you	can	still	listen	mp3,	open	the	
picture.
Note:	you	need	to	propose	an	algorithm	for	insertion	the	message	into	the	chosen	
file.
Prove	that,	it	is	impossible,	or	very	difficult,	for	the	bad	people	if	they	want	to	take	
the	hidden	message	out.

### To start encoding message, type the following in python interpreter with any png image:
> python encoder.py source.png

The length of the message is hidden in only the first pixel, therefore the message length can't be more than 63 character.

### To get the hidden message out, use:
> python decoder.py
