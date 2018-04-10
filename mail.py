import myusps
import requests
import os
import json



#slack
webhook_url = os.environ.get('webhook_url')

#imugr
from imgurpython import ImgurClient
imgur_client_id = "88476dd48e0ed08"
imgur_client_secret = "fe1128d77d7ea9d8d9d78805ffb943bbf63d82a2"
client = ImgurClient(imgur_client_id, imgur_client_secret)


# Establish a session.
username = os.environ.get('usps_username')
password = os.environ.get('usps_password')

# Use the login credentials you use to login to My USPS via the web.
# A login failure raises a `USPSError`.
#TODO Add check for windows/linux. If linux, use Chrome NOT phantomJS
session = myusps.get_session(username, password, driver='chrome')


# Get all packages that My UPS knows about.
packages = myusps.get_packages(session)

print (f"Number of Packages: {len(packages)}")
for pkg in packages:
        print (f"Tracking Number",pkg['tracking_number'])

# Get mail delivered today
import datetime
mail = myusps.get_mail(session, datetime.datetime.now().date())


print (f"Number of Mail Items: {len(mail)}")

mail_num = (f"Number of Mail Items Today: {len(mail)}")
slack_data = {"text": mail_num}


response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)


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
        response = requests.post(
        webhook_url, data=json.dumps(slack_data),
         headers={'Content-Type': 'application/json'}
        )       




