# based off https://gist.github.com/micolous/123ac1b7c3e9fb389e259ccd63df7992
# converted to python3 with minor changes
from argparse import ArgumentParser, FileType
from struct import unpack
from datetime import datetime, date, timedelta

class t:
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    OFF = '\033[91m'
    ON = '\033[92m'
    BLUE = '\033[94m'

EPOCH = datetime(2000, 1, 1, 0, 0)

def parseDump(inputData):
    if len(inputData) != 1024: # check if the dump exceeds the mifare 1k size
        print("Card dump must be exactly 1024 bytes")
        exit()

    trips = [] # Read trips (sector 10-13, blocks 0-2)
    print(t.BOLD + "Time | Cost | Route | Tag status" + t.ENDC)
    for off in (0x280, 0x290, 0x2a0, 0x2c0, 0x2d0, 0x2e0, 0x300, 0x310, 0x320, 0x340): # sectors with trip records
        ts, tap_on, route, cost = unpack("<3xLB4s1xH1x", inputData[off:off+16])
        ts = EPOCH + timedelta(seconds=ts) # get tag on/off time
        tag_on = (tap_on & 0x10 == 0x10) # calculate tag on
        route = route.rstrip(b"\0").decode("utf-8") # get route number
        cost /= 100. # get trip cost
        trips.append((ts.ctime(), cost, route, (t.ON+"Tag on"+t.ENDC) if tag_on else (t.OFF+"Tag off"+t.ENDC))) # compile all that into an entry
    trips.sort(key=lambda x: x[0]) # sort the records by order of time
    for trip in trips:
        print("%s | $%.2f | %s | %s" % trip)

    for off in ([0xe0]):  # Read balance (sector 2&3, block 2)
        balance = unpack("<7xH7x", inputData[off:off+16])[0]
    balance /= 100.
    print("Card balance: $" + str(balance))

    for off in ([0x50]):  # Read card token (sector 1 at offset 88 at )
        token = unpack("<8x1b7x", inputData[off:off+16])[0]
        print("Card token: 0x0" + str(token))
    
    for off in ([0x50]): # read card issue (sector 1, offset 80 at 0x50)
        issued = unpack("<2H12x", inputData[off:off+16])[0]
        issued = date(int(1997) ,int(1), int(1)) + timedelta(issued) # subtract the days from 1997-1-1
        print("Card issued: " + str(issued))

    for off in ([0x52]): # read card token expiry (sector 1, offset 82 at 0x52)
        expiry = unpack("<2H12x", inputData[off:off+16])[0]
        expiry = date(int(1997) ,int(1), int(1)) + timedelta(expiry) # subtract the days from 1997-1-1
        print("Card token expiry: " + str(expiry))

parser = ArgumentParser()
parser.add_argument("input", type=FileType("rb"), nargs=1)
options = parser.parse_args()
print(t.HEADER + t.BOLD + "SmartRider dump reader" + t.ENDC) 
parseDump(options.input[0].read())
