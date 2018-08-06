#! /usr/bin/python3
#
# @(!--#) @(#) swss.py, version 002, 27-july-2018
#
# open a series of home pages and take a screen shot of each one
#

################################################################################################

#
# imports
#

import sys
import os
import argparse
import glob
import shutil
import tempfile
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

################################################################################################


def expandips(ip):
    octets = ip.split('.')
    
    if len(octets) != 4:
        return [ip]
    
    lastoctet = octets[3]
    
    if lastoctet.find('-') == -1:
        return [ip]

    startend = lastoctet.split('-')
    
    if len(startend) != 2:
        return [ip]
    
    try:
        start = int(startend[0])
        end = int(startend[1])
    except ValueError:
        return [ip]

    iplist = []
        
    while start <= end:
        iplist.append("{}.{}.{}.{}".format(octets[0], octets[1], octets[2], start))
        start += 1

    return iplist
    
#########################################################################
    
def readipsfromfile(filename):
    global progname
    
    funcname = 'readipsfromfile'
    
    try:
        file = open(filename, "r", encoding="utf-8")
    except IOError:
        print("{}: {}: cannot open IP address/hostname file \"{}\" for reading".format(filename))
        sys.exit(2)

    iplist = []
    
    for line in file:
        line = line.strip()
        
        if line == "":
            continue
        
        iplist.append(line)
    
    return iplist

#########################################################################

def leadzeroip(ip):
    octets = ip.split('.')
    
    if len(octets) != 4:
        return ip

    for octet in octets:
        try:
            dummy = int(octet)
        except ValueError:
            return ip

    return "{:03d}-{:03d}-{:03d}-{:03d}".format(int(octets[0]), int(octets[1]), int(octets[2]), int(octets[3]))

#########################################################################

def csv(s):
    
    r = '"'
    
    for c in s:
        if c == '"':
            r += '""'
        else:
            r += c
            
    r += '"'
    
    return r

#########################################################################

def logmsg(logfile, msg):
    global progname
    
    print("{}: {}".format(progname, msg))

    print("{}: {}".format(datetime.datetime.now(), msg), file=logfile)
    
    logfile.flush()
    
    return
    
#########################################################################

def swss(ipaddresses, port, logfile, csvfile):
    global progname
    
    funcname = 'wss'
    
    logmsg(logfile, "starting FireFox browser")
    
    browser = webdriver.Firefox()
    browser.implicitly_wait(10)
    browser.set_window_position(0, 0)
    browser.maximize_window()

    logmsg(logfile, "FireFox started")

    for ip in ipaddresses:
        if (port == "http") or (port == "80"):
            url = "http://{}/".format(ip)
            portnum = "80"
        elif (port == "https") or (port == "443"):
            url = "https://{}/".format(ip)
            portnum = "443"
        else:
            url = "http://{}:{}/".format(ip, port)
            portnum = port

        logmsg(logfile, "getting  URL \"{}\"".format(url))

        try:
            browser.get(url)
            logmsg(logfile, "waiting for page load to settle")
            time.sleep(2.0)
            status = "ok"
        except WebDriverException as exception:
            errortext = str(exception).strip()
            logmsg(logfile, "error getting URL \"{}\" - \"{}\"".format(url, errortext))
            status = "get failed: {}".format(errortext)

        if status != "ok":
            title = "n/a"
        else:
            title = browser.title

        screenshotfilename = 'swss-{}-{}.png'.format(leadzeroip(ip), portnum)
        logmsg(logfile, "taking screenshot to file \"{}\"".format(screenshotfilename))
        browser.save_screenshot(screenshotfilename)
        
        print('{},{},{},{}'.format(csv(leadzeroip(ip)), csv(url), csv(status), csv(title)), file=csvfile)
        csvfile.flush()

    logmsg(logfile, "quiting FireFox browser")
    browser.quit()
    
    logmsg(logfile, "FireFox stopped")
    
    return            

################################################################################################

def main():
    funcname = 'main'    

    parser = argparse.ArgumentParser()

    parser.add_argument("--iplist",  help="list of IP addresses to visit",           required=True)
    parser.add_argument("--logfile", help="log file name",                           default="swss.log")
    parser.add_argument("--csvfile", help="CSV file name",                 default="swss.csv")
    parser.add_argument("--port",    help="port (http/https/port#)",                 default="https")

    args = parser.parse_args()
    
    try:
        logfile = open(args.logfile, 'w', encoding='utf-8')
    except IOError:
        print("{}: {}: unable to open log file name \"{}\" for writing".format(progname, funcname, args.logfile))
        sys.exit(2)

    try:
        csvfile = open(args.csvfile, 'w', encoding='utf-8')
    except IOError:
        print("{}: {}: unable to open CSV file name \"{}\" for writing".format(progname, funcname, args.csvfile))
        sys.exit(2)

    ipaddresses = []

    for ip in args.iplist.split(','):
        if ip.find('-') != -1:
            ipaddresses.extend(expandips(ip))
        elif ip.find('+') == 0:
            ipaddresses.extend(readipsfromfile(ip[1:]))
        else:
            ipaddresses.append(ip)

    swss(ipaddresses, args.port, logfile, csvfile)

    logfile.close()

    csvfile.close()

    return 0

##########################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
