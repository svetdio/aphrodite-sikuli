from sikuli import *
from java.awt import Robot, event
from java.awt.event import InputEvent
import curlAPI

regions = [
        Region(7,32,645,475), Region(650,6,612,515), Region(1276,0,644,524), 
        Region(0,517,641,513), Region(644,525,638,515), Region(1279,521,641,512)
       ]

#Update the accounts based on whether they are for transfer or seamless
accounts = ["testcny1","testcny2","testcny3","testcny4","testcny5", ""]

GAME_LOGO = Pattern("GAME_LOGO.png").similar(0.71)
SLOT_PAGE = Pattern("SLOT_GAME.png").similar(0.73)
SLOT_FIND = Pattern("SLOT_FIND.png").similar(0.72)
SLOT_LAUNCH = Pattern("SLOT_LAUNCH.png").similar(0.73)

SLOT_LOGO = "AUTOPLAY.png"
AUTOPLAY = Pattern("AUTOPLAY.png").similar(0.72)
X_SPEED = Pattern("X_SPEED.png").similar(0.81)
SPINNING = Pattern("SPINNING.png").similar(0.72)
AUTO_SPIN = Pattern("AUTO_SPIN.png").similar(0.72)

robot = Robot()
launch_lobby = False
open_slot = False
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

def slot_nav(): 
    try:
        for region, expected_username in zip(regions, accounts):
            print("Checking region for navigation in %s" % expected_username)
    
            if exists(SLOT_PAGE, 2):
                region.click(SLOT_PAGE)
            wait(2)
                
            wheel(region, WHEEL_DOWN, 4)  # Scroll down inside the region
           
            if exists(SLOT_FIND, 1):  # Wait up to 3 seconds for LIVE_FIND
                region.hover(SLOT_FIND)
                region.click(SLOT_LAUNCH)
    except:
        pass

def auto_spin_regions(region):
    try:
        for region, expected_username in zip(regions, accounts):
            print("Checking region for %s" % expected_username)

            if region.exists(SPINNING, 1):
                continue

            if region.exists(AUTOPLAY, 0.5):
                print("Starting autoplay in region for %s." % expected_username)
                region.click(AUTOPLAY)
                wait(0.2)

                if region.exists(X_SPEED, 0.5):
                    region.click(X_SPEED)
                    print("X-Speed activated in region for %s." % expected_username)
                
    except Exception as e:
        print("Error in auto_spin_region: {}".format(e))
         
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
        
    if not open_slot:
        slot_nav()
        open_slot = True

    for region in regions:
        auto_spin_regions(region)