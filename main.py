# from Vid_Read import Video_Read
# import comm_platform
import cv2
import pygame
from button import Button
from Timer import Timer
import time
from Hand_Detection import Player

# start game and load resources
pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('Hands-ON')
clock = pygame.time.Clock()
background = pygame.image.load('Assets/Graphics/back_ground.jpg')
leaderboard = {}
player = None


# Loads the font with given size
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Fonts/VIDEOPHREAK.ttf", size)


# Sets background and title
def set_background(img):
    screen.blit(img, (0, 0))
    screen.blit(img, (751, 0))
    screen.blit(img, (0, 751))
    screen.blit(img, (751, 751))


# make a text box in position
def make_text_box(string: str, size: int, position: tuple):
    text = get_font(size).render(string, True, "#1e0b7d")
    tex_rect = text.get_rect(center=position)
    screen.blit(text, tex_rect)


# Get player max reverse, zero and max throttle hand positions
def calibrate():
    # TODO: build this function
    player = Player(#TODO: fill req)


# The main game loop where the game itself happens
def play() -> None:

    # check if there is a player set
    if player is None:
        set_background(background)
        make_text_box("Player not set, returning to main menu!", 50, (840, 450))
        main_menu()

    # Set up phase
    start_cond = False
    timer = Timer()
    best_lap = 9999999
    penalty = 0

    while not start_cond:
        set_background(background)
        make_text_box("Place car at starting position and press SPACE!", 50, (840, 100))
        make_text_box("Press ESC to exit to main menu anytime",30, (840, 150))

        # event handler for setup phase
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_cond = True
                # TODO: 1.get car position
                # TODO: 2. get starting position
                # TODO: if starting position good set start_cond to True
                # TODO: else write starting position bad
            pygame.display.update()

    # finished set up not countdown to start game
    set_background(background)
    make_text_box("GET READY!", 200, (840, 450))
    pygame.display.update()
    time.sleep(1)
    set_background(background)
    make_text_box("3", 300, (840, 450))
    pygame.display.update()
    time.sleep(1)
    set_background(background)
    make_text_box("2", 300, (840, 450))
    pygame.display.update()
    time.sleep(1)
    set_background(background)
    make_text_box("1", 300, (840, 450))
    pygame.display.update()
    time.sleep(1)
    set_background(background)
    make_text_box("GO!", 300, (840, 450))
    pygame.display.update()
    timer.start()

    # game phase
    while True:
        # TODO: draw mop
        # TODO: get player input and send to car
        # TODO: get car location
        # TODO: check track limits
        if track_limits == True:
            penalty += 0.01
        # TODO: check if lap ended
        if lap_end == True:
            curr_time = timer.get_timer()
            if curr_time + penalty < best_lap:
                best_lap = curr_time
                timer.stop()
                timer.start()
                penalty = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # TODO: make a player object
                leaderboard[player.name] = best_lap
                main_menu()


# Sets the current track
def detect_map():
    print('DETECT MAP NOT IMPLEMENTED YET')


# Shows a leader board from the game
def show_leader_board():



# The main menu of the game. while loop redraws each frame
def main_menu() -> None:
    while True:
        set_background(background)
        make_text_box("Hands-ON", 150, (840, 100))
        get_mouse_pos = pygame.mouse.get_pos()  # get mouse position on screen

        # Create buttons
        calib_button = Button(pos=(840, 300), text_input='Calibration', font=get_font(50), base_color="#1e0b7d",
                              hovering_color='#ab0333')
        detect_button = Button(pos=(840, 400), text_input='Map Detection', font=get_font(50), base_color="#1e0b7d",
                               hovering_color='#ab0333')
        play_button = Button(pos=(840, 500), text_input='Play', font=get_font(50), base_color="#1e0b7d",
                             hovering_color='#ab0333')
        lead_button = Button(pos=(840, 600), text_input='Leader Board', font=get_font(50), base_color="#1e0b7d",
                             hovering_color='#ab0333')
        quit_button = Button(pos=(840, 700), text_input='Quit', font=get_font(50), base_color="#1e0b7d",
                             hovering_color='#ab0333')

        # Check mouse is on button and draw button on screen accordingly
        for button in [calib_button, detect_button, play_button, lead_button, quit_button]:
            button.changeColor(get_mouse_pos)
            button.update(screen)

        # Event handler for buttons clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if calib_button.checkForInput(get_mouse_pos):
                    calibrate()
                if detect_button.checkForInput(get_mouse_pos):
                    detect_map()
                if play_button.checkForInput(get_mouse_pos):
                    play()
                if lead_button.checkForInput(get_mouse_pos):
                    show_leader_board()
                if quit_button.checkForInput(get_mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()  # update the screen with changes in this frame


if __name__ == '__main__':
    main_menu()
