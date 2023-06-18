# vietnamese-news-crawler
Build Vietnamese news crawler service running on AWS

Websites:
- [Bao tuoi tre](https://tuoitre.vn/tin-moi-nhat.htm)

Author: Le Viet Nam

## Install prerequisites
```
cd /home/ubuntu
sudo apt-get update && apt-get install -y \
  fonts-liberation \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libatspi2.0-0 \
  libcups2 \
  libdbus-1-3 \
  libdrm2 \
  libgbm1 \
  libgtk-3-0 \
  libnspr4 \
  libnss3 \
  libwayland-client0 \
  libxcomposite1 \
  libxdamage1 \
  libxfixes3 \
  libxkbcommon0 \
  libxrandr2 \
  xdg-utils \
  libu2f-udev \
  libvulkan1 \
  libcurl3-gnutls \ 
  libcurl3-nss \
  libcurl4 \ 
  wget
```
```
sudo apt update && apt install -y \
  git \
  python3-pip \ 
  zip
```
## Download and install Google Chrome
```
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  dpkg -i google-chrome-stable_current_amd64.deb && \
  rm google-chrome-stable_current_amd64.deb
```
## Create python virtual environment
```
mkdir python3_venvs
python3 -m venv python3_venvs/vietnamese-news-crawler
source /home/ubuntu/python3_venvs/vietnamese-news-crawler/bin/activate
```
## Clone git repository
```
git clone https://github.com/namlv7197/vietnamese-news-crawler.git
```

## Download Chrome driver
```
  cd vietnamese-news-crawler && \
  wget https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip && \
  unzip chromedriver_linux64.zip -d chromedriver
```


