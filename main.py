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


# main func

def main():
    # camera_hands = Video_Read(0)
    # port = comm_platform.init_port()
    # comm_platform.Set_package_and_transmit('r', port)
    # while True:
    #     signal = input()
    #     hands_frame = camera_hands.Read_video_from_live_cam()
    #     cv2.imshow("Digital Image Processing", hands_frame)
    #     cv2.waitKey(20)
    #     comm_platform.Set_package_and_transmit(signal, port)
    pass


def set_background(img):
    screen.blit(img, (0, 0))
    screen.blit(img, (751, 0))
    screen.blit(img, (0, 751))
    screen.blit(img, (751, 751))
    title = get_font(150).render("Hands-ON", True, "#1e0b7d")
    title_rect = title.get_rect(center=(840, 100))
    screen.blit(title, title_rect)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Fonts/VIDEOPHREAK.ttf", size)


def calibrate():
    print("CALIBRATION NOT IMPLEMENTED YET")


def play():
    print('PLAY NOT IMPLEMENTED YET')


def detect_map():
    print('DETECT MAP NOT IMPLEMENTED YET')


def show_leader_board():
    print('LEADER BOARD NOT IMPLEMENTED YET')

def main_menu() -> None:
    while True:
        set_background(background)
        get_mouse_pos = pygame.mouse.get_pos()
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

        for button in [calib_button, detect_button, play_button, lead_button, quit_button]:
            button.changeColor(get_mouse_pos)
            button.update(screen)

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

        pygame.display.update()


if __name__ == '__main__':
    main_menu()
