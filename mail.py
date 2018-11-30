import myusps
import requests
import os
import json
import datetime
from pushbullet import Pushbullet


#pushbullet setup
pushbullet_enabled = os.environ.get('pushbullet_enabled')
if pushbullet_enabled == 1:
    pushbullet_key = os.environ.get('pushbullet_key')
    pb = Pushbullet(pushbullet_key)


#slack setup
webhook_url = os.environ.get('webhook_url')

def slack_post(webhook_url, slack_data):
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    return response

#setup imgur
from imgurpython import ImgurClient
imgur_client_id = "88476dd48e0ed08"
imgur_client_secret = "fe1128d77d7ea9d8d9d78805ffb943bbf63d82a2"

try:
    client = ImgurClient(imgur_client_id, imgur_client_secret)
except:
    print("Imgur is down, mail images will not show up")
    pass


# Establish a session.
username = os.environ.get('usps_username')
password = os.environ.get('usps_password')

# Use the login credentials you use to login to My USPS via the web.
# A login failure raises a `USPSError`.
# Using the Firefox driver here for selenium as it appears to be the most stable one at the moment. 
session = myusps.get_session(username, password, driver='firefox')


# Get all packages that My UPS knows about.
packages = myusps.get_packages(session)

#Check for packages that haven't been delivered yet
upcoming_packages = 0
for p in packages:
    tracking_number = p['tracking_number']
    delivery_date = p['delivery_date']
    primary_status = p['primary_status']
    #Skip delivered package
    if primary_status == "Delivered":
        continue
    upcoming_packages += 1


#Handle any packages in the queue
if upcoming_packages > 0:
    slack_text = (f"Number of upcoming USPS Package Items: {upcoming_packages}")
    slack_data = {"text": slack_text}
    slack_post(webhook_url, slack_data)
    for pkg in packages:
        #Check to make sure they have not been delivered
        tracking_number = pkg['tracking_number']
        primary_status = pkg['primary_status']
        secondary_status = pkg['secondary_status']
        delivery_date = pkg['delivery_date']
        present = datetime.datetime.now().date()
        if delivery_date is None:
            continue
        if present < delivery_date:
            print ("Tracking Number",pkg['tracking_number'])
            slack_text = (
            f"Tracking Number: {tracking_number}\n"
            f"Primary Status: {primary_status}\n"
            f"Secondary Status: {secondary_status}\n"
            f"Delivery Date: {delivery_date}\n"
            )
            slack_data = {"text": slack_text}
            slack_post(webhook_url, slack_data)

#No Packages set for delivery today or after today's date
else:
    print("No Packages in the queue for delivery!")
    slack_text= ("No USPS Package Items Today!")
    slack_data = {"text": slack_text}
    slack_post(webhook_url, slack_data)


# Get mail delivered today
mail = myusps.get_mail(session, datetime.datetime.now().date())

if len(mail) == 0:
    print("You have no mail today")
    #Post to pushbullet if enabled
    if pushbullet_enabled == 1:
        push = pb.push_note("MyUSPS", "No USPS Mail Items Today!")
    #post to slack
    slack_text= ("No USPS Mail Items Today!")
    slack_data = {"text": slack_text}
    slack_post(webhook_url, slack_data)

else:
    #Print number of mail items to console
    print (f"Number of Mail Items: {len(mail)}")
    mail_num = (f"Number of USPS Mail Items Today: {len(mail)}")
    #Post to pushbullet if enabled
    if pushbullet_enabled == 1:
        push = pb.push_note("MyUSPS", mail_num)
    slack_data = {"text": mail_num}
    slack_post(webhook_url, slack_data)

    #Post images of each mail item to slack / pushbullet
    for item in mail:
            print (f"ID:",item['id'])
            print (f"Image:",item['image'])
            print (f"Date:",item['date'])
            id = item['id']

            #Download Image of mail
            image = session.get(item['image'], allow_redirects=False)
            if image.status_code == 200:
                with open("mailpieceImg.jpg", 'wb') as f:
                    f.write(image.content)
        
            #upload to imgur
            imgurlink = client.upload_from_path("mailpieceImg.jpg", config=None, anon=True)
            print(imgurlink["link"])
            #Push to pushbullet if enabled
            if pushbullet_enabled == 1:
             push = pb.push_file(file_url=imgurlink["link"], file_name="mailpieceImg.jpg", file_type="image/jpeg")
            
            #construct slack message
            slack_data = {
            "attachments": [
            {
                "image_url": imgurlink["link"],
                "text": "",
            }
            ]
            }

            #Write to Slack channel via MyUsps Application webhook
            slack_post(webhook_url, slack_data)    




