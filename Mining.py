# Mining script by Taharnak
# Mining
from System.Collections.Generic import List
import datetime
import sys
import winsound

###########################################################
# Global variables
###########################################################

# Pack Llama id
packLlamaSerial = 0x000064CC
# Ore ID
oreTypeId = 0x19B9
# Pickaxe Type Id
_pickaxeType = 3718
# Servers drag delay
dragTime = 650
# Message Colors
colors = {
    'green': 65,
    'cyan': 90,
    'orange': 45,
    'red': 1100,
    'yellow': 52
}
# Stop Weight
stopWeight = 380
# Completed Language
miningCompletePhrases = ["You can't mine there.", "You can't dig while", "Target cannot be seen.", 
                        "You dig some", "You loosen", "There is no metal here to mine.", "You can't mine that."]
# Bad mining spots
badMiningLocation = ["You can't dig while", "Target cannot be seen.", "You can't mine that."]
# Spot Cleared
spotCleared = "There is no metal here to mine."
# Cave Tiles
caveTiles = [0x1339, 0x1340, 0x1341, 0x1342, 0x1343, 0x1344, 0x3898]
badTiles = [0x1353, 0x8600]

###########################################################
# Mining Functions
###########################################################

def startMining():
    global targetX
    global targetY
    for y in range(-2, 3):
        for x in range (-2, 3):
            targetX = Player.Position.X + x
            targetY = Player.Position.Y + y
            mineLocation(targetX, targetY)
    Player.HeadMessage(colors['red'], "Finished mining." )

def mineLocation(targetX, targetY):
    while (True):
        Journal.Clear()
        Misc.Pause(150)
        Items.UseItem(pickaxeId)
        Target.WaitForTarget(500)
        
        # Get Tile Info
        tileID = None
        staticsTileInfo = Statics.GetStaticsTileInfo( targetX, targetY, Player.Map )
        # If there isn't a tile there, break.
        if staticsTileInfo.Count == 0:
            Player.HeadMessage(colors['red'], "No tile info.")
            Misc.Pause(100)
            Target.Cancel()
            break
        else:
            for tile in staticsTileInfo:
                tileID = tile.StaticID
                #Player.HeadMessage(colors['orange'], str(targetX) + ", " + str(targetY) + " Tile info: " + str(tile.StaticID))
                Target.WaitForTarget(500)
                Target.TargetExecute(targetX, targetY, Player.Position.Z, tile.StaticID)
        
        # If it's not a mineable tile, break.
        if (tileID in badTiles):
            Player.HeadMessage(colors['orange'], "Bad tile. Skipping.")
            Misc.Pause(100)
            break
        
        #Calculate wait timer
        waitTime = datetime.datetime.now() + datetime.timedelta(seconds=5)

        # Wait for mining to complete
        while (not any(Journal.Search(phrase) for phrase in miningCompletePhrases)
            and not any(Journal.Search(phrase) for phrase in badMiningLocation)
            and datetime.datetime.now() < waitTime):
            Misc.Pause(1000)
            #Player.HeadMessage(colors['orange'], "Waiting...")
        
        # See if the spot is empty
        if (Journal.Search(spotCleared) or any(Journal.Search(phrase) for phrase in badMiningLocation)):
            #Player.HeadMessage(colors['orange'], "Spot is cleared. Break.")
            break

        # Mining is done or timed out, looping.
        # Player.HeadMessage(colors['orange'], "Completed mining or timed out.")
        
        # If tool is broken, get a new one.
        if (Journal.Search("You have worn out your tool!")):
            Player.HeadMessage(colors['orange'], "Pickaxe broke. Finding a new one.")
            findPickaxe()
        
        # Check to see if overweight
        checkWeight()
    
    # Spot is marked clear.
    Player.HeadMessage(colors['orange'], str(targetX) + ", " + str(targetY) + " cleared.") #Moving to next spot.")


#def waitLoop(targetX, targetY):
#    waitTime = datetime.datetime.now() + datetime.timedelta(minutes=1)
#    while (not any(Journal.Search(phrase) for phrase in miningCompletePhrases) and datetime.datetime.now() < waitTime):
#        Misc.Pause(1000)
#        Player.HeadMessage(colors['orange'], "Waiting...")
#    if (any(Journal.Search(spotCleared))):
#        Player.HeadMessage(colors['orange'], "This spot is cleared...")
#    Player.HeadMessage(colors['orange'], "Completed mining or timed out.")

###########################################################
# Global Functions
###########################################################

def findPickaxe():
    global pickaxeId
    Player.HeadMessage(colors['orange'], "Looking for pickaxe.")
    player_bag = Items.FindBySerial(Player.Backpack.Serial)
    if not Player.CheckLayer('RightHand'):
        Player.HeadMessage(colors['orange'], "Right hand empty. Checking bag.")
        foundPickaxe = False
        for i in player_bag.Contains:
            if i.ItemID == _pickaxeType:
                Player.HeadMessage(colors['orange'], "Found pickaxe in bag.")
                Player.EquipItem(i.Serial)
                Misc.Pause(dragTime)
                foundPickaxe = True
                break
        if not foundPickaxe:
            Player.HeadMessage(colors['red'], "No Pickaxes Found, Stopping Script.")
            #Player.ChatSay(33, "No Pickaxes Found, Stopping Script.")
            sys.exit()
    elif Player.GetItemOnLayer('RightHand').ItemID == _pickaxeType:
        Player.HeadMessage(colors['orange'], "Already equipped.")
    else:
        Player.HeadMessage(colors['red'], "No Pickaxes Found, Stopping Script.")
        #Player.ChatSay(33, "No Pickaxes Found, Stopping Script.")
        sys.exit()
    pickaxeId = Player.GetItemOnLayer('RightHand').Serial

def checkWeight():
    if Player.Weight >= stopWeight:
        Player.HeadMessage(colors['orange'], "Moving ores.")
        dropOres()
        #Player.HeadMessage(colors['orange'], "Go bank this shit.")
        #playAlertSounds()
        #sys.exit()

def dropOres():
    oreFound = None
    oreFound = Items.FindByID(oreTypeId, -1, Player.Backpack.Serial)
    if (not oreFound is None):
        Items.Move(oreFound.Serial,packLlamaSerial,0)
        Misc.Pause(dragTime)
        Player.HeadMessage(45, "Ore moved.")
        dropOres()

def worldSave():
    if Journal.SearchByType("The world is saving, please wait.", "Regular" ):
        Misc.SendMessage("Pausing for world save", 33)
        while not Journal.SearchByType("World save complete.", "Regular"):
            Misc.Pause(1000)
        Misc.SendMessage("Continuing", 33)
        Journal.Clear()

def playAlertSounds():
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

###########################################################
# Actual code
###########################################################

# Check if player is mounted.
if (Player.Mount):
    Player.HeadMessage(colors['red'], "You can't mine mounted, dipshit.")
    playAlertSounds()
    sys.exit()

# Find pickaxe
findPickaxe()

# Start mining
startMining()
