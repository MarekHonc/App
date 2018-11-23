from appJar import gui
import requests
import json

url = "https://8b20e2c2.ngrok.io/api/"

app=gui("Wifiπ", "fullscreen")
app.setSticky("news")
app.setExpand("both")
app.setFont(20)

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

def close(btn):
    app.hideAllSubWindows(useStopFunction=False)

def connectToWiFi(btn):
    x = 15
    y = x + 2

def seeGUID(btn):
    guid = getGUID()

    if(guid == "ERORR"):
        app.showSubWindow("GUID-error")
    else:
        app.setLabel("GUID-success-label", "Vaše GUID: " + guid)
        app.showSubWindow("GUID-success")

def connect(btn):
    ping = requests.get(url + "ping")
    if(ping.status_code == 200):
        payload = {"guid" : getGUID }
        token = requests.post(url + "connect", data = payload)
        data = json.loads(token.text)

        if(token.status_code == 404):
            app.setLabel("connection-error-not-registered-label2", data["registration"])
            app.showSubWindow("connection-error-not-registered")

        else:
            token = data["token"]
    else:
        app.showSubWindow("connection-error")

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

app.addImageButton("clickme", connectToWiFi, "signal.png", 0, 0)
app.addButton("GUID", seeGUID, 0, 1)
app.addButton("připojit", connect, 0, 2)

app.go()