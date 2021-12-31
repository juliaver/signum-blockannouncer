import requests
import json
import numpy as np
import time

mUrl = "discord webhook url"

poolurl = "signum pool url"

def storeId(blockId):
    np.save('mostRecentBlock', blockId)


def getId():
    try:
        blockId = np.load('mostRecentBlock.npy')
    except IOError as err:
        print(err)
        storeId(1)
        blockId = np.load('mostRecentBlock.npy')
        if blockId != 1:
            raise Exception("Could not read nor create 'mostRecentBlock.dat' file.")
        else:
            return blockId
    else:
        newId = blockId.min()
        return newId


wonBlocksResponse = requests.get(poolurl + "/api/getWonBlocks")
wonBlocks = json.loads(wonBlocksResponse.text)

mostRecentBlock = getId()
runningHighest = 0

for entry in wonBlocks.get("wonBlocks")[::-1]:
    if entry.get("height") > mostRecentBlock and str(entry.get("reward")) != "Processing...":
        time.sleep(1)
        print(entry.get("name"))
        print(entry.get("generator"))
        account = str(entry.get("generator"))
        if str(entry.get("name")) != "None":
            name = str(entry.get("name"))
        else:
            name = str(entry.get("generator"))
        data = {
            "content": "<:block:867846020250599444> Block won! " "Height: " + str(entry.get("height")) + " won by: [" + name + "](https://explorer.signum.network/address/" + account + "). The total reward for this block was: " + str(entry.get("reward")) + ". **Plus 5% bonus:** " + str(entry.get("poolShare"))
        } 
        response = requests.post(mUrl, json=data)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(response.status_code))

        print("blockId: " + str(entry.get("height")) + " won by: " + name + ". The total reward for this block was: " + str(entry.get("reward")))
        if entry.get("height") > runningHighest:
            runningHighest = entry.get("height")
            storeId(runningHighest)
