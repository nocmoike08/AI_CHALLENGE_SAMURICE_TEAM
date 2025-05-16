import pygame, sys
from pygame.locals import *
import pygame_menu

pygame.init()
pygame.mixer.init()

# Nhạc nền
pygame.mixer.music.load(r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\supershy-beat.mp3')
pygame.mixer.music.set_volume(1)

# Fullscreen
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOWWIDTH, WINDOWHEIGHT = DISPLAYSURF.get_size()

# Màu nền
BG_COLOR = (175, 238, 238)

# Font
FONT_PATH = r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\font.ttf'

# FPS
FPS = 60
fpsClock = pygame.time.Clock()

# Load icon exit
exit_img = pygame.image.load(r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\exit.png')
exit_img = pygame.transform.scale(exit_img, (40, 40))

def draw_exit_button():
    DISPLAYSURF.blit(exit_img, (WINDOWWIDTH - 50, 10))
    return pygame.Rect(WINDOWWIDTH - 50, 10, 40, 40)

def gameStart():
    heading_image = pygame.image.load(r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\heading2.png')
    heading_image = pygame.transform.scale(heading_image, (600, 200))  # Resize nếu cần
    heading_img_rect = heading_image.get_rect(center=(WINDOWWIDTH // 2, 150))  # Hiển thị ở gần đầu

    while True:
        DISPLAYSURF.fill(BG_COLOR)
        DISPLAYSURF.blit(heading_image, heading_img_rect)
        exit_button_rect = draw_exit_button()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            if event.type == MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)

def character_carousel_menu():
    characters = [
        (r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\guma.png', 'Tram Do'),
        (r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\tao.png', 'Thoo'),
        (r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\mike.png', 'Moike'),
        (r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\noledavang.png', 'Puc'),
    ]
    total_characters = len(characters)
    current_index = 0

    while True:
        DISPLAYSURF.fill(BG_COLOR)

        # Load nhân vật
        image = pygame.image.load(characters[current_index][0])
        image = pygame.transform.scale(image, (400, 400))
        DISPLAYSURF.blit(image, (WINDOWWIDTH // 2 - 200, WINDOWHEIGHT // 2 - 150))

        # Tên nhân vật
        font = pygame.font.Font(FONT_PATH, 50)
        text_surface = font.render(characters[current_index][1], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT - 100))
        DISPLAYSURF.blit(text_surface, text_rect)

        exit_button_rect = draw_exit_button()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    current_index = (current_index + 1) % total_characters
                elif event.key == K_LEFT:
                    current_index = (current_index - 1) % total_characters
                elif event.key == K_RETURN:
                    gameStart()
                elif event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    current_index = (current_index + 1) % total_characters

        pygame.display.update()
        fpsClock.tick(FPS)

def main_menu():
    pygame.mixer.music.play(-1)

    custom_theme = pygame_menu.themes.Theme(
        background_color=pygame_menu.baseimage.BaseImage(image_path=r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\bg.jpg'),
        widget_font=r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\font.fon',
        widget_font_size=60,
        widget_font_color=(0, 0, 204),
        selection_color=(0, 204, 0),
        title_font_size=30
    )

    menu = pygame_menu.Menu('Main Menu', WINDOWWIDTH, WINDOWHEIGHT, theme=custom_theme)
    menu.add.button('START', character_carousel_menu)
    menu.add.button('EXIT', pygame_menu.events.EXIT)
    menu.mainloop(DISPLAYSURF)
    
def main():
    while True:
        main_menu()

if __name__ == '__main__':
    main()

def choose_character_menu():
    global selected_character
    menu = pygame_menu.Menu('Choose your character', WINDOWWIDTH, WINDOWHEIGHT, theme=main_menu)
    # Thêm nút vào menu
    for character_image, character_label, character_number in characters:
        menu.add.button(character_label, select_character, character_number)
        menu.add.generic_widget(pygame_menu.widgets.Image(image_path=character_image, angle=00, scale=(1.5, 1)))
    menu.add.button('Back', main_menu)
    menu.mainloop(SCREEN)


def select_character(character):
    global selected_character
    selected_character = f"Character{character}"
    start_game(selected_character)


def start_game(choose_character):
    if selected_character:
        start_game_logic(choose_character)


def start_game_logic(selected_character):
    if selected_character is not None:

        character_classes = {
            "Character1": rf"{folder}\jumpy_tut\assets\character1.png",
            "Character2": rf"{folder}\jumpy_tut\assets\character2.png",
            "Character3": rf"{folder}\jumpy_tut\assets\character3.png",
            "Character4": rf"{folder}\jumpy_tut\assets\character4.png",
            "Character5": rf"{folder}\jumpy_tut\assets\character5.png",
            "Character6": rf"{folder}\jumpy_tut\assets\character6.png",
        }
        character_image = character_classes.get(selected_character)
        # if character_image:
        #     print(selected_character)
        #     # Khởi tạo đối tượng người chơi với hình ảnh đã chọn
        #     player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, character_image)
        if character_image:
            # Khởi tạo đối tượng người chơi với hình ảnh đã chọn
            player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, character_image)
            run_game(game_over, bg_scroll, platform, score, high_score, fade_counter, player)
