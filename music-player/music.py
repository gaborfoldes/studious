
import RPi.GPIO as GPIO
from omxplayer import OMXPlayer
from os import walk
from time import sleep
import random
from os import system
from pprint import pprint

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
 '8': 'hannukah.mp3',
 '#': 'radio'
}

radio = 0
radiodir = songdir # + 'Music Together/'
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

def play_song(song):
  global player
  if 'player' in globals(): player.quit()
  print 'Playing ' + song
  player = OMXPlayer(song, args = ['--no-osd', '--no-keys', '-o', 'local'])
  paused = 0
  

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

      elif k == 'A':
        system('curl -X POST https://api.particle.io/v1/devices/3c002f000547343337373737/xmas -d access_token=e4347a6c2c5f936c1e249c215f48a783d9696b31 -d setTo=switch1')

      elif k == 'B':
        system('curl -X POST https://api.particle.io/v1/devices/3c002f000547343337373737/xmas -d access_token=e4347a6c2c5f936c1e249c215f48a783d9696b31 -d setTo=switch2')

      elif k == '#':
        print 'Turning radio ON...'
        radio = 1
        play_song(random.choice(radio_songs))

      elif k == '0':
        if 'player' in globals(): player.quit()
        print 'Turning radio OFF...'
        radio = 0

      elif k in songs:
        play_song( songdir + songs[k] )

      sleep(0.25)

    if radio == 1:
      if player._process_monitor._Thread__stopped:
        play_song(random.choice(radio_songs))

except KeyboardInterrupt:
  if 'player' in globals(): player.quit()

finally:
  GPIO.cleanup()


