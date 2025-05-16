import pygame, sys, cv2
from pygame.locals import *
import pygame_menu
from ultralytics import YOLO
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import datetime

# Khởi tạo pygame
pygame.init()
pygame.mixer.init()

# Cấu hình màn hình
WINDOWWIDTH, WINDOWHEIGHT = 1280, 720
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BG_COLOR = (175, 238, 238)
FPS = 60
fpsClock = pygame.time.Clock()

# Nhạc nền
pygame.mixer.music.load(r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\supershy-beat.mp3')
pygame.mixer.music.set_volume(1)

# Font
FONT_PATH = r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\font.ttf'
font = pygame.font.SysFont(None, 30)
# Load model YOLO và CNN
cnn_model = load_model(r"C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\food1_cnn_model.h5")
yolo_model = YOLO(r"C:\Users\PC\Documents\Zalo Received Files\project-5-at-2025-05-11-13-43-7b83d22c\runs\detect\train\weights\best.pt")

# Class và giá
class_names = ["Ca kho", "Canh bau", "Canh bi do", "Canh cai", "Canh chua", "Com",
               "Dau hu xao ca chua", "Ga chien", "Rau muong xao", "Thit kho",
               "Thit kho trung", "Trung chien"]

price_dict = {
    "Ca kho": 20000, "Canh bau": 15000, "Canh bi do": 15000, "Canh cai": 15000,
    "Canh chua": 15000, "Com": 5000, "Dau hu xao ca chua": 18000, "Ga chien": 25000,
    "Rau muong xao": 12000, "Thit kho": 25000, "Thit kho trung": 30000, "Trung chien": 10000
}

# Nhân vật chọn
selected_character = None

# Load icon exit
exit_img = pygame.image.load(r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\exit.png')
exit_img = pygame.transform.scale(exit_img, (40, 40))

character_image_dict = {
    'Guma': r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\guma.png',
    'Winter': r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\tao.png',
    'Quac': r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\mike.png',
    'Ipper': r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\noledavang.png'
}
selected_characters = []
def draw_exit_button():
    DISPLAYSURF.blit(exit_img, (WINDOWWIDTH - 50, 10))
    return pygame.Rect(WINDOWWIDTH - 50, 10, 40, 40)

def payment_menu(total_price):
    selected_payment = [None]

    def set_payment(value, payment_type):
        selected_payment[0] = payment_type

    menu = pygame_menu.Menu('Chọn phương thức thanh toán', WINDOWWIDTH, WINDOWHEIGHT, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.selector('Thanh toán :', [('Chuyển khoản', ''), ('Tiền mặt', 'Tiền mặt')], onchange=set_payment)
    menu.add.button('Xác nhận', pygame_menu.events.EXIT)
    menu.mainloop(DISPLAYSURF)

    return selected_payment[0] if selected_payment[0] else "Không chọn"


def detect_and_pay(selected_characters):
    cap = cv2.VideoCapture(0)
    total_price = 0
    cam_w, cam_h = 640, 480
    cam_surface = pygame.Surface((cam_w, cam_h))
    font_detect = pygame.font.Font(FONT_PATH, 40)

    char_imgs = []
    for char in selected_characters:
        if char in character_image_dict:
            img = pygame.image.load(character_image_dict[char])
            img = pygame.transform.scale(img, (150, 150))
            char_imgs.append(img)

    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.resize(frame, (640, 480))

        # YOLO detect
        results = yolo_model.predict(frame, conf=0.25)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()

        temp_detected_items = []
        temp_detected_names = set()

        if len(boxes) > 0:
            for i in range(len(boxes)):
                class_idx = int(classes[i])
                class_name = class_names[class_idx]

                if class_name not in temp_detected_names:
                    price = price_dict[class_name]
                    temp_detected_names.add(class_name)
                    temp_detected_items.append((class_name, price))

                    x1, y1, x2, y2 = map(int, boxes[i])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{class_name}-{price}VND', (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        else:
            print("⚠️ Không phát hiện món nào.")

        # Hiển thị khung camera lên Pygame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (cam_w, cam_h))
        pygame_frame = pygame.surfarray.make_surface(np.rot90(frame_rgb, 1))
        cam_surface.blit(pygame_frame, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
                elif event.key == K_c:
                    added_price = sum([item[1] for item in temp_detected_items])
                    total_price += added_price
                    print(f'✅ Cộng {added_price} vào tổng ({total_price})')

        DISPLAYSURF.fill(BG_COLOR)

        for idx, img in enumerate(char_imgs):
            DISPLAYSURF.blit(img, (50, 50 + idx * 160))

        cam_rect = cam_surface.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
        DISPLAYSURF.blit(cam_surface, cam_rect)

        text_surf = font_detect.render(f'Total: {total_price} VND', True, (255, 0, 0))
        DISPLAYSURF.blit(text_surf, (WINDOWWIDTH // 2 - text_surf.get_width() // 2, 20))

        pygame.display.update()
        fpsClock.tick(FPS)
    if total_price > 0:
        payment_type = payment_menu(total_price)
        bill_text = f'Bill\nCharacter: {", ".join(selected_characters)}\nPayment: {payment_type}\nTotal: {total_price} VND\n'
        filename = f'bill_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(bill_text)
        print(f'Đã lưu bill: {filename}')

    cap.release()
    cv2.destroyAllWindows()


def character_carousel_menu():
    characters = [
        (r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\guma.png', 'Guma'),   
        (r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\tao.png', 'Winter'),
        (r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\mike.png', 'Quac'),
        (r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\noledavang.png', 'Ipper'),
    ]
    total_characters = len(characters)
    current_index = 0

    heading_image = pygame.image.load(r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\heading.png')
    heading_image = pygame.transform.scale(heading_image, (600, 200))
    heading_img_rect = heading_image.get_rect(center=(WINDOWWIDTH // 2, 120))

    colors = {
        'Guma': (128,128,0),
        'Ipper': (128,128,0),
        'Winter': (128,128,0),
        'Quac': (128,128,0)
    }

    while True:
        DISPLAYSURF.fill(BG_COLOR)
        DISPLAYSURF.blit(heading_image, heading_img_rect)

        image = pygame.image.load(characters[current_index][0])
        image = pygame.transform.scale(image, (450, 450))
        image_rect = image.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
        DISPLAYSURF.blit(image, image_rect)

        font = pygame.font.Font(FONT_PATH, 60)
        name = characters[current_index][1]
        color = colors.get(name, (255, 255, 255))
        text_surface = font.render(name, True, color)
        text_rect = text_surface.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT - 100))
        DISPLAYSURF.blit(text_surface, text_rect)

        exit_button_rect = draw_exit_button()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    current_index = (current_index + 1) % total_characters
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    current_index = (current_index + 1) % total_characters
                elif event.key == K_LEFT:
                    current_index = (current_index - 1) % total_characters
                elif event.key == K_RETURN:
                    char_name = characters[current_index][1]
                    if char_name not in selected_characters:
                        selected_characters.append(char_name)
                        print(f"Đã chọn: {char_name}")
                elif event.key == K_s:  # Nhấn S để vào game
                    detect_and_pay(selected_characters)
                    return
                elif event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()
                    current_index = (current_index + 1) % total_characters

        pygame.display.update()
        fpsClock.tick(FPS)

def main_menu_manual_loop():
    pygame.mixer.music.play(-1)

    custom_theme = pygame_menu.themes.Theme(
        background_color=pygame_menu.baseimage.BaseImage(image_path=r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\bg.jpg'),
        widget_font=FONT_PATH,
        widget_font_size=60,
        widget_font_color=(255, 99, 71),
        selection_color=(128, 0, 0),
        title_font_size=30
    )

    menu = pygame_menu.Menu('Main Menu', WINDOWWIDTH, WINDOWHEIGHT, theme=custom_theme)
    menu.add.button('START', character_carousel_menu)
    menu.add.button('EXIT', pygame_menu.events.EXIT)

    heading_image = pygame.image.load(r'C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\code\heading2.png')
    heading_image = pygame.transform.scale(heading_image, (500, 150))
    heading_img_rect = heading_image.get_rect(center=(WINDOWWIDTH // 2, 150))

    while True:
        DISPLAYSURF.fill(BG_COLOR)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        menu.update(events)
        menu.draw(DISPLAYSURF)
        DISPLAYSURF.blit(heading_image, heading_img_rect)

        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    main_menu_manual_loop()

if __name__ == '__main__':
    main()
