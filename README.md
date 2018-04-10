# Slack Notification module built around the MyUsps python library (https://github.com/happyleavesaoc/python-myusps)

# Install Instructions 
```sudo docker pull nshores/my_usps_notifications```  
```sudo docker run nshores/my_usps_notifications```  

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



