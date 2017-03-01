from block_io import BlockIo
import os
import datetime
import time
import csv
import os.path
import sys

print "********* Bitcoin wallet checker started *********\n\n"

# check to see if config and results .csv files exist. If they don't create them. Also check for api_keys.csv

api_keys = [] # list to hold API key and secret pin

if os.path.isfile("api_keys.csv") == True:
    print "[*] api_keys.csv identified as being in path"
    with open('api_keys.csv', 'r') as userFile:
            userFileReader = csv.reader(userFile)
            for row in userFileReader:
                api_keys.append(row)      
else:
    print "[*] api_keys.csv not identified as being in path. Creating new file now..."
    try:
        with open('api_keys.csv', 'w') as newFile:
            newFileWriter = csv.writer(newFile)    
            newFileWriter.writerow([''])    
        print "[*] api_keys.csv file creation success. Go and get an API key from block.io. Add the Bitcoin key to A1, and your secret pin to A2 in api_keys.csv"
        exit()
    except:
        if os.path.isfile("api_keys.csv") == True:
            pass
        else:
            print "[*] Error in creating api_keys.csv. Quitting..."
            exit()

config_ids = [] # list to hold wallet_ids to search against 

if os.path.isfile("config.csv") == True:
    print "[*] config.csv identified as being in path"
    print "[*] Grabbing config wallet_ids from config.csv"
    with open('config.csv', 'r') as userFile:
                userFileReader = csv.reader(userFile)
                for row in userFileReader:
                    config_ids.append(row[0])
                config_ids.pop(0)
                print "[*] config_ids collected from config.csv:", len(config_ids) 
                if len(config_ids) == 0:
                    print "[*] Zero bitcoin wallets founds in config.csv. Quitting..."
                    exit()
    pass
else:
    print "[*] config.csv not identified as being in path. Creating new file now..."
    try:
        with open('config.csv', 'w') as newFile:
            newFileWriter = csv.writer(newFile)    
            newFileWriter.writerow(["Wallet ID"])    
        print "[*] config.csv file creation success"
        print "[*] Go to config.csv and add new rows with bitcoin wallet IDs. Then rerun this script"
        exit()
    except:
        if os.path.isfile("config.csv") == True:
            pass
        else:
            print "[*] Error in creating config.csv. Quitting..."
            exit()

tx_ids = []

if os.path.isfile("bitcoin.csv") == True:
    print "[*] bitcoin.csv identified as being in path"
    with open('bitcoin.csv', 'r') as userFile:
            userFileReader = csv.reader(userFile)
            for row in userFileReader:
                tx_ids.append(row[4])
            print "[*] TX_IDs already in bitcoin.csv:", len(tx_ids)-1
else:
    print "[*] bitcoin.csv not identified as being in path. Creating new file now..."
    try:
        with open('bitcoin.csv', 'w') as newFile:
            newFileWriter = csv.writer(newFile)    
            newFileWriter.writerow(["Sender", "Confidence", "TX_epoch", "TX_epoch_dtg", "TX_ID", "Amount", "Recipient"])    
        print "[*] bitcoin.csv file creation success"
    except:
        if os.path.isfile("bitcoin.csv") == True:
            pass
        else:
            print "[*] Error in creating bitcoin.csv. Quitting..."
            exit()

# Set up block_io

version = 2
try:
    key1 = str(api_keys[0])[2:21]
    key2 = str(api_keys[1])[2:12]
except:
    print "[*] Error with reading API keys from api_keys.csv. Check that the API_key is in A1, and the secret pin is in A2. Quitting..."
    exit()

block_io = BlockIo(key1, key2, version)

# set up counters

new_items = 0
old_items = 0

# define function to use block_io API to get transactions from a wallet_id

def check_wallet(wallet_id):
    
    global new_items
    global old_items
    
    print "\n[*] Checking:", wallet_id
    
    result = block_io.get_transactions(type='received', addresses=wallet_id)      
        
    for item in result['data']['txs']:
        
        sender = item['senders'][0]
        confidence = item['confidence']
        tx_epoch = item['time']
        tx_epoch_dtg = datetime.datetime.fromtimestamp(item['time']).strftime('%Y-%m-%d %H:%M:%S.%f')
        tx_id = item['txid']
        
        for item in item['amounts_received']:
           
            amount = item['amount']
            recipient = item['recipient']
        
            if any(tx_id in s for s in tx_ids):
                print "[*] TX_ID",tx_id ,"already in bitcoin.csv"
                old_items += 1

            else:
                print "\n[*] Item not in bitcoin.csv, adding now..."
                print "[*] Sender:", sender
                print "[*] Confidence:", confidence
                print "[*] EPOCH time:", tx_epoch
                print "[*] EPOCH time converted:", tx_epoch_dtg
                print "[*] TXID:", tx_id     
                print "[*] Amount:", amount
                print "\n[*] Recipient:", recipient                
                with open('bitcoin.csv', 'a') as newFile:
                    newFileWriter = csv.writer(newFile)
                    newFileWriter.writerow([sender, confidence, tx_epoch, tx_epoch_dtg, tx_id, amount, recipient])
                new_items += 1
                print "[*] Adding success"
                 
    else:

        pass

for item in config_ids:
    check_wallet(item)
    print "[*] Sleeping for 3 seconds for rate limiting"
    time.sleep(3)

print "\n[*] New items:", new_items
print "[*] Old items:", old_items
print "[*] Wallets checked:", len(config_ids) 

print "\n\n********* Bitcoin wallet checker completed *********"

