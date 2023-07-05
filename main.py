import time
import cv2
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
email_sender = ''
email_receiver = '' 
email_username = ''
email_password = '' # genarated app password for Gmail

# Set the path to the folder where images will be saved
image_folder = 'secimages'

# Set the interval in seconds
capture_interval = 3600  # 1 hour

# Create the image folder if it doesn't exist
os.makedirs(image_folder, exist_ok=True)

# Function to capture an image from the camera
def capture_image():
    print('Capturing image...')
    camera = cv2.VideoCapture(0)
    _, frame = camera.read()
    image_path = os.path.join(image_folder, 'image.jpg')
    cv2.imwrite(image_path, frame)
    camera.release()
    return image_path

def delete_image(image_path):
    print('Deleting image...')
    os.remove(image_path)

# Function to send an email with the captured image
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

# Main loop
while True:
    try:
        image_path = capture_image()
        send_email(image_path)
        delete_image(image_path)
    except Exception as e:
        print(f'An error occurred: {e}')

    print(f'Waiting {capture_interval} seconds...')
    time.sleep(capture_interval)
