import time, pyautogui, os, cv2, smtplib, ssl
import numpy as np

rPar = [910,68,5,5] 
rPar2 = [1605,770,5,5]

#positions of Overwatch characters on a 1080 x 1920 computer screen
heroPositionsY = 925
heroPositionsX = {'diva':111,'dva':111,'d.va':111,'orisa':159,'reinhart':216,'roadhog':272,
'rein':216,'sigma':318,'hog':272,'sig':318,'monkey':375,'ball':428,'wrecking ball':428,
'doom':675,'junk':885,'cree':938,'reap':1109,'soldier':1161,'sym':1261,'torb':1319,
'widow':1429,'bap':1560,'brig':1611,'zen':1837,'winston':375,'hammond':428,'zarya':482,
'ashe':564,'bastion':616,'doomfist':675,'echo':720,'genji':771,'hanzo':836,'junkrat':885,
'mccree':938,'mei':995,'pharah':1051,'reaper':1109,'soldier 76':1161,'sombra':1215,
'symmetra':1261,'torbjorn':1319,'tracer':1381,'widowmaker':1429,'ana':1503,'baptiste':1560,
'brigette':1611,'lucio':1661,'mercy':1717,'moira':1773,'zenyatta':1837}
selectButtonX = 965
selectButtonY = 1009

server = smtplib.SMTP("smtp.gmail.com:587")
auth = ('overwatchgamestarting@gmail.com', 'Alohabobs11')

#asking user to input which Overwatch character they would like the program to instant lock
hero = input('Please select which hero you would like to be: ')
heroSelectionXY = (heroPositionsX.get(hero),heroPositionsY)
selectButtonXY = (selectButtonX,selectButtonY)

#initializing smtplib for email notification
def initGmail():

    server.ehlo()
    server.starttls()
    server.login(auth[0],auth[1])

#sending message
def send():

    try:
        message = 'Subject: Overwatch match starting!!!'
        server.sendmail(auth[0], auth[0], message)
        server.quit()
        print('Game found!\nNotification sent!')
    except:
        print('Unable to send notification...')

#instant locks an Overwatch character based on previous user input
def instaLock():

    if hero == '':
        print('No hero has been selected to be instalocked!')
    else:
        pyautogui.click(heroSelectionXY)
        time.sleep(.3)
        pyautogui.click(selectButtonXY)
        print(hero + ' has been selected!')

#primary function which determines if an online match has been found based on color values of
#specific locations on the screen
def gameQueue():

    time.sleep(.5)

    #initialize values for spot and spot2 for later use
    spot = 0
    spot2 = 0

    #perform screenshots that will be used to determine whether an online match has been found
    sc = pyautogui.screenshot()
    os.remove('C:\OWSC\\OWSC.png')
    sc.save('C:\OWSC\\OWSC.png')

    #assign positions on the screenshot as roi and roi2 (region of interest)
    rawGameScreen = cv2.imread('C:\OWSC\\OWSC.png')
    roi = rawGameScreen[rPar[1]:rPar[1]+rPar[2],rPar[0]:rPar[0]+rPar[3]]
    roi2 = rawGameScreen[rPar2[1]:rPar2[1]+rPar2[2],rPar2[0]:rPar2[0]+rPar2[3]]

    #Purple "Match Found" Notification
    avg_color_per_row = np.average(roi, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    #below are the parameters for a successful match found
    #[251.52 160.64 222.44]
    if avg_color[0] > 251 and avg_color[0] < 252:
        if avg_color[1] > 160 and avg_color[1] < 161:
            if avg_color[2] > 222 and avg_color[2] < 223:
                spot = 1

    #Join Voice Chat
    avg_color_per_row2 = np.average(roi2, axis=0)
    avg_color2 = np.average(avg_color_per_row2, axis=0)
    #below are the parameters for a successful match found
    #[188. 117.  28.]
    if avg_color2[0] == 188:
        if avg_color2[1] == 117:
            if avg_color2[2] == 28:
                spot2 = 1

    #here we send an email notification based on whether one of the top two requirements
    #were met
    if spot == 1:
        send()
        
    if spot2 == 1:
        print('Instalocking '+hero+'...')
        instaLock()
        if spot != 1:
            send()
        raise SystemExit(0)

if __name__ == "__main__":
    initGmail()
    print('Searching for game...')
    while True:
        gameQueue()
