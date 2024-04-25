# This file was created by ishan routray
'''
health bar (working on adding a second enemy so i can work on my health)
coin bar/coin counter - DONE
moving enemies - DONE
create start screen
'''

# Import modules
import pygame as pg
from settings import *
from sprites import *
from utils import *
from health_bar import *
from random import randint
import sys
from os import path
from math import floor

LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
LEVEL3 = "level3.txt"
# This function draw_health_bar draws a health bar on a surface at a specified position with a given percentage:
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# Creating the base bleprints
class Game:
    # Initializer -- sets up the game
    def __init__(self):
        # Setting -- set canvas, width, eght, and title
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting pygame clock 
        self.clock = pg.time.Clock()
        self.load_data()
    # his function load_data serves the purpose of initializing game resources such as images,
    # sounds, and map data, by setting up their respective file paths and loading them into memory.
    def load_data(self):
        # game_folder = path.dirname(__file__)
        # self.img_folder = path.join(game_folder, 'images')
        # self.snd_folder = path.join(game_folder, 'sounds')
        self.game_folder = path.dirname(__file__)
        # Setting image and sound folder paths relative to the game folder
        self.img_folder = path.join(self.game_folder, 'images')
        self.snd_folder = path.join(self.game_folder, 'sounds')
        # creates images for characters through converting a png 
        self.player_img = pg.image.load(path.join(self.img_folder, 'drake.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, 'shrek.png')).convert_alpha()
        self.BossMob_img = pg.image.load(path.join(self.img_folder, 'panda.png')).convert_alpha()
        self.mob2_img = pg.image.load(path.join(self.img_folder, 'python.png')).convert_alpha()
        # Initializing an empty list for map data
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        self.currLvl = LEVEL1
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    # This change_level method facilitates the transition to a new game level
    def change_level(self, lvl):
        self.currLvl = lvl
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'b':
                    Mob(self, col, row)
                if tile == 'H':
                    HealthPowerUp(self, col, row)
                if tile == 'S':
                    SlowPowerUp(self, col, row)
                if tile == 'l':
                    Mob2(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'M':
                    BossMob(self, col, row)
    
    # Create run method which runs the whole GAME
    def new(self):
        # loading sound for use...not used yet
        # pg.mixer.music.load(path.join(self.snd_folder, 'soundtrack2.mp3'))
        # self.collect_sound = pg.mixer.Sound(path.join(self.snd_folder, 'sfx_sounds_powerup16.wav'))
        # create timer
        # This snippet initializes game resources, creates sprite groups, and sets up timers.
        self.cooldown = Timer(self)
        self.testclass = Test()
        print("start the game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()

        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        # This loop iterates through the map data, creating game objects based on the tile types:
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'H':
                    HealthPowerUp(self, col, row)
                if tile == 'S':
                    SlowPowerUp(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'l':
                    Mob2(self, col, row)
                if tile == 'b':
                    Mob(self, col, row)
                if tile == 'M':
                    BossMob(self, col, row)
    
    # Runs our game
    def run(self):
        # start playing sound on infinite loop (loops=-1)
        # pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def quit(self):
         pg.quit()
         sys.exit()
      # This update method manages the game state and progression:
    def update(self):
        # Update cooldown
        # Updates self
        self.cooldown.ticking()
        # Update all sprites
        self.all_sprites.update()
        # Check player's hitpoints and perform actions accordingly
        if self.player.hitpoints < 1:
            # Show death screen
            self.show_death_screen()
            # Show mad screen
            self.show_mad_screen()
            # Change level to LEVEL1
            self.change_level(LEVEL1)
            # Check player's moneybag count and current level, change level accordingly
        if 2 < self.player.moneybag < 4 and self.currLvl != LEVEL2:
             self.change_level(LEVEL2)
              # Check if player's moneybag count exceeds 4, change level to LEVEL3
        if self.player.moneybag > 4:
            self.change_level(LEVEL3)
    # just drwaws our grid
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    # This draw_text method is used to render text onto a surfaces
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    # This draw method handles rendering elements onto the screen:
    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        # draw the timer
        self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        self.draw_text(self.screen, str(self.cooldown.event_time), 24, WHITE, WIDTH/2 - 32, 80)
        self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)
        draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y-8, self.player.hitpoints)   
        pg.display.flip()

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         Allows for the character to move lefts
            #         self.player1.move(dx=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_w:
            #         Allows for the character to move up
            #         self.player1.move(dy=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_d:
            #         Allows for the character to move right
            #         self.player1.move(dx=1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_s:
            #         Allows for the character to move down
            #         self.player1.move(dy=1)

    # These methods display different screens with messages and wait for a key press:
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "u ready? press any key for hell", 24, WHITE, WIDTH/2.75, HEIGHT/2.25)
        pg.display.flip()
        self.wait_for_key()
    # Display the death screen with a message and wait for any key press
    def show_death_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "dawg u trash", 40, WHITE, WIDTH/3.75, HEIGHT/2.25)
        pg.display.flip()
        self.wait_for_key()
    # Display the "mad" screen with a message and wait for any key press
    def show_mad_screen(self):
        self.screen.fill(BGCOLOR) 
        # Fill the screen with background color
        self.draw_text(self.screen, "so we're in copper", 40, WHITE, WIDTH/3.75, HEIGHT/2.25)
        pg.display.flip()
        # Update the display
        self.wait_for_key()
        # Wait for a key press to continue
# Wait for a key press or a quit event
    def wait_for_key(self):
        waiting = True
         # Set the flag for waiting
        while waiting:
            self.clock.tick(FPS)
            # Cap the frame rate
            for event in pg.event.get():
                # Check for events
                if event.type == pg.QUIT:
                    # If the event is quitting, exit
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    # If the event is a key release, stop waiting
                    waiting =  False

# Create a new game
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    # create new game
    g.new()
    # run the game
    g.run()
g.show_go_screen()
g.run()

def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
 
            if str(hits[0].__class__.__name__) == "PowerUp":
                print ("You just got Powered Up!")




def load_random_level(self):
        # Select a random level from the available level files
        level_files = ["level1.txt", "level2.txt", "level3.txt"]
        random_level = choice(level_files)
        game_folder = path.dirname(__file__)
        # Reload the game with the selected level
        self.map_data = []  # Clear existing map data
        with open(path.join(game_folder, random_level), 'rt') as f:
            for line in f:
                self.map_data.append(line)
   
   
        self.new()
 
        def load_data(self):
                #the following code under game_flder until self.map_data was given to us from mr CoZart fully
         game_folder = path.dirname(__file__)
        self.map_data = []
       
        r = Random()
        level_files = ["level1.txt", "level2.txt", "level3.txt"]
       
        LEVEL = r.choice(level_files)
        '''
        The with statement is a context manager in Python.
        It is used to ensure that a resource is properly closed or released
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, LEVEL), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
       
        def new(self):
    #These define the groups
        #I need to add to it (almost)everytime I add a feture that needs to be loaded in the game
         print("create new game...")
        self.cooldown = Timer(self)
        self.pov = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.healup = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.speed = pg.sprite.Group()
        self.kill_wall = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.nosee_wall = pg.sprite.Group()
        self.sprinting = pg.sprite.Group()
        self.keys = pg.sprite.Group()
        self.keywall = pg.sprite.Group()
        self.lookskeywall = pg.sprite.Group()
        self.next_level_wall = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        self.load_random_level