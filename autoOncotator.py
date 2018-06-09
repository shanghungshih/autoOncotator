# -*- coding: utf-8 -*-
"""
Created on Thu June 03 22:07:31 2018

@author: Shang-Hung, Shih
"""

import os
import re
import time
import warnings
from selenium import webdriver
from multiprocessing import Pool


class autoOncotator:
    
    def __init__(self, mainPath, sleeptime, project):
        self.mainPath = mainPath
        self.sleeptime = sleeptime
        self.project = project
        
    def somaticMutect2_v3(self, project):
        project = str(project)
        path = os.path.join(os.getcwd())
        in_filename = project+".mutect2.vcf"
        in_file = os.path.join(path, in_filename)
        out_filename = project+".mutect2.filter.vcf"
        out_file = os.path.join(path, out_filename)
        out = open(out_file, 'w') 
        with open(in_file, 'r') as f:
            for i in f.readlines():
                if i.count('#') == 0:
                    if i.split(sep='\t')[0].split(sep='chr')[1].isnumeric() == True or i.split(sep='\t')[0].split(sep='chr')[1].endswith('X') == True or i.split(sep='\t')[0].split(sep='chr')[1].endswith('Y') == True:
                        if i.split(sep='\t')[2].startswith('rs') == False:
                            out.writelines(i)
        out.close()

    def vcf2oncotator(self, project):
        project = str(project)
        in_filename = project+".mutect2.filter.vcf"
        in_file = os.path.join(os.getcwd(), in_filename)
        out_filename = project+'.onco.tsv'
        out_file = os.path.join(os.getcwd(), out_filename)
        out = open(out_file, 'w')
        with open(in_file, 'r') as f:
            for l in f.readlines():
                if l.count('#') == 0:
                    if l.split(sep='\t')[0].split(sep='chr')[1].isnumeric() == True or l.split(sep='\t')[0].split(sep='chr')[1].endswith('X') == True or l.split(sep='\t')[0].split(sep='chr')[1].endswith('Y') == True:
                        if l.split(sep='\t')[2].startswith('rs') == False:
                            # SNV
                            if len(l.split(sep='\t')[3]) == 1 and len(l.split(sep='\t')[4]) == 1:
                                line = str(l.split(sep='\t')[0].split(sep='chr')[1])+'\t'+str(l.split(sep='\t')[1])+'\t'+str(l.split(sep='\t')[1])+'\t'+str(l.split(sep='\t')[3])+'\t'+str(l.split(sep='\t')[4])+'\n'
                                out.writelines(line)
                            # deletion
                            if len(l.split(sep='\t')[3]) != 1 and len(l.split(sep='\t')[4]) == 1:
                                line = str(l.split(sep='\t')[0].split(sep='chr')[1])+'\t'+str(int(l.split(sep='\t')[1])+1)+'\t'+str(int(l.split(sep='\t')[1])+len(l.split(sep='\t')[3][1:]))+'\t'+str(l.split(sep='\t')[3][1:])+'\t'+'-'+'\n'
                                out.writelines(line)
                            # insertion
                            if len(l.split(sep='\t')[3]) == 1 and len(l.split(sep='\t')[4]) != 1:
                                line = str(l.split(sep='\t')[0].split(sep='chr')[1])+'\t'+str(int(l.split(sep='\t')[1]))+'\t'+str(int(l.split(sep='\t')[1])+len(l.split(sep='\t')[4])-1)+'\t'+'-'+'\t'+str(l.split(sep='\t')[4][1:])+'\n'
                                out.writelines(line)
        out.close()

    def oncotatorCrawler(self, sleeptime, project, download):
        project = str(project)

        xpath = '/html/body/div[2]/div[3]/div[1]/a[1]'
        #download  = '/Users/shanghungshih/Downloads'

        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.dir', download)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/html')

        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get('http://portals.broadinstitute.org/oncotator/')

        while True:
            try:
                driver.find_element_by_id('id_file').send_keys(os.path.join(os.getcwd(), project+'.onco.tsv'))
                driver.find_element_by_name('upload_submit').click()
                time.sleep(100)
                #time.sleep(sleeptime*2+2)
                driver.find_element_by_xpath(xpath).click()
                time.sleep(4)
                os.system('mv %s %s' %(os.path.join(download, 'oncotator.maf.txt'), os.path.join(download, project+'.oncotator.maf.txt')))
                driver.close()
                break
            except:
                warnings.warn('oncotatorCrawler error occor.')

def getID():
    yn = input('Show all patient ID of sub directory?(Y/n) (ex. y): ')
    if yn.strip().lower() == 'y':
        print('Current directory: ' )
        os.system('pwd')
        path = input('Please enter the path to your vcf (ex. /home/bio608/OSCC/annotation/86xWES): ')
        prefix = input('Please enter the prefix (ex. 546.mutect2.vcf >>> .mutect2.vcf ): ')
        os.system('ls -lt %s > getID.txt' %(path))
        name = []
        with open('getID.txt', 'r') as f:
            for i in f.readlines():
                if i.split(' ')[-1:][0].replace('\n', '').endswith('vcf') is True:
                    if i.split(re.findall(' [0-9][0-9]:[0-9][0-9]', i)[0]+' ')[1].replace('i\n', '').count(prefix) != 0:
                        name.append(i.split(re.findall(' [0-9][0-9]:[0-9][0-9]', i)[0]+' ')[1].replace('\n', '').replace(prefix, ''))
        out = ('%s' %(name))
        print('>>>>>> total patient of %s : %s' %(path, len(name)))
        print(out.replace('[', '').replace(']', '').replace("'", ""))

        os.system('rm getID.txt')

def enterData():
    #subproject = 'tmp'
    patient = input('Please enter patient ID to add in analysis queue (ex. 599, 631, 632, 652): ').split(',')
    print('Current directory: ' )
    os.system('pwd')
    download = input('Please enter the path to download as: ')
    work = []
    for j, i in enumerate(patient):
        if (j+1) <= 5:
            work.append([(j*3), i.strip()])
        else:
            work.append([5, i.strip()])
    work = tuple(work)
    return work, download

getID()    
work, download =  enterData()
print(work)

def work_log(work_data):
    
    p1 = autoOncotator(os.getcwd(), work_data[0], work_data[1])
    
    p1.somaticMutect2_v3(p1.project)
    p1.vcf2oncotator(p1.project)
    startTime = time.time()
    p1.oncotatorCrawler(p1.sleeptime, p1.project, download)
    endTime = time.time()
    print('>>>>>> TotalTimeUse for patient=%s : %s sec' %(work_data[1], endTime-startTime))
def pool_handler():
    p = Pool(1)
    p.map(work_log, work)

if __name__ == '__main__':
   pool_handler()
