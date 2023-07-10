import time
import cv2
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import win32gui
import win32con

# Email configuration
smtp_server = ''
smtp_port = 587
email_sender = ''
email_receiver = ''
email_username = ''
email_password = ''  # generated app password for Gmail

# Set the path to the folder where images will be saved
image_folder = 'secimages'

# Set the interval in seconds
capture_interval = 2000

# Set the maximum number of capture attempts
max_capture_attempts = 3

# Create the image folder if it doesn't exist
os.makedirs(image_folder, exist_ok=True)

##################################################################
# Functions
##################################################################
def capture_image():
    print('Capturing image...')
    camera = cv2.VideoCapture(0)
    attempt = 0
    while attempt < max_capture_attempts:
        _, frame = camera.read()
        if frame is not None:
            camera.release()
            image_path = os.path.join(image_folder, 'image.jpg')
            cv2.imwrite(image_path, frame)
            return image_path
        attempt += 1
    camera.release()
    raise Exception('Failed to capture image')

def delete_image(image_path):
    print('Deleting image...')
    os.remove(image_path)

def send_email(image_path):
    print('Sending email...')
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = 'Sec Image'
    # Attach the image to the email
    with open(image_path, 'rb') as file:
        img = MIMEImage(file.read())
        img.add_header('Content-Disposition', 'attachment', filename='image.jpg')
        msg.attach(img)
    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_username, email_password)
        server.send_message(msg)

def turn_on_screen():
    # Turn on the screenC
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 1)

def turn_off_screen():
    # Turn off the screen
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)


##################################################################
# Main
##################################################################
while True:
    try:
        turn_on_screen() # hack around (
        image_path = capture_image()
        turn_on_screen()


        time.sleep(2)
        send_email(image_path)


        time.sleep(2)
        delete_image(image_path)


    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        print(f'Waiting {capture_interval} seconds...')
        turn_off_screen()
        time.sleep(capture_interval)