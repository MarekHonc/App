import pyshark
import time
import requests
import argparse
import json
import os

class Data(object):
        pass

def capture_packets(capture_time, ssid):
        capture = pyshark.LiveCapture(interface='wlan1') # filtrování nefunguje
        capture.sniff(timeout=capture_time)
        print(len(capture))
        data = Data()
        data.data = Data()
        data.data.addresses = []
        capture.close()
        for i in range(len(capture)):
                try:
                        if str(capture[i].layers[3].ssid) == ssid and (not capture[i].wlan.sa in data.data.addresses):
                                print("found: " + str(capture[i].wlan.sa))
                                data.data.addresses.append(capture[i].wlan.sa)
                        else:
                                pass
                except:
                        pass
        data.timestamp = time.time()
        print(data.data.addresses)
        print(data.timestamp)
        return data


def getGUID():
        guid = "0000000000000000"
        try:
                f = open('/proc/cpuinfo','r')
                for line in f:
                        if line[0:6]=='Serial':
                                guid = line[10:26]
                f.close()
                print(guid)
        except:
                guid = "ERORR"

        return guid


#def the_great_loop(capture_time, ssid, token):
parser = argparse.ArgumentParser()
parser.add_argument("capture_time", type=int)
parser.add_argument("ssid")
parser.add_argument("token")
args = parser.parse_args()

url = "https://8b20e2c2.ngrok.io/api/upload/" + getGUID()
print(args.capture_time)
print(args.ssid)
print(args.token)
status = 200
while(status == 200):
        data = capture_packets(args.capture_time, args.ssid)
        adr = data.data.addresses
        json_adr = {"addresses": adr}
        json_payload = {"timestamp": str(int(data.timestamp)),
                        "data": json.dumps(json_adr),
                        "token": args.token}
        json_params = {"token": args.token}
        response = requests.post(url, data=json_payload)
        status = response.status_code
        print(json_payload)
        print(url)
        print(response)
os.remove("token.txt")
os.remove("ssid.txt")
