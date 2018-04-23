# Slack/Email/Pushbullet Notification module built around the [MyUsps python library](https://github.com/happyleavesaoc/python-myusps)


# CLI output
```
root@33e223d445d7:/my_usps_notifications# python3.6 mail.py 
Number of Packages: 1
Tracking Number 9205596900893491619272
Number of Mail Items: 0

```


# Screenshots

![Alt text](https://raw.githubusercontent.com/nshores/my_usps_notifications/master/example.png?raw=true "Title")


**You need a free account at [USPS Informed Delivery](https://informeddelivery.usps.com/box/pages/intro/start.action) to use this --**

# Install Instructions 
```sudo docker pull nshores/my_usps_notifications```  

After pulling, you can either edit the included ```docker_run.sh``` script with your enviormental variables and run that, or run it directly from the command line as seen below. After running it for the first time, you can simply run ```sudo docker start myusps_notifications``` whenever you like. I recomend you schedule it to run daily with crontab.

```sudo docker run -name myusps_notifications -e webhook_url="XXXX" -e usps_username="XXXX" -e usps_password="XXXX" nshores/my_usps_notifications```  


## Environment Variables


| Docker Environment Var. | Description |
| ----------------------- | ----------- |
| `-e webhook_url="XXXX"`<br/> **Required** | Set to your SlackWebhook URL (https://get.slack.help/hc/en-us/articles/115005265063-Incoming-WebHooks-for-Slack#set-up-incoming-webhooks)
| `-e usps_username="XXXX"`<br/> **Required** | Set to your https://informeddelivery.usps.com/ Username
| `-e usps_password="XXXX"`<br/> **Required** | Set to your https://informeddelivery.usps.com/ password
| `-e pushbullet_enabled="XXXX"`<br/> | Set to "1" for enabling pushbullet support
| `-e pushbullet_key="XXXX"`<br/> | Set your pushbullet api key here (Founder under https://www.pushbullet.com/#settings/account - Access tokens)

# Requirments for manual install

  * Register a webhook in your slack channel   - [Custom Slack application](https://api.slack.com/apps)  
  * Obtain Imgur API Key - [Register imgur client here](https://api.imgur.com/oauth2/addclient)  

Install the folowing --

[GeckoDriver](https://github.com/mozilla/geckodriver/releases)  
Firefox v59  
Selenium 3.11 (`pip install selenium`)
USPS Informed Delivery Account.  
Python3.6   
imgurpython (`pip install imgurpython`  )  
Pushbullet Python Library (`pip install pushbullet.py`)



