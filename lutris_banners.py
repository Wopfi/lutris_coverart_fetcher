#!/usr/bin/python3

# 1. Get Steam ID and Lutris ID
# 2. Check if banner is already in ~/.local/share/lutris/coverart/
# 3. If not, fetch Banner from https://steamcdn-a.akamaihd.net/steam/apps/{APPID}/library_600x900_2x.jpg
# 4. Profit

import sqlite3
import yaml
import os
import urllib.request
import shutil
from pathlib import Path

home = str( Path.home() )
coverartPath = home + '/.local/share/lutris/coverart/'
configPath = home + '/.config/lutris/games/';
bannerPage = 'https://steamcdn-a.akamaihd.net/steam/apps/'
bannerFilename = 'library_600x900_2x.jpg'

print( "Home directory: {}".format(home) )

conn = sqlite3.connect( home + '/.local/share/lutris/pga.db' )
c = conn.cursor()

c.execute('SELECT name,slug,configpath FROM games')

for row in c:
    fullName = row[0]
    slug = row[1]
    configFile = row[2]
    bannerName = coverartPath + slug + ".jpg"

    if ( os.path.exists(bannerName) ):
        print ( "Banner for {} already exists -> skipping".format(fullName) )
    else:
        if ( configFile ):
            fullConfigFilename = configPath + configFile + ".yml";

            if ( os.path.exists(fullConfigFilename) ):
                with open(fullConfigFilename) as file:
                    list = yaml.load(file, Loader=yaml.FullLoader)

                    for item, doc in list.items():
                        if ( item == "game" ):
                            if ( "appid" in doc ):
                                appId = doc["appid"]
                                print( "Checking \"{}\" with ID {}".format(fullName, appId) )
                                fullBannerName = bannerPage + appId + "/" + bannerFilename
                                print( "  Trying to fetch Banner for ID {}, name {}".format(appId, fullBannerName), end='' )

                                try:
                                    with urllib.request.urlopen(fullBannerName) as response, open(bannerName, 'wb') as outputFile:
                                        shutil.copyfileobj(response, outputFile)
                                        print( " -> Success!" )
                                except urllib.error.URLError as e:
                                    print( " -> Error: {}".format(e.reason) )
#                            else:
#                                print( "  No Steam ID found -> skipping" )
#            else:
#                print( "  No config file {} found -> skipping".format(configFile+".yml") )
#        else:
#            print( "  No config file -> skipping" )


#gamesDir = "/home/thomas/.config/lutris/games/"

#for subdir, dirs, files in os.walk(gamesDir):
#    for file in files:
#        name,ext = os.path.splitext( file )
#
#        if (ext.lower() == ".yml"):
#            print( name + " " + ext )
