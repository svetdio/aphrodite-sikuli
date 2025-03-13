from sikuli import *
from java.awt import Robot, event
from java.awt.event import InputEvent
import curlAPI

regions = [
        Region(7,32,645,475), Region(650,6,612,515), Region(1276,0,644,524), 
        Region(0,517,641,513), Region(644,525,638,515), Region(1280,519,635,515)
       ]

#Update the accounts based on whether they are for transfer or seamless
accounts = ["testcny1","testcny2","testcny3","testcny4","testcny5",""]

GAME_LOGO = Pattern("GAME_LOGO.png").similar(0.71)
LIVE_PAGE = Pattern("LIVE_GAME.png").similar(0.71)
LIVE_FIND = Pattern("LIVE_FIND.png").similar(0.66)
LIVE_LAUNCH = Pattern("LIVE_LAUNCH.png").similar(0.68)
LIVE_PFP = Pattern("Live_PFP.png").similar(0.67)
DRAGON = "DRAGON.png"
CONFIRM_BET = Pattern("CONFIRM_BET.png").similar(0.78)
IDLE = Pattern("IDLE.png").similar(0.68)
REBET =Pattern("REBET.png").similar(0.69)
STOP_BET = Pattern("STOP_BET.png").similar(0.69)
CARDS = Pattern("CARDS.png").similar(0.71)

robot = Robot()
launch_lobby = False
open_live = False
first = False

def launch():
    try:
        for region, expected_username in zip(regions, accounts):
            print("Checking region for %s" % expected_username)
            if not region.exists(GAME_LOGO):
                print("Game not yet launched in region for %s" % expected_username)
                region.click()
                print("Attempting to login for user: %s" % expected_username)
                for account in curlAPI.accounts:
                    if account["username"] == expected_username:
                        game_url = curlAPI.get_token_and_launch_game(account["username"], account["password"])
                        if game_url:
                            region.click()
                            type("w", KeyModifier.CTRL)
                            wait(1)
                            type("t", KeyModifier.CTRL)
                            App.setClipboard(game_url)
                            type("v", KeyModifier.CTRL)
                            type(Key.ENTER)
                        else:
                            print("Failed to get game URL for %s" % expected_username)
                        break
    except:
        pass

def live_nav(): 
    try:
        for region, expected_username in zip(regions, accounts):
            print("Checking region for navigation in %s" % expected_username)
    
            if exists(LIVE_PAGE, 2):
                region.click(LIVE_PAGE)
                
            wheel(region, WHEEL_DOWN, 1)  # Scroll down inside the region
           
            if exists(LIVE_FIND, 1):  # Wait up to 3 seconds for LIVE_FIND
                region.hover(LIVE_FIND)
                region.click(LIVE_LAUNCH)
    except:
        pass


def live_game(region):
    try:      
        for region, expected_username in zip(regions, accounts):

            if exists(STOP_BET, 0.2):
                continue
            
            if exists(REBET, 0.2):
                region.click(REBET)
            else:
                region.click(DRAGON)
                
            region.click(CONFIRM_BET)

    except:
        pass
                
            
def callCurl(username, target, region):
    try:
        print("Attempting to login for user: %s" % username)
        for account in curlAPI.accounts:
            if account["username"] == username:
                game_url = curlAPI.get_token_and_launch_game(account["username"], account["password"])
                if game_url:
                    region.click(target)
                    type("w", KeyModifier.CTRL)
                    type("t", KeyModifier.CTRL)
                    App.setClipboard(game_url)
                    type("v", KeyModifier.CTRL)
                    type(Key.ENTER)
                else:
                    print("Failed to get game URL for %s" % username)
                break
    except:
        pass

def open_game_url(url):
    type("w", KeyModifier.CTRL)
    type("t", KeyModifier.CTRL)
    type(url)
    type(Key.ENTER)

while True:
    if not launch_lobby:
        launch()
        launch_lobby = True
        
    if not open_live:
        live_nav()
        open_live = True

    for region in regions:
        live_game(region)