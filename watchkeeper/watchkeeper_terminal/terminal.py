#! /usr/bin/env python3
import os
import os.path
from os.path import exists
from pathlib import Path 
import csv
import sys, getopt
import argparse
import feedparser
import pandas as pd
from tabulate import tabulate
from datetime import date
today = date.today()
today_date = today.strftime('%d/%m/%Y')
path_to_file = '/bin/csvcut'
do_exists_ = os.path.exists(path_to_file)

def show_feed(max_vaule):
    print('Latest Proof-of-Concept code on github ' + today_date)
    feed = feedparser.parse('https://poc-in-github.motikan2010.net/rss')
    for cve_amount in range(max_vaule):
        entry = feed.entries[cve_amount]
        table = [cve_amount,entry.title,entry.updated,entry.link]
        print(str(table) + '\n')
    print('feed amount : ', len(feed.entries))

def check_install():
    do_exists_ = os.path.exists(path_to_file)
    if do_exists_ == True:
        pass
    else:
        pass
check_install() 

def conf_folder():
    path_to_file ='/tmp/Autonomous_Threat_Sweeper_2022_Intelligence_Summary.csv'
    do_exists_ = os.path.exists(path_to_file)
    if do_exists_ == True:
        pass
    else:
        os.system('wget https://raw.githubusercontent.com/Securonix/AutonomousThreatSweeper/main/Autonomous_Threat_Sweeper_2022_Intelligence_Summary.csv -P /tmp/')
        conf_folder()
conf_folder()

def update_intel():
    os.system('rm -r /tmp/Autonomous_Threat_Sweeper_2022_Intelligence_Summary.csv')
    os.system('wget https://raw.githubusercontent.com/Securonix/AutonomousThreatSweeper/main/Autonomous_Threat_Sweeper_2022_Intelligence_Summary.csv -P /tmp/ | grep "Success"')
    print('Intelligence sources updated')

def display(max_rows):
    pd.options.display.max_rows = max_rows
    data = pd.read_csv('/tmp/Autonomous_Threat_Sweeper_2022_Intelligence_Summary.csv')
    print(data)

def main(argv):
    options = 'hutpa:'
    long_options = ['help', 'update_intel', 'table','poc_github', 'all']
    try:
        arguments, vaules = getopt.getopt(argv, options, long_options)
        for current, currentvaule in arguments:
            if current in ('-h', '--help'):
                print('watchkeeper.py -u    --update   (Update intelligence sources)')
                print('watchkeeper.py -t    --table   (Show table)')
                print('watchkeeper.py -t max_rows    --table row_amount   (Show table and specify max amount of rows)')
                print('watchkeeper.py -p    --poc_github   (Show POC code from github)')
                print('watchkeeper.py -a    --all   (Show all)')
            if current in ('-u', '--update_intel'):
                update_intel()
            if current in ('-t', '--table'):
                max_row = 200
                display(int(currentvaule))
            if current in ('-p', '--poc_github'):
                show_feed(int(currentvaule))
            if current in ('-a', '--all'):
                currentvaule = 20
                display(int(currentvaule))
                currentvaule = 10
                show_feed(int(currentvaule))
    except getopt.error as err:
        print (str(err))
        print ('example: ./watchkeeper.py -h')
if __name__ == "__main__":
    main(sys.argv[1:])
