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

if len(packages) == 0:
    print ("You have no packages right now")
    slack_text= ("No USPS Packages Today!")
    slack_data = {"text": slack_text}
    slack_post(webhook_url, slack_data)
else:
    print (f"Number of Packages: {len(packages)}")
    for pkg in packages:
        print (f"Tracking Number",pkg['tracking_number'])

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




