import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import csv

ch=input("Want to save to drive ? (y/n) : ")
if ch.lower()=="n":
    saveToDrive=False
else:
    saveToDrive=True

# PYDRIVE INIT
def auth():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("creds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("creds.txt")
    return GoogleDrive(gauth)
def addTodrive(fname):
    file_drive = drive.CreateFile({'title':os.path.basename(fname) })  
    file_drive.SetContentFile(fname) 
    file_drive.Upload()
    permission = file_drive.InsertPermission({
                            'type': 'anyone',
                            'value': 'anyone',
                            'role': 'reader'})
    permaLink=file_drive['alternateLink']
    print(fname+"  saved at "+permaLink)
    return permaLink 

if saveToDrive!=False:
    drive = auth()

# Getting records from text file
with open('urls.txt','r') as f:
    x=f.read()
URLS=x.split("\n")
# SELENIUM FOR SS,REQUESTS FOR PDF
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)

with open(r'Records.csv','a',encoding='utf-8',newline='') as f:
    writer = csv.writer(f)
    if saveToDrive!=False:
        writer.writerow(['WEB URL','TIME','PERMALINK'])
    else:
        writer.writerow(['WEB URL','TIME'])
    for URL in URLS:
        now = datetime.now()                                     
        r=requests.get(URL)
        content_type = r.headers.get('content-type')
        if 'application/pdf' in content_type:
            fname=now.strftime("%d-%m-%Y_%H-%M-%S")+'.pdf'
            with open(fname, 'wb') as f:
                f.write(r.content)
        else:    
            driver.get(URL)
            time.sleep(2) #to load content in js based sites
            S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
            driver.set_window_size(S('Width'),S('Height'))
            fname=now.strftime("%d-%m-%Y_%H-%M-%S")+'.png'  
            driver.find_element_by_tag_name('body').screenshot(fname)
        if saveToDrive!=False:
            permaLink=addTodrive(fname)
            writer.writerow([URL,now.strftime("%d-%m-%Y %H:%M:%S"),permaLink])
        else:
            writer.writerow([URL,now.strftime("%d-%m-%Y %H:%M:%S")])
            print(fname + " saved")
    driver.quit()
#chaha0s
