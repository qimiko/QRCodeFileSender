# QRCodeFileSender
script made for the purpose of sending files to the 3ds using qr codes (for quick development of CIA files)

command line python script (requires 3.x)!!!!!!!!!!!

## arguments

--file FILE, -f FILE  File to use (if not specified, a file picker will be opened.)
--ip IP, -ip IP       IP to use (if not specified, your computer's local ip will be chosen)
--port PORT, -p PORT  Port to use (if not specified, port 80 will be chosen)
--show, -s            Shows image instead of printing to console (requires a GUI!)
--invert, -i          Invert colors on ASCII QR code if you use a black on white configuration

### example use:
```python3 ~/3dsfilesender.py -f homebrew.cia -p 8080 -i```

## required modules:
* qrcode

### optional modules:
* tkinter when not using the -f argument (may be removed)

# Notices
ports under 1024 require sudo perms on linux machines, so just change the port to something above it to avoid it (i use 8080)
there may be some slight things that go wrong idk
