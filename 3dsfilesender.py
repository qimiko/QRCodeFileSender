from http.server import BaseHTTPRequestHandler, HTTPServer
import mimetypes, socket, urllib, qrcode, os, argparse, sys

#create parser arguments (probably can be simplified)

parser = argparse.ArgumentParser(
    description="Hosts a file for easy 3DS downloading.",
     prog='3DS File Sender',
     epilog="<o/")

parser.add_argument(
  "--file","-f", help="File to use (if not specified, a file picker will be opened.)")

parser.add_argument(
  "--ip","-ip", help="IP to use (if not specified, your computer's local ip will be chosen)")

parser.add_argument(
  "--port","-p", help="Port to use (if not specified, port 80 will be chosen)", type=int)

qrgroup = parser.add_mutually_exclusive_group()

qrgroup.add_argument(
    "--show", "-s", help="Shows image instead of printing to console (requires GUI!)", action="store_true")

qrgroup.add_argument(
    "--invert", "-i", help="Invert colors on ASCII QR code", action="store_true")


args = parser.parse_args()


# get port for some wicked port checking stuff
port = 80

if args.port:
  port = args.port

if (sys.platform == "linux" or sys.platform == "linux2") and port < 1024:
  print("Notice: ports over 1024 require root perms unless otherwise done\n" +
  "If you're running using sudo or noticing permission errors, consider changing the port\n")



if args.file:
  path = args.file
else:

  import tkinter

  from tkinter.filedialog import askopenfilename

  tkinter.Tk().withdraw() 
  
  path = askopenfilename()

if not os.path.isfile(path):
  raise FileNotFoundError("Selected path does not exist as a file!")

filename = os.path.basename(path)

# url name for file (gives the 3DS the filename/extension to store and act upon)
pathtofile = urllib.parse.quote_plus(filename)

if args.ip:
  currentip = args.ip
else:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
      s.connect(('10.255.255.255', 1))
      currentip = s.getsockname()[0]
  except:
      currentip = '127.0.0.1'
  finally:
      s.close()

def print_statusline(msg: str):

    last_msg_length = len(print_statusline.last_msg) if hasattr(
        print_statusline, 'last_msg') else 0

    print(' ' * last_msg_length, end='\r')
    print(msg, end='\r')

    sys.stdout.flush()
    print_statusline.last_msg = msg

#print(path)

#print(size)
 
# HTTPRequestHandler class
class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
    try:

      # Send the okay code
      self.send_response(200)

      # headers
      self.send_header('Content-Type', mimetypes.guess_type(path)[1]) #type for some reason
      self.send_header('Content-Length', os.path.getsize(path)) #size for progress bars
      self.end_headers()

      file = open(path, 'rb') # path accessed by url reallllly doesn't matter does it

      self.wfile.write(file.read())
		
      file.close()
      
      return
 
    except IOError:
      self.send_error(404, '404 - File not found') # since it doesn't exist i guess someone was careless weren't they

  def log_message(self, format, *args):
    print_statusline("New Request at %s" %
                     (self.log_date_time_string()))
    return

 
def run():

  print_statusline('starting server...')
 
  # Server settings

  server_address = (currentip, port)

  try:
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
  except socket.gaierror as e:
    raise TypeError("%s (IP address or port is incorrect!)" % (e))

  print('running server..., go to %s:%d\\%s\nPress ^C (CTRL C) to exit' %
    (currentip, port, pathtofile)) #print because the status stuff doesn't support newline


  qrimg = qrcode.QRCode()
  qrimg.add_data('http://%s:%d/%s' % 
    (currentip, port, pathtofile))
  
  if not args.show:
    qrimg.print_ascii(invert=args.invert)
  else:
    qrshow = qrimg.make_image()
    qrshow.show()

  try:
    httpd.serve_forever()
  except (KeyboardInterrupt, SystemExit):
    httpd.shutdown()
    httpd.socket.close()
    print("\n")

run()
