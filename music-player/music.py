
import RPi.GPIO as GPIO
from omxplayer import OMXPlayer
from os import walk
from time import sleep
import random

rows = [0, 4, 25, 24]
cols = [23, 22, 21, 18]

keypad = [
  ['1', '2', '3', 'A'],
  ['4', '5', '6', 'B'],
  ['7', '8', '9', 'C'],
  ['*', '0', '#', 'D']
]

songdir = '/home/pi/Music/'
songs = {
 '1': 'santa_town.mp3',
 '2': 'jingle.mp3',
 '3': 'feliz_navidad.mp3',
 '4': 'frosty.mp3',
 '5': 'housetop.mp3',
 '6': 'little_snowman.mp3',
 '7': 'monkeys.mp3',
 '#': 'radio'
}

radiodir = songdir + 'Music Together/'
radio_songs = []
for (dirpath, dirnames, filenames) in walk(radiodir):
  radio_songs.extend([dirpath + '/' + f for f in filenames])

GPIO.setmode(GPIO.BCM)
GPIO.setup(rows, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(cols, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def get_key():
  pressed = [ [0 for x in range(len(cols))] for y in range(len(rows)) ]
  key = ''
  for y in range(len(rows)):
    GPIO.output(rows[y], GPIO.HIGH)
    for x in range(len(cols)):
      if GPIO.input(cols[x]):
        pressed[y][x] = 1
        key = keypad[y][x]
    GPIO.output(rows[y], GPIO.LOW)
  return key

try:

  while True:
    k = get_key()

    if k != '':

      print 'Pressed: ' + k
      if k == '*' and 'player' in globals():
        if paused:
          player.play()
          print 'Playing...'
          paused = 0
        else:
          player.pause()
          print 'Paused...'
          paused = 1

      elif k in songs:
        if 'player' in globals(): player.quit()
        song = random.choice(radio_songs) if songs[k] == 'radio' else songdir + songs[k]
        print 'Playing ' + song
        player = OMXPlayer(song)
        paused = 0

      sleep(0.25)    

except KeyboardInterrupt:
  if 'player' in globals(): player.quit()

finally:
  GPIO.cleanup()


