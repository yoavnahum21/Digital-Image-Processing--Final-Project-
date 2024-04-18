import comm_platform
import cv2
import pygame
import time
from button import Button
from Timer import Timer
from big_code_version import FrameProcessor
from RaceCar import RaceCar
from Hand_Detection import Player
from Mapping import Track
import numpy as np

# start game and load resources
pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('Hands-ON')
clock = pygame.time.Clock()
background = pygame.image.load('Assets/Graphics/back_ground.jpg')
leaderboard = {}
hand_cam = cv2.VideoCapture(0)
track_cam = cv2.VideoCapture(1)
player = Player('', hand_cam)
processor = FrameProcessor()
car = RaceCar(track_cam)
track = Track(track_cam)
port = comm_platform.init_port()

def finish_mode(port):
    comm_platform.Set_package_and_transmit('d', port)  # go right
    time.sleep(5)
    comm_platform.Set_package_and_transmit('r', port)  # go right

    return

def fsm(grad, port):
    if grad is None:
        comm_platform.Set_package_and_transmit('r', port)  # stop car
    elif (grad <= 0.2) and (grad >= -0.2):
        comm_platform.Set_package_and_transmit('w', port)  # go forward
    elif (grad < -0.2) and (grad >= -0.5):
        comm_platform.Set_package_and_transmit('d', port)  # go forward and right
    elif (grad > 0.2) and (grad <= 0.5):
        comm_platform.Set_package_and_transmit('y', port)  # go forward and left
    elif grad > 0.5:
        comm_platform.Set_package_and_transmit('a', port)  # go right
    elif grad < -0.5:
        comm_platform.Set_package_and_transmit('d', port)  # go right
    else:
        return
    cv2.waitKey(50)
    comm_platform.Set_package_and_transmit('r', port)
    return


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
    # We ask user to enter their name
    global player
    name = ''
    name_phase = True
    while name_phase:
        set_background(background)
        make_text_box(f"Enter Name: {name}", 100, (840, 300))

        # Event Handler for this loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[: -1]
                elif event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_RETURN:
                    name_phase = False
                else:
                    name += event.unicode
        pygame.display.update()  # update the screen with changes in this frame
    player.name = name
    player.calibration()
    print("finish")
    main_menu()


# The main game loop where the game itself happens
def play() -> None:
    # check if there is a player set
    if player is None:
        set_background(background)
        make_text_box("Player not set, returning to main menu!", 50, (840, 300))
        back_button = Button(pos=(1300, 800), text_input='Menu', font=get_font(50), base_color="#1e0b7d",
                             hovering_color='#ab0333')
        while True:
            get_mouse_pos = pygame.mouse.get_pos()
            back_button.changeColor(get_mouse_pos)
            back_button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(get_mouse_pos):
                        main_menu()
            pygame.display.update()  # update the screen with changes in this frame

    # Set up phase
    start_cond = False
    timer = Timer()
    best_lap = 10000
    penalty = 0


    while not start_cond:
        set_background(background)
        make_text_box("Place car at starting position and press SPACE!", 50, (840, 100))
        make_text_box("Press ESC to exit to main menu anytime", 30, (840, 150))

        # event handler for setup phase
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                car.take_img()
                start_cond = True
                scale_x, scale_y = 1.8 / car.car_img.shape[1], 1.8 / car.car_img.shape[0]
                car.location[1], car.location[0], car.velocity, car.orientation =\
                    processor.process_single_frame(car.car_img, 30, scale_x, scale_y)
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
    time.sleep(0.5)
    timer.start()

    # game phase
    while True:
        set_background(background)
        car.take_img()
        car.location[1], car.location[0], car.velocity, car.orientation = (
            processor.process_single_frame(car.car_img, 30, scale_x, scale_y))
        # car_surr = car.get_surrounding(track.bev_track)
        # vec = np.array([car.location[0], car.location[1], 1])
        # loc = track.persp_mat @ vec

        print(car.location)
        car.car_img = cv2.rotate(car.car_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        track_live = cv2.rotate(cv2.flip(car.car_img, 1), cv2.ROTATE_180)
        # track_live = cv2.circle(track_live, (car.location[1], car.location[0]), 10, 255)
        live_screen = pygame.surfarray.make_surface(track_live)
        live_screen_rect = live_screen.get_rect(center=(840, 450))
        screen.blit(live_screen, live_screen_rect)
        slope = player.sift()
        fsm(slope, port)
        # TODO: check track limits
        # if track_limits == True:
        #     penalty += 0.01
        # TODO: check if lap ended
        # if lap_end == True:
        #     curr_time = timer.get_timer()
        #     if curr_time + penalty < best_lap:
        #         best_lap = curr_time
        #         timer.stop()
        #         timer.start()
        #         penalty = 0
        # make_text_box("Lap Time:", 50, (200, 130))
        # make_text_box(str(timer.get_timer()), 50, (200, 180))
        # make_text_box("Speed:", 50, (200, 720))
        # make_text_box(str(car.velocity), 50, (200, 770))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                leaderboard[player.name] = best_lap
                main_menu()


# Sets the current track
def detect_map(new_track: Track):
    global leaderboard
    leaderboard = {}
    set_background(background)
    make_text_box("When the track and candles are visible", 40, (840, 50))
    make_text_box("press R to take a picture", 40, (840, 100))
    pygame.display.update()  # update the screen with changes in this frame
    # new_track.origin_img = cv2.imread("camera_test/test_img.png")
    new_track.get_track_img()
    new_track.get_bev_track()
    # new_track.get_starting_pos()
    cv2.imshow("BEV Track", new_track.bev_track)
    back_button = Button(pos=(1300, 800), text_input='Menu', font=get_font(50), base_color="#1e0b7d",
                         hovering_color='#ab0333')

    while True:
        get_mouse_pos = pygame.mouse.get_pos()
        back_button.changeColor(get_mouse_pos)
        back_button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cv2.destroyAllWindows()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(get_mouse_pos):
                    cv2.destroyAllWindows()
                    main_menu()
        pygame.display.update()  # update the screen with changes in this frame


# Shows a leader board from the game
def show_leader_board(lead_board: dict) -> None:
    set_background(background)
    make_text_box("Leader Board", 100, (840, 100))
    sorted_players = sorted(lead_board.items(), key=lambda item: item[1], reverse=True)

    # Loop over elements using the sorted players
    for p in range(len(sorted_players)):
        if p + 1 > 10:
            break
        else:
            make_text_box(f"P{p + 1}.", 30, (180, 180 + 50 * p))
            make_text_box(f"{sorted_players[p][0]}", 30, (300, 180 + 50 * p))
            make_text_box(f"{sorted_players[p][1]}", 30, (1400, 180 + 50 * p))

    back_button = Button(pos=(1300, 800), text_input='Menu', font=get_font(50), base_color="#1e0b7d",
                         hovering_color='#ab0333')
    while True:
        get_mouse_pos = pygame.mouse.get_pos()
        back_button.changeColor(get_mouse_pos)
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(get_mouse_pos):
                    main_menu()
        pygame.display.update()  # update the screen with changes in this frame


# The main menu of the game. while loop redraws each frame
def main_menu() -> None:
    while True:
        set_background(background)
        make_text_box("Hands-ON", 150, (840, 100))
        get_mouse_pos = pygame.mouse.get_pos()  # get mouse position on screen

        # Create buttons
        calib_button = Button(pos=(840, 300), text_input='Set Player', font=get_font(50), base_color="#1e0b7d",
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
                    detect_map(track)
                if play_button.checkForInput(get_mouse_pos):
                    play()
                if lead_button.checkForInput(get_mouse_pos):
                    show_leader_board(leaderboard)
                if quit_button.checkForInput(get_mouse_pos):
                    finish_mode(port)
                    pygame.quit()
                    exit()

        pygame.display.update()  # update the screen with changes in this frame


if __name__ == '__main__':
    main_menu()
