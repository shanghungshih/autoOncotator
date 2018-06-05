# autoOncotator
automatically annotate vcf file (called by GATK3.8 Mutect2)

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

### 3. install selenium
```
# install pip3
sudo apt install python3-pip

# install package selenium
pip3 install selenium
```


## 4. copy to your working directory

### Usage
```python
python3 autoOncotator_mac
```
```python
python3 autoOncotator_linux
```
