
import RPi.GPIO as GPIO
from omxplayer import OMXPlayer
from time import sleep

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
 '1': 'santa_town.mp3'
}

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

      if k == '*' and 'player' in globals():
        if paused:
          player.play()
          paused = 0
        else:
          player.pause()
          paused = 1

      elif k in songs:
        if 'player' in globals(): player.quit()
        player = OMXPlayer(songs[k])
        paused = 0

      sleep(0.25)    

except KeyboardInterrupt:
  if 'player' in globals(): player.quit()

finally:
  GPIO.cleanup()


