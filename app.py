import pygame
from mutagen.mp3 import MP3
from collections import deque

with open('songs.txt', mode='r') as f:
   l = [ e.replace('\n', '') for e in f.readlines() if e != '\n' ]

q = deque(l)

# pygame initilization
pygame.init()
pygame.mixer.init()

# create the screen
screen = pygame.display.set_mode((200, 233))

# title and icon
pygame.display.set_caption('Music Player')
icon = pygame.image.load('./images/walf.jpg')
pygame.display.set_icon(icon)

# load button images and make them 200x200
play_img = pygame.image.load('./images/play.png').convert_alpha()
play_img = pygame.transform.smoothscale(play_img, (200, 200))
pause_img = pygame.image.load('./images/pause.png').convert_alpha()
pause_img = pygame.transform.smoothscale(pause_img, (200, 200))
callsign_img = pygame.image.load('./images/callsign.png').convert_alpha()
callsign_img = pygame.transform.smoothscale(callsign_img, (200, 33))

# play/pause button class
BUTTON_PRESSED = pygame.USEREVENT + 1
button_pressed = pygame.event.Event(BUTTON_PRESSED)
class PlayPauseButton:
   def __init__(self, play_image, pause_image):
      self.images = [play_image, pause_image]
      self.playing = 0
      self.image = self.images[self.playing]
      self.rect = self.image.get_rect()
      self.clicked = False

   def draw(self):
      # get mouse position
      mouse_pos = pygame.mouse.get_pos()

      if self.rect.collidepoint(mouse_pos):
         if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
      if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
         pygame.event.post(button_pressed)
         self.clicked = False
         if self.playing:
            self.playing = 0
         else:
            self.playing = 1

      # update image
      self.image = self.images[self.playing]
      # draw button on screen
      screen.blit(self.image, (0, 0))

# callsign button class
CALLSIGN_BUTTON_PRESSED = pygame.USEREVENT + 3
callsign_button_pressed = pygame.event.Event(CALLSIGN_BUTTON_PRESSED)
class callsignButton():
   def __init__(self, image, x, y):
      self.image = image
      self.rect = self.image.get_rect()
      self.rect.topleft = (x, y)
      self.clicked = False
   
   def draw(self):
      mouse_pos = pygame.mouse.get_pos()
      if self.rect.collidepoint(mouse_pos):
         if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
      if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
         pygame.event.post(callsign_button_pressed)
         self.clicked = False

      # draw button on screen
      screen.blit(self.image, (self.rect.x, self.rect.y))


# create button instances
button = PlayPauseButton(play_img, pause_img)
callsign_button = callsignButton(callsign_img, 0, 200)

# song handling
SONG_END = pygame.USEREVENT + 2
pygame.mixer.music.set_endevent(SONG_END)

def play_next_song():
   """
   Plays song at front of queue and moves it to the back.
   """
   next_song = q.popleft()
   print(f'Currently playing {next_song}')
   q.append(next_song)
   song = './music/' + next_song + '.mp3'
   pygame.mixer.music.load(song)
   pygame.mixer.music.play()

   # returns length of song in minutes
   return round(MP3(song).info.length, 2)

def play_callsign():
   """
   Plays the callsign without changing current song
   """
   # save pause location
   pause_time = pygame.mixer.music.get_pos()

   # play callsign
   callsign_sound = './callsign.mp3'
   pygame.mixer.music.load(callsign_sound)
   pygame.mixer.music.rewind()
   pygame.mixer.music.play()
   
   # move song at back of queue to front of queue
   q.appendleft(q.pop())
   return pause_time


# get the first song ready
t = 0
t += play_next_song()
pygame.mixer.music.pause()

# song loop
running = True
playing = False
callsign_played = False
pause_time = 0
skip = True
while running:
   for event in pygame.event.get():
      if event.type == SONG_END:
         if callsign_played: # callsign was manually played
            callsign_played = False
            t = 0
            t += play_next_song()
            pygame.mixer.music.set_pos(pause_time * .001) # music tends to resume from an earlier point than actual pause
            pygame.mixer.music.pause()
            pause_time = 0
         elif t >= 30 * 60: # play callsign after total playtime exceeds 30min
            pygame.mixer.music.load('./callsign.mp3')
            pygame.mixer.music.play()
            t = 0
         else: # play next song after a song ends
            print('-- playing next song --')
            t += play_next_song()
      elif event.type == BUTTON_PRESSED: # play/pause button
         if playing:
            pygame.mixer.music.pause()
            playing = False
         else:
            pygame.mixer.music.unpause()
            playing = True
      elif event.type == CALLSIGN_BUTTON_PRESSED: # callsign button pressed
         print('-- playing callsign --')
         pause_time = play_callsign()
         callsign_played = True
      elif event.type == pygame.QUIT:
         running = False

   # background
   screen.fill((210, 210, 210))
   if playing == False: # hide callsign button if music is playing
      callsign_button.draw()
   button.draw()
   pygame.display.update()

pygame.quit()