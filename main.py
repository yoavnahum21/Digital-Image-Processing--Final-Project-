# from Vid_Read import Video_Read
# import comm_platform
import cv2
import pygame
from button import Button

# start game and load resources
pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('Hands-ON')
clock = pygame.time.Clock()
background = pygame.image.load('Assets/Graphics/back_ground.jpg')


# Loads the font with given size
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Fonts/VIDEOPHREAK.ttf", size)


# Sets background and title
def set_background_title(img):
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
    print("CALIBRATION NOT IMPLEMENTED YET")


# The main game loop where the game itself happenes
def play() -> None:
    # Set up phase written in pseudocode
    ''' 1. prompt player to put car in starting position
        2. ask player to press a key when done
        3. once done - check if car at good position
        4. if car at good position start countdown
        5. play!
    '''
    start_cond = False
    while not start_cond:
        set_background_title(background)
        make_text_box("Place car at starting position and press SPACE!", 50, (840,100))
        make_text_box("Press ESC to exit to main menu anytime",30, (840,150))

        # event handler for setup phase
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("SPACE RANGERS")
                # TODO: 1.get car position
                # 2. get starting position
                # if starting position good set start_cond to True
                # else write starting position bad
            pygame.display.update()


    # game phase
    ''' 0.1 build UI
        1. start timer
        2. get player input from hand camera and send to car
        3. get car location
        4. check for lap end (if true reset timer and save best lap)
        5. check for track limits
        6. if ESC pressed return to main menu
    '''


# Sets the current track
def detect_map():
    print('DETECT MAP NOT IMPLEMENTED YET')


# Shows a leader board from the game
def show_leader_board():
    print('LEADER BOARD NOT IMPLEMENTED YET')


# The main menu of the game. while loop redraws each frame
def main_menu() -> None:
    while True:
        set_background_title(background)
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
