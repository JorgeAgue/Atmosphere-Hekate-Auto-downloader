import requests
import os
from zipfile import ZipFile
import shutil
from pathlib import Path
import datetime
import time

def getLatestPage(url): # Send request to Github to get the URL for the latest release
    try: #Handle any potential HTTP errors
        response = requests.get(url) 
        response.raise_for_status()

    except requests.exceptions.HTTPError as err:
        print("HTTP Error " + str(err.response.status_code) + " has occured")
        print("Please try again later")
        time.sleep(3)
        exit()
    return response.json()[0]['url'] ,response.json()[0]['tag_name'] #Return the url for the latest with the version number of that release

def getAssets(apiURL): # Get the URLs for the indiviual assests stored in a list
    response= requests.get(apiURL)
    response.raise_for_status()
    return response.json()['assets']

def downloadAssets(assetsList, items): #items is how many things to download
    for i in range(items):
        response = requests.get(assetsList[i]['browser_download_url']) # Get the download URLs for each asset
        response.raise_for_status()
        
        #Download the assets
        f = open(assetsList[i]['name'], 'wb')   
        f.write(response.content)
        f.close()
        print(assetsList[i]['name'], 'has finished downloading')
        shutil.move(assetsList[i]['name'], monthDay+'/')

def unZipAndClean():
    print('\n')
    #Unzip the contents in downloads folder
    for file in Path(monthDay).glob('*.zip'):
        with ZipFile(file, 'r') as zipper:
            print('Unzipping '+ file.name)
            zipper.extractall(monthDay)
        os.remove(file)  #Delete the unzipped files after unzipping

#The links for the release page
atmUrl = 'https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases' 
hekUrl = 'https://api.github.com/repos/CTCaer/hekate/releases'

atmLatest, atmVer = getLatestPage(atmUrl) 
hekLatest, hekVer = getLatestPage(hekUrl)

print('Current version of Atmosphere: ' + atmVer )
print('Current version of Hekate: '+ hekVer +'\n')

atmAssets = getAssets(atmLatest)
hekAssets = getAssets(hekLatest)

today = datetime.datetime.now()
monthDay = today.strftime("%m.%d")

if not os.path.exists(monthDay):
    os.makedirs(monthDay) #Create folder for the downloads

downloadAssets(atmAssets,2)
downloadAssets(hekAssets,1)

unZipAndClean()

print("\nAll downloads complete and extracted")
time.sleep(3)