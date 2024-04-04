from tools import *
import argparse

connect_and_launch()
waitUntilGameActive()

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--teamup", action = 'store_true', help = "Run the Team-up function")
parser.add_argument("-d", "--dailies", action = 'store_true', help = "Run the Dailies function")
parser.add_argument("-c", "--config", metavar="CONFIG", default = "settings.ini", help = "Define alternative settings file to load")
args = vars(parser.parse_args())

if args['config']:
    settings = os.path.join(cwd, args['config'])
else:
    settings = os.path.join(cwd, 'settings.ini')
config.read(settings)

def dailies():
    claim_afk_rewards()
    friend_points_collect()
    mail_connect()
    emporium_purchases()
    arena()
    quests()
    print('Dailies done!')

def teamup():
    while 1 == 1:
        team_up()

def team_up():
    timer = 0
    while 1 == 1:
        while not isVisible('labels/sunandstars', region=(770, 40, 100, 100)):
            click_location('neutral')
            wait()
        print('Opening chat')
        while not isVisible('teamup/join'):
            click('teamup/chat', seconds=0, suppress=True)
            click('teamup/teamup', seconds=1, suppress=True)
            if isVisible('teamup/join'):
                # Prioritise Corrupt Creatures over Synergy battles
                continue
            if isVisible('teamup/synergy'): # So we don't open the same one twice in a row
                x, y = returnxy('teamup/synergy')
                if return_pixel_colour(x, y + 220, 2, seconds=0) < 200:
                    print('Synergy Battle found!')
                    clickXY(x, y + 220)
                    if isVisible('buttons/back'):
                        clickXY(300, 900)
                        clickXY(650, 1800)
                        click('buttons/back', suppress=True)
                        print('Hero lent\n')
                        wait(10)
                        return
                    else:
                        print('Something went wrong, returnin\n')
                        wait(10)
                        return
        print('Corrupt Creature found!')
        click('teamup/join', seconds=5)
        if not isVisible('teamup/ready'):
            print('Something went wrong, waiting and restarting\n')
            wait(10)
            return
        click('teamup/ready', seconds=6)
        # print('Readying up in the lobby')
        while isVisible('teamup/quit', confidence=0.8):
            timer += 1
            if timer > 15:
                print('Timeout error!\n')
                click('teamup/quit', seconds=2)
                clickXY(850, 1250, seconds=4)
                return
        while isVisible('teamup/ready_lobby'):
            print('Deploying heroes')
            clickXY(120, 1300)
            clickXY(270, 1300)
            clickXY(450, 1300)
            click('teamup/ready_lobby')
        while not isVisible('labels/tap_to_close', confidence=0.8):
            timer += 1
            if timer > 20:
                print('Timeout error!\n')
                click_location('neutral')
                return
        click('labels/tap_to_close', confidence=0.8)
        timer = 0
        print('Battle complete!\n')
        wait(3)
    team_up()



def claim_afk_rewards():
    print('Claiming AFK Rewards')
    clickXY(100, 1800, seconds=4)  # Open AFK Rewards
    clickXY(550, 1400)  # Click Chest
    clickXY(550, 1080)  # Click Collect
    # Double FR
    clickXY(100, 1800)  # Close
    if isVisible('labels/sunandstars', region=(770, 40, 100, 100)):
        return
    else:
        print('Something went wrong')

def friend_points_collect():
    print('Claiming friend gifts')
    click('buttons/main_menu', region=(900, 1750, 150, 150))
    click('buttons/friends', region=(30, 1450, 200, 200), seconds=2)
    clickXY(700, 1800, seconds=2)
    clickXY(850, 300, seconds=2)
    clickXY(420, 50)  # Neutral location for closing reward pop ups etc, should never be an in game button here
    click('buttons/back', region=(50, 1750, 150, 150))
    click('buttons/back', region=(50, 1750, 150, 150))
    if isVisible('labels/sunandstars', region=(770, 40, 100, 100)):
        return
    else:
        print('Something went wrong')

def mail_connect():
    print('Claiming Mail')
    click('buttons/main_menu', region=(900, 1750, 150, 150))
    click('buttons/mail', region=(240, 1250, 200, 200), seconds=2)
    clickXY(750, 1800, seconds=2)
    clickXY(750, 1800, seconds=2)
    click('buttons/back', region=(50, 1750, 150, 150))
    click('buttons/back', region=(50, 1750, 150, 150))
    if isVisible('labels/sunandstars', region=(770, 40, 100, 100)):
        return
    else:
        print('Something went wrong')

def emporium_purchases():
    print('Purchasing daily shop bits')
    click('buttons/main_menu', region=(900, 1750, 150, 150))
    click('buttons/emporium', region=(850, 1250, 200, 200), seconds=2)
    clickXY(100, 700, seconds=2) # guild store
    clickXY(325, 900, seconds=2) # daily card
    clickXY(650, 1800, seconds=2)  # purchase
    clickXY(875, 1250, seconds=2)  # diamonds confirm
    click_location('neutral')
    click('buttons/back2', region=(50, 1750, 150, 150))
    click('buttons/back', region=(50, 1750, 150, 150))
    if isVisible('labels/sunandstars', region=(770, 40, 100, 100)):
        return
    else:
        print('Something went wrong')

def arena(battles=9):
    counter = 0
    print('Battling Arena')
    clickXY(450, 1825)
    if isVisible('labels/battle_modes'):
        click('buttons/arena', seconds=2)
        click_location('neutral')
        click_location('neutral')
        while counter < battles:
            print('Fighting Arena Battle ' + str(counter+1) + ' of ' + str(battles))
            click('buttons/challenge', seconds=3)
            if isVisible('buttons/confirm'):
                print('Purchase challenge pop-up detected, confirming')
                click('buttons/confirm')
                click('buttons/challenge', seconds=3)
            clickXY(180, 1450, seconds=5)
            click('buttons/battle')
            while not isVisible('labels/tap_to_close'):
                wait()
                # Clear promotion screen if visible
                if isVisible('labels/arena_promote'):
                    click_location('neutral')
            print('Battle complete')
            while isVisible('labels/tap_to_close'):
                click('labels/tap_to_close', seconds=3)
            counter += 1
        click('buttons/back', region=(50, 1750, 150, 150), seconds=2)
        click('buttons/back2', region=(50, 1750, 150, 150))
    if isVisible('labels/sunandstars', region=(770, 40, 100, 100)):
        return
    else:
        print('Something went wrong')
        save_screenshot('something_went_wrong')


def quests():
    print('Collecting quests')
    click('buttons/main_menu', region=(900, 1750, 150, 150))
    click('buttons/quests', seconds=3)

    # Daily quests
    clickXY(300, 1800, seconds=2)
    if isVisible('buttons/quick_collect'):
        click('buttons/quick_collect', seconds=2)
        clickXY(900, 200, seconds=2)  # collect dailies
        click_location('neutral')

    # Guild quests
    clickXY(500, 1800, seconds=2)
    while isVisible('buttons/collect'):
        click('buttons/collect')

    # Growth Trials
    clickXY(950, 1800, seconds=2)
    while isVisible('buttons/collect'):
        click('buttons/collect')

    click('buttons/back2', confidence=0.8, region=(40, 1750, 150, 150))
    click('buttons/back', region=(50, 1750, 150, 150))

    if isVisible('labels/sunandstars', region=(770, 40, 100, 100)):
        return
    else:
        print('Something went wrong')
        save_screenshot('something_went_wrong')


if args['dailies']:
    print('Starting up dailies')
    dailies()

if args['teamup']:
    print('Starting up team-up farming\n')
    teamup()