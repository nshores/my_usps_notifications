# Slack/Email/Pushbullet Notification module built around the MyUsps python library (https://github.com/happyleavesaoc/python-myusps)

**You need a free account at USPS Informed Delivery to use this -- https://informeddelivery.usps.com/box/pages/intro/start.action**

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

# Requirments for manual install
**Chromedriver https://sites.google.com/a/chromium.org/chromedriver/  
Google Chrome.  
USPS Informed Delivery Account.  
Python3.6.5 (For f-strings)  
Imgur API Key - Register imgur client here - https://api.imgur.com/oauth2/addclient  
imgurpython (`pip install imgurpython`  )  
Custom Slack application (https://api.slack.com/apps)**

# CLI output
```
root@33e223d445d7:/my_usps_notifications# python3.6 mail.py 
Number of Packages: 1
Tracking Number 9205596900893491619272
Number of Mail Items: 0

```


# Screenshots

![Alt text](https://raw.githubusercontent.com/nshores/my_usps_notifications/master/example.png?raw=true "Title")



