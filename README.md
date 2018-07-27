# autoOncotator
> Python programs for automatically annotate vcf (variant call) file with Oncotator by selenium webdriver
> http://portals.broadinstitute.org/oncotator/

## Prerequisite
* Python 3.6

## Installation
``` shell
git clone https://github.com/shanghungshih/autoOncotator.git
```
## Internal Dependencies
### 1. download firefox
#### For Mac:
https://www.mozilla.org/zh-TW/firefox/new/

#### For Linux:
```
# download firefox
sudo apt install firefox
```

### 2. download geckodriver (v0.19.1)
https://github.com/mozilla/geckodriver/releases
```
# download geckodriver-v0.19.1
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
 
# unzip 
tar zxvf geckodriver-v0.19.1-linux64.tar.gz
 
# copy geckodriver to /usr/local/bin/
sudo cp geckodriver /usr/local/bin/
```

### 3. install selenium (v3.12.0)
```
# install pip3
sudo apt install python3-pip

# install package selenium
pip3 install selenium==3.12.0
```

## Current Functions
* `--vcf` - Variant call file, vcf format
* `--input_dir` - input directory (default: current working directory)
* `--output_dir` - output directory (default: current working directory)
* `--tsv` - Generate the input format file for Oncotator, you can defined the name of the file (default: tsv)
* `--maf` - output file name (default: oncotator.maf.txt)
* `--list_id` - list all vcf files in specified directory
* `--pool_size` - Pool size of multi-thread for parallel computing (default: 1)

## Quick start
### list all vcfs in specified directory (e.g. current working directory)
```
python3 autoOncotator.py -l .
```

### for running one vcf file
```
python3 autoOncotator.py -v test_562.mutect2.vcf
```

### for Parallelly running mutiple vcf files (e.g. pool size = 10)
* Notes: 'NO SPACE' between vcf files
```
python3 autoOncotator.py -p 10 -v test_562.mutect2.vcf,test_553.mutect2.vcf,test_546.mutect2.vcf,test_543.mutect2.vcf,test_556.mutect2.vcf,test_544.mutect2.vcf,test_573.mutect2.vcf,test_548.mutect2.vcf,test_579.mutect2.vcf,test_565.mutect2.vcf
```
