#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import time

GPIO.setmode(GPIO.BCM)

# enumeration not supported on python 2.7 so making poor man enums
whole = 1
half = 2
quarter = 4
eighth = 8

# -------------------------FUNCTIONS---------------------------
def noteStrToInt(noteStr):
  if noteStr == "whole":
    return 1;
  elif noteStr == "half":
    return 2;
  elif noteStr == "quarter":
    return 4;
  elif noteStr == "eighth":
    return 8;
  else:
    return 0;  # invalid string passed to function

def noteIntToStr(noteInt):
  if noteInt == 1:
    return "whole";
  elif noteInt == 2:
    return "half";
  elif noteInt == 4:
    return "quarter";
  elif noteInt == 8:
    return "eighth";
  else: 
    return "INVALID"; # invalid string passed to function

# beat sleep time function
def betweenBeatSleep(note, bpm):
  returnVal = (60.0/bpm) * (timeSignatureNote/note)
  return returnVal

# play song function
def PlaySong():
  noteCount = 0
  print("\n-----BEGIN SONG-----")
  for bell in bells:
    # debug
    print(bell + " " + notes[noteCount])
    # end debug
    if bell == 'W':
      time.sleep(betweenBeatSleep(int(notes[noteCount]), bpm))
    else:
      GPIO.output(pins[bell], GPIO.LOW)
      time.sleep(0.05)
      GPIO.output(pins[bell], GPIO.HIGH)
      time.sleep(betweenBeatSleep(int(notes[noteCount]), bpm))
    noteCount += 1 
  return 0

# ----------------------END OF FUNCTIONS------------------------

# ------------------- variable initializations -------------------
songFileName = ""
songFileContents = ""
songFileContentsListStepOne = []
songFileContentsListStepTwo = []
bells = []
notes = []
elementEven = False

# Time signature for all songs (for now) will be 4/4. Will always use simple time signatures (quarter note gets one beat)
timeSignatureBeats = 4.0
timeSignatureNote = 4.0

# Set the bpm value with either command line inputs or if made into a module, make a function to set this
bpm = 130 # default 95 bpm

# time to sleep between quarter notes is set by user's choice of bpm (reciprocal of bpm in sec is how often in time there is a beat)
sleepTimeBeat = 60/bpm  #in seconds

# ----------------------- end vaiable init -----------------------

# Command Line handling
if (len(sys.argv) > 2):
  print("Too many command line arguments. Exiting...")
  exit(2)
else:
  songFileName = str(sys.argv[1])

# read the song file (everything you need should just be on the first line)
with open(songFileName, 'r') as f:
  songFileContents = f.readline()

#debug
print("\n---SONG FILE CONTENTS---\n")
print(songFileContents)
#end debug

# Parse the song file into bells and note types
songFileContentsListStepOne = songFileContents.split(',')

#debug
print("\n---SONG FILE CONTENT LIST STEP ONE---\n")
print(songFileContentsListStepOne)
#end debug

for element in songFileContentsListStepOne:
  songFileContentsListStepTwo.append(element.split('-')[0])
  songFileContentsListStepTwo.append(element.split('-')[1])

#debug
print("\n---SONG FILE CONTENT LIST STEP TWO---\n")
print(songFileContentsListStepTwo)
#end debug


for element in songFileContentsListStepTwo:
  if (elementEven):
    notes.append(element)
    elementEven = False
  else:
    bells.append(element)
    elementEven = True

# init list with pin numbers for relays
#pinList = [2, 3, 4, 17, 27, 22, 10, 9]
# map pin numbers to bell color
pins = {
  'R' : 9,
  'O' : 10,
  'Y' : 22,
  'L' : 27,
  'G' : 17,
  'T' : 4,
  'B' : 3,
  'P' : 2 
}

# loop through pins and set mode and state to 'high' (Close relays by changing to low)
#for i in pinList: 
#    GPIO.setup(i, GPIO.OUT) 
#    GPIO.output(i, GPIO.HIGH)

for bell in pins:
  GPIO.setup(pins[bell], GPIO.OUT)
  GPIO.output(pins[bell], GPIO.HIGH)

# play song
try:
  PlaySong()

# End program cleanly with keyboard
except KeyboardInterrupt:
  print "  Quit"

  # Reset GPIO settings
  GPIO.cleanup()
