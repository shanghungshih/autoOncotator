#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 22:46:11 2018

@author: shanghungshih
"""

import os
import time
import warnings
import argparse
import logging
import random
from textwrap import dedent
from selenium import webdriver
from multiprocessing import Pool


logger_stderr = logging.getLogger(__name__+'stderr')
logger_stderr.setLevel(logging.INFO)
stderr_handler = logging.StreamHandler()
stderr_handler.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
logger_stderr.addHandler(stderr_handler)
logger_null = logging.getLogger(__name__+'null')
null_handler = logging.NullHandler()
logger_null.addHandler(null_handler)

VERSION = (1, 0, 0)
__version__ = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])

class autoOncotator:
    
    def __init__(self, filesize, project, input_dir, output_dir, tsv, maf, num):
        self.filesize = filesize
        self.project = project
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.tsv = project.replace('.vcf', '.'+tsv)
        self.maf = maf
        self.num = num
        
    def remove_snp(self, project, input_dir, output_dir):
        in_file = os.path.join(input_dir, project)
        out_file = os.path.join(output_dir, project.replace('.vcf', '.filter.vcf'))
        out = open(out_file, 'w+') 
        with open(in_file, 'r') as f:
            for i in f.readlines():
                if i.count('#') == 0:
                    if i.split(sep='\t')[0].split(sep='chr')[1].isnumeric() == True or i.split(sep='\t')[0].split(sep='chr')[1].endswith('X') == True or i.split(sep='\t')[0].split(sep='chr')[1].endswith('Y') == True:
                        if i.split(sep='\t')[2].startswith('rs') == False:
                            out.writelines(i)
        out.close()
        
    def vcf2oncotator(self, project, output_dir, tsv):
        in_file = os.path.join(output_dir, project.replace('.vcf', '.filter.vcf'))
        out_file = os.path.join(os.getcwd(), tsv)
        out = open(out_file, 'w+')
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
        
    def oncotator(self, filesize, project, output_dir, tsv, maf, num):
        fail = []
        xpath = '/html/body/div[2]/div[3]/div[1]/a[1]'

        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.dir', output_dir)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/html')

        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get('http://portals.broadinstitute.org/oncotator/')
        
        driver.find_element_by_id('id_file').send_keys(os.path.join(os.getcwd(), tsv))
        driver.find_element_by_name('upload_submit').click()
        if int(filesize) > 7500000:
            while True:
                try:
                    time.sleep(480)
                    driver.find_element_by_xpath(xpath).click()
                    time.sleep(45)
                    #if num == 0:
                    #    os.system('mv %s %s' %(os.path.join(output_dir, 'oncotator.maf.txt'), os.path.join(output_dir, project.replace('.vcf', '.'+maf))))
                    #else:
                    #    os.system('mv %s %s' %(os.path.join(output_dir, 'oncotator.maf{}.txt'.format('(%s)' %(num)), os.path.join(output_dir, project.replace('.vcf', '.'+maf)))))
                    time.sleep(5*num)
                    break
                except:
                    fail.append(project)
                    warnings.warn('selenium webdriver error occor: [%s]' %(project))
        else:
            while True:
                try:
                    time.sleep(240)
                    driver.find_element_by_xpath(xpath).click()
                    time.sleep(10)
                    #if num == 0:
                    #    os.system('mv %s %s' %(os.path.join(output_dir, 'oncotator.maf.txt'), os.path.join(output_dir, project.replace('.vcf', '.'+maf))))
                    #else:
                    #    os.system('mv %s %s' %(os.path.join(output_dir, 'oncotator.maf{}.txt'.format('(%s)' %(num)), os.path.join(output_dir, project.replace('.vcf', '.'+maf)))))
                    time.sleep(5*num)
                    break
                except:
                    fail.append(project)
                    warnings.warn('selenium webdriver error occor: [%s]' %(project))
        driver.close()
        return fail
    
    def get_maf(project, output_dir, maf, num):
        if num == 0:
            os.system('mv %s %s' %(os.path.join(output_dir, 'oncotator.maf.txt'), os.path.join(output_dir, project.replace('.vcf', '.'+maf))))
        else:
            os.system('mv %s %s' %(os.path.join(output_dir, 'oncotator.maf{}.txt'.format('(%s)' %(num)), os.path.join(output_dir, project.replace('.vcf', '.'+maf)))))

def work_log(work_data):
    startTime = time.time()
    p1 = autoOncotator(work_data[0], work_data[1], args.input_dir, args.output_dir, args.tsv, args.maf, work_data[2])
    
    p1.remove_snp(p1.project, p1.input_dir, p1.output_dir)
    p1.vcf2oncotator(p1.project, p1.output_dir, p1.tsv)
    fail = p1.oncotator(p1.filesize, p1.project, p1.output_dir, p1.tsv, p1.maf, p1.num)
    time.sleep(100)
    p1.get_maf(p1.project, p1.output_dir, p1.maf, p1.num)
    
    endTime = time.time()
    logger_stderr.info('Done for vcf [%s] : %.2f min.' %(work_data[1], (endTime-startTime)/60))
    if len(fail) != 0:
        logger_stderr.info('Fail for annotation: [%s]' %(args.input_dir))

def pool_handler():
    p = Pool(args.pool_size)
    p.map(work_log, work)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=dedent("""\
Testing environment: Python 3.6

Inputs:
1. vcf file: Specify the file name with the -v or --vcf argument.

Outputs:
1. filter.vcf file: Remove SNP from the specified vcf file.
2. tsv file: Generate the input format file for Oncotator.
3. maf file: Annotated variants by Oncotator(http://portals.broadinstitute.org/oncotator/) using selenium webdriver.

Usage:
1. List all vcfs in specified directory (e.g. current working directory)
python3 autoOncotator.py -l .
2. for running one vcf file
python3 autoOncotator.py -v test123.mutect2.vcf
3. for Parallelly running mutiple vcf files (e.g. pool size = 15)
* Notes: 'NO SPACE' between vcf files
python3 autoOncotator.py -p 15 -v test721.mutect2.filter.vcf,test123.mutect2.filter.vcf,test476.mutect2.filter.vcf
"""))
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-v', '--vcf', type=str, help='Variant call file, vcf format.')
    optional.add_argument('-i', '--input_dir', type=str, default=os.getcwd(), help='input directory (default: current working directory)')
    optional.add_argument('-o', '--output_dir', type=str, default=os.getcwd(), help='output directory (default: current working directory)')
    optional.add_argument('-t', '--tsv', type=str, default='tsv', help='Generate the input format file for Oncotator, you can defined the name of the file (default: tsv)')
    optional.add_argument('-m', '--maf', type=str, default='oncotator.maf.txt', help='output file name (default: oncotator.maf.txt)')
    optional.add_argument('-l', '--list_id', type=str, help='list all vcf files in specified directory')
    optional.add_argument('-p', '--pool_size', type=int, default=1, help='Pool size of multi-thread for parallel computing (default: 1)')
    optional.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
    parser._action_groups.append(optional)
    args = parser.parse_args()
    
    if args.vcf is None and args.list_id is None:
        parser.print_help()
        
    if args.vcf:
        vcfs = str(args.vcf).split(',')
        logger_stderr.info('Loading %s...' %(vcfs))
        
        if args.input_dir:
            logger_stderr.info('Input directory: [%s]' %(args.input_dir))
            
        if args.output_dir:
            logger_stderr.info('Output directory: [%s]' %(args.output_dir))
            
        if args.tsv:
            logger_stderr.info('Name of input file for Oncotator: [%s]' %(args.tsv))
            
        if args.maf:
            logger_stderr.info('Output file name: [%s]' %(args.maf))
        
        if args.pool_size:
            logger_stderr.info('Pool size of multi-thread for parallel computing: [%s]' %(args.pool_size))
            
        os.system('ls -lt %s > project_size.txt' %(args.input_dir))
        work = []
        project_size = {}
        with open('project_size.txt', 'r') as f:
            ct = 0
            for i in f.readlines():
                if i.split()[-1] in vcfs:
                    work.append([i.split()[4], i.split()[-1]], ct)
                    ct+=1
        
        os.system('rm project_size.txt')
        logger_stderr.info('Add to queuing: %s' %(work))
        pool_handler()
    
    if args.list_id is not None:
        test = [i for i in os.listdir(args.list_id) if '.vcf' in i and '.filter.vcf' not in i]
        txt = str()
        for i in test:
            txt += i+','
        logger_stderr.info('list all vcfs in [%s]' %(os.getcwd()))
        logger_stderr.info('Num. of list: [%s]' %(len(test)))
        logger_stderr.info('list: [%s]' %(txt[:-1]))
    

