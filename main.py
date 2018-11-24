from appJar import gui
import requests
import json
import os.path
import sys
from wifi import Cell, Scheme

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

def connect():
    ping = requests.get(url + "ping")
    print(ping)
    if(ping.status_code == 200):
        payload = {"guid" : getGUID() }
        token = requests.post(url + "connect", data = payload)
        data = json.loads(token.text)
        print(token)
        if(token.status_code == 404):
            app.setLabel("connection-error-not-registered-label2", data["registration"])
            app.showSubWindow("connection-error-not-registered")
        else:
            token = {"token" : data["token"]}
            file = open(filename, "w+")
            file.write(json.dumps(token))
            file.close()
            cmd = "python3 collect_data.py " + str(5) + " " + "hackathon" + " " + token["token"]
            os.system(cmd)

            # zavolat járu
    else:
        app.showSubWindow("connection-error")

        #ukázat app běží (49 - 52 řádek)


app=gui("Wifiπ", "fullscreen")
app.setSticky("news")
app.setExpand("both")
app.setFont(20)

url = "https://8b20e2c2.ngrok.io/api/"
filename = "token.txt"
guid = getGUID()
interval = 15 * 60

if os.path.exists(filename) == True:
    file = open(filename, "r")
    content = file.read()

    #zasijsit připojení (tzv. pokud už rasp bylo připojeno, připojíš ho, asi se připojí automaticky)

    ping = requests.get(url + "ping")
    if(ping.status_code == 200):
        payload = { "token" : json.loads(content)["token"], "guid" : guid }
        print(payload)
        isvalid = requests.get(url + "verify-token", params = payload)
        print(isvalid.text)
        if(json.loads(isvalid.text)["valid"]):
            print("cool")
            payload = {"guid" : guid }
            response = requests.post(url + "connect", data = payload)
            data = json.loads(response.text)


def close(btn):
    app.hideAllSubWindows(useStopFunction=False)

def seeWiFi(btn):
    cmd = "sudo rfkill unblock wifi"
    os.system(cmd)

    cmd = "sudo ifconfig wlan0 up"
    os.system(cmd)

    wlans = Cell.all("wlan0")
    ssids = []

    for cell in wlans:
        if(cell.ssid != ""):
            ssids.append(cell.ssid)

    # ssids = [cell.ssid for cell in Cell.all('wlan0')]

    if(len(ssids) != 0):
        app.clearOptionBox("ssids")
        app.changeOptionBox("ssids", ssids, 0)

    app.showSubWindow("Wifi-connect")


def seeGUID(btn):
    if(guid == "ERORR"):
        app.showSubWindow("GUID-error")
    else:
        app.setLabel("GUID-success-label", "Vaše GUID: " + guid)
        app.showSubWindow("GUID-success")


def connectToWiFi(btn):
    ssid = app.getOptionBox("ssids")
    password = app.getEntry("password") 

    #uložit do raspberry
    cmd = "add_network"
    os.system(cmd)

app.startSubWindow("connection-error", title=" ", modal=True)
app.setSize(600, 250)
app.addLabel("connection-error-label1", "Nelze se připojit na službu.")
app.addLabel("connection-error-label2", "Zkontrolujte připojení k Wi-Fi")
app.addNamedButton("OK", "ok-1", close)
app.setButtonSticky("ok-1", "right")
app.stopSubWindow()

app.startSubWindow("connection-error-not-registered", title=" ", modal=True)
app.setSize(600, 250)
app.addLabel("connection-error-not-registered-label1", "Nejste zaregistrovaní, registraci provedete zde:")
app.addLabel("connection-error-not-registered-label2", "")
app.addNamedButton("OK", "ok-2", close)
app.setButtonSticky("ok-2", "right")       
app.stopSubWindow()            

app.startSubWindow("GUID-error", title=" ", modal=True)
app.setSize(600, 250)
app.addLabel("GUID-error-label", "GUID nelze přečíst")
app.addNamedButton("OK", "ok-3", close)
app.setButtonSticky("ok-3", "right")          
app.stopSubWindow()

app.startSubWindow("GUID-success", title=" ", modal=True)
app.setSize(600, 250)
app.addLabel("GUID-success-label", "", 0, 0, 3)
app.addLabel("Web", "https://8b20e2c2.ngrok.io/App/register", 1, 0, 2)   
app.addNamedButton("OK", "ok-4", close)
app.setButtonSticky("ok-4", "right")     
app.stopSubWindow()

app.startSubWindow("Wifi-connect", title=" ", modal=True)
app.setSize(600, 250)
app.addLabel("avaible-ssids", "Dostupné sítě", 0, 0, 1)
app.addLabelOptionBox("ssids", "", 1, 0, 1)
app.addLabel("password-label", "Heslo", 0, 1, 1)
app.addEntry("password", 1, 1, 1)   
app.addNamedButton("Připojit", "ok-5", connectToWiFi, 2, 1, 1)
app.setButtonSticky("ok-5", "right")
app.addNamedButton("Zrušit", "ok-6", close, 2, 1, 1)
app.setButtonSticky("ok-6", "middle")  
app.stopSubWindow()

app.addImageButton("clickme", seeWiFi, "signal.png", 0, 0)
app.addButton("GUID", seeGUID, 0, 1)
app.addButton("připojit", connect, 0, 2)

app.go()