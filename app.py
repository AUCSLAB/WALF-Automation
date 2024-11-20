import pygame
import os 
from mutagen.mp3 import MP3
from collections import deque

with open('songs.txt', mode='r') as f:
   l = [ e.replace('\n', '') for e in f.readlines() if e != '\n' ]

q = deque(l)
def automatic_folder_reader(folder, output):
   with open(output, 'w') as file:
      musiclst=os.listdir(folder)
      for i in range(len(musiclst)):
         file.write(musiclst[i]+'\n')
automatic_folder_reader('music','songs.txt')
# pygame initilization
pygame.init()
pygame.mixer.init()

# create the screen
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
background = pygame.image.load('./images/BackGround.jpg')


# title and icon
pygame.display.set_caption('Music Player')
icon = pygame.image.load('./images/walf.jpg')
pygame.display.set_icon(icon)

# load button images and make them 200x200
play_img = pygame.image.load('./images/play.png').convert_alpha()
play_img = pygame.transform.smoothscale(play_img, (150, 150))
pause_img = pygame.image.load('./images/pause.png').convert_alpha()
pause_img = pygame.transform.smoothscale(pause_img, (150, 150))
next_img = pygame.image.load('./images/next.png').convert_alpha()
next_img = pygame.transform.smoothscale(next_img, (150, 150))
callsign_img = pygame.image.load('./images/callsign.png').convert_alpha()
callsign_img = pygame.transform.smoothscale(callsign_img, (150, 33))
X_img=pygame.image.load('./images/x.png').convert_alpha()
X_img = pygame.transform.smoothscale(X_img, (50, 50))
window_img=pygame.image.load('images/Window.png')
window_img=pygame.transform.smoothscale(window_img,(50,50))
max_img=pygame.image.load('images/max.png').convert_alpha()
max_img=pygame.transform.smoothscale(max_img,(100,50))
logo_img=pygame.image.load('./images/logo.png').convert_alpha()
logo_img=pygame.transform.smoothscale(logo_img, (800,200))
logo_rect=logo_img.get_rect(center=(screen.get_width() // 2,1/4*((screen.get_height()))-50))
logo1_img=pygame.image.load('./images/logo1.png').convert_alpha()
logo1_img=pygame.transform.smoothscale(logo1_img, (500,250))
logo1_rect=logo1_img.get_rect(center=((screen.get_width()-150),((screen.get_height()-110))))

   
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
      self.rect.center = (screen.get_width() // 2, screen.get_height() - self.rect.height // 2 - 53)
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
      screen.blit(self.image, (self.rect))



# callsign button class
CALLSIGN_BUTTON_PRESSED = pygame.USEREVENT + 3
callsign_button_pressed = pygame.event.Event(CALLSIGN_BUTTON_PRESSED)
class callsignButton():
   def __init__(self, image):
      self.image = image
      self.rect = self.image.get_rect()
      
      self.clicked = False
   
   def draw(self):
      self.rect.center = (screen.get_width() // 2, screen.get_height() - self.rect.height // 2 - 20)
      mouse_pos = pygame.mouse.get_pos()
      if self.rect.collidepoint(mouse_pos):
         if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
      if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
         pygame.event.post(callsign_button_pressed)
         self.clicked = False

      # draw button on screen
      screen.blit(self.image, (self.rect))

class Button:
   def __init__(self,image):
      self.img=image
      self.rect=self.img.get_rect()
      
      self.click=False
   def draw(self):
      
      mouse_pos = pygame.mouse.get_pos()
      if self.rect.collidepoint(mouse_pos):
         if pygame.mouse.get_pressed()[0]:
            self.click=True
      screen.blit(self.img, (self.rect))

# create button instances
next_button = Button(next_img)
next_button.rect.center = (screen.get_width() // 2+50, screen.get_height() - next_button.rect.height // 2 - 53)
button = PlayPauseButton(play_img, pause_img)
callsign_button = callsignButton(callsign_img)
XButton= Button(X_img)
XButton.rect.center=(screen.get_width()-25, 0+25)
WindowButton= Button(window_img)
WindowButton.rect.center=(screen.get_width()-80, 0+25)
FullScreen=Button(max_img)
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
   song = './music/' + next_song
   if '.mp3' not in song:
      song += '.mp3'
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
Windowed=False
x=0
y=0
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
      elif event.type == pygame.QUIT or XButton.click==True:
         running = False
      elif next_button.click== True:
         play_next_song()
      elif WindowButton.click==True:
         screen = pygame.display.set_mode((900,600), pygame.RESIZABLE)
         logo1_img=pygame.transform.smoothscale(logo1_img, (400,200))
         logo_rect.x-=200
         WindowButton.click=False
         Windowed=True
         
      elif FullScreen.click==True:
         screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
         logo1_img=pygame.transform.smoothscale(logo1_img, (500,250))
         logo_rect.x+=200
         FullScreen.click=False
         Windowed=False
         FullScreen.draw()
   background = pygame.transform.scale(background, screen.get_size())
   screen.blit(background,(0,0))  
   if playing == False: # hide callsign button if music is playing
    callsign_button.draw()
   button.draw()
   next_button.draw()
       
   if Windowed:
      FullScreen.rect.center=(screen.get_width()-35, 0+25)
      FullScreen.draw()
      if screen.get_width()>600:
         screen.blit(logo1_img,(screen.get_width()-300,screen.get_height()-180))
   else:
      XButton.draw()
      screen.blit(logo_img,(logo_rect))
      screen.blit(logo1_img,(logo1_rect))

      WindowButton.draw()
   
         
         
   pygame.display.update()

pygame.quit()
