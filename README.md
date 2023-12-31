# vietnamese-news-crawler
Build Vietnamese news crawler service running on AWS

Websites:
- [Bao tuoi tre](https://tuoitre.vn/tin-moi-nhat.htm)

Author: Le Viet Nam

## Download and install Google Chrome
```
cd /home/ubuntu
sudo apt-get update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```
If an error occurs during installation ```dpkg -i google-chrome-stable_current_amd64.deb```, run the following command and then reinstall.
```
sudo apt --fix-broken install -y
```
## Clone git repository
```
git clone https://github.com/namlv7197/vietnamese-news-crawler.git
```
## Install python virtual environment
```
sudo apt update && apt install -y zip python3-venv
```
## Create python virtual environment
```
mkdir python3_venvs
python3 -m venv python3_venvs/vietnamese-news-crawler
source /home/ubuntu/python3_venvs/vietnamese-news-crawler/bin/activate
```
## Download Chrome driver
```
cd vietnamese-news-crawler
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d chromedriver
```
## Install python libraries
```
pip install -r requirements.txt
```


