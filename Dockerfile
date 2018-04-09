# A basic apache server. To use either add or bind mount content under /var/www
FROM ubuntu:16.04

MAINTAINER Nick Shores



#Install Python 3
RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update


#install curl
RUN sudo apt-get install curl

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

#Install MyUsps Library
RUN pip install myusps

#Clone myusps_notifications repo
RUN git clone https://github.com/nshores/my_usps_notifications.git


#Set Env Variables
ENV SELENIUM_STANDALONE_VERSION=3.4.0
RUN SELENIUM_SUBDIR=$(echo "$SELENIUM_STANDALONE_VERSION" | cut -d"." -f-2)
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`

#Install Dependencies
RUN sudo apt-get update
RUN sudo apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4


# Install Chrome.
RUN sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN sudo echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN sudo apt-get -y update
RUN sudo apt-get -y install google-chrome-stable

# Install ChromeDriver.
RUN wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN sudo chown root:root /usr/local/bin/chromedriver
RUN sudo chmod 0755 /usr/local/bin/chromedriver

# Install Selenium.
RUN wget -N http://selenium-release.storage.googleapis.com/$SELENIUM_SUBDIR/selenium-server-standalone-$SELENIUM_STANDALONE_VERSION.jar -P ~/
RUN sudo mv -f ~/selenium-server-standalone-$SELENIUM_STANDALONE_VERSION.jar /usr/local/bin/selenium-server-standalone.jar
RUN sudo chown root:root /usr/local/bin/selenium-server-standalone.jar
RUN sudo chmod 0755 /usr/local/bin/selenium-server-standalone.jar



CMD [""]
CMD [""]
