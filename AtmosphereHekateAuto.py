import requests
import os
from zipfile import ZipFile
import datetime

atmUrl = 'https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases' #The link for the release page
hekUrl = 'https://api.github.com/repos/CTCaer/hekate/releases'

now = datetime.datetime.now()
monthDay = now.strftime("%m.%d")

if not os.path.exists(monthDay):
    os.makedirs(monthDay) #Create folder for the downloads

# Send 2 requests to Github to get information about release pages
atmResponse = requests.get(atmUrl)
atmResponse.raise_for_status()

hekResponse = requests.get(hekUrl)
hekResponse.raise_for_status()

atmLatest = atmResponse.json()[0]['html_url'] #Get the URL for the latest release

#Convert that url into the api link version
atmApi = atmLatest[:8] + 'api.' + atmLatest[8:]
atmApi2 = atmApi[:23] + 'repos/' + atmApi [23:]
atmApi3 = atmApi2[:66] + 's' + atmApi2 [66:]

hekLatest= hekResponse.json()[0]['html_url']

hekApi = hekLatest[:8] + 'api.' + hekLatest[8:]
hekApi2 = hekApi[:23] + 'repos/' + hekApi [23:]
hekApi3 = hekApi2[:55] + 's' + hekApi2 [55:]

#Send request to  GitHub API to get information about latest release
atmResponse = requests.get(atmApi3) 
atmResponse.raise_for_status()

hekResponse = requests.get(hekApi3) 
hekResponse.raise_for_status()

# Get the URLs for the indiviual assests
#Array containing assets from the release page
atmAssets = atmResponse.json()['assets'] 
hekAssets = hekResponse.json()['assets'] 

# Download the assets
for i in range(len(atmAssets)):
    
    response = requests.get(atmAssets[i]['browser_download_url']) # Get the download URLs for each asset
    response.raise_for_status()
    
    #Download the assets
    f = open(atmAssets[i]['name'], 'wb')   
    f.write(response.content)

hekResponse = requests.get(hekAssets[0]['browser_download_url']) 
hekResponse.raise_for_status()
    
f = open(hekAssets[0]['name'], 'wb')   
f.write(hekResponse.content)
