# autoOncotator
automatically annotate vcf (variant call) file with Oncotator

http://portals.broadinstitute.org/oncotator/
- - -
## 1. download firefox
#### For Mac:
https://www.mozilla.org/zh-TW/firefox/new/

#### For Linux:
```
# download firefox
sudo apt install firefox
```

## 2. download geckodriver (v0.19.1)
https://github.com/mozilla/geckodriver/releases
```
# download geckodriver-v0.19.1
 wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
 
# unzip 
tar zxvf geckodriver-v0.19.1-linux64.tar.gz
 
# copy geckodriver to /usr/local/bin/
sudo cp geckodriver /usr/local/bin/
```

## 3. install selenium
```
# install pip3
sudo apt install python3-pip

# install package selenium
pip3 install selenium
```


## 4. copy autoOncotator_linux.py to your working directory
- - -

## Usage
#### for Linux and MacOS
```python
python3 autoOncotator.py
```
