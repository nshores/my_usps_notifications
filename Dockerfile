FROM ubuntu:16.04

MAINTAINER Nick Shores

#Install Python 3.6
RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

#install curl
RUN apt-get install curl wget

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

#Install imgrurpython
RUN pip install imgurpython

#Install MyUsps Library
RUN pip install myusps

#Clone myusps_notifications repo
RUN git clone https://github.com/nshores/my_usps_notifications.git

#Install Dependencies
RUN apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4


# Install Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

#Install Chrome Driver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE); wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/ 
RUN wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

#Start Main script which runs chromedriver and keeps container open
#TODO - Create main start script and loop

#Keep container online
CMD [ "sh", "-c", "service ssh start; bash"]
