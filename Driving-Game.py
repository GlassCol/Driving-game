import time
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
display = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Driving Simulator")

framerate = 60

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
yellow = (255, 255, 0)
dark_yellow = (200, 200, 0)
green = (45, 140, 90)

# Set up fonts
title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 36)

# Define Button class
class Button:
    def __init__(self, text, position, font, action):
        self.text = text
        self.position = position
        self.font = font
        self.action = action
        self.rect = pygame.Rect(position[0], position[1], 250, 50)
        self.corner_radius = 10

    def draw(self, display):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(display, dark_yellow, self.rect, border_radius=self.corner_radius)  # Fill the button with yellow color
            pygame.draw.rect(display, dark_yellow, self.rect, width=2, border_radius=self.corner_radius)  # Draw the button outline
        else:
            pygame.draw.rect(display, yellow, self.rect, border_radius=self.corner_radius)  # Fill the button with yellow color
            pygame.draw.rect(display, yellow, self.rect, width=2, border_radius=self.corner_radius)  # Draw the button outline

        text_surface = self.font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        display.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


# Define action functions for buttons
def start_game():
    initialize(display)
    game_loop(display)
    
def change_framerate():
    change_framerate()
    
def quit_game():
    pygame.quit()
    sys.exit()

# Calculate center positions based on display size
center_x_percent = 0.5  # Adjust this value to change the horizontal centering position (0.0 - leftmost, 1.0 - rightmost)
center_y_percent = 0.5  # Adjust this value to change the vertical centering position (0.0 - topmost, 1.0 - bottommost)
center_x = int(display.get_width() * center_x_percent)
center_y = int(display.get_height() * center_y_percent)



# Create buttons
start_button = Button("Start", (center_x - 125, center_y - 100), button_font, start_game)
framerate_button = Button("Change Framerate", (center_x - 125, center_y - 40), button_font, change_framerate)
quit_button = Button("Quit", (center_x - 125, center_y + 20), button_font, quit_game)

def draw_buttons():
    global start_button, speed_button,framerate_button, quit_button
    # Calculate center positions based on display size
    center_x_percent = 0.5  # Adjust this value to change the horizontal centering position (0.0 - leftmost, 1.0 - rightmost)
    center_y_percent = 0.5  # Adjust this value to change the vertical centering position (0.0 - topmost, 1.0 - bottommost)
    center_x = int(display.get_width() * center_x_percent)
    center_y = int(display.get_height() * center_y_percent)

    # ReCreate buttons
    start_button = Button("Start", (center_x - 125, center_y - 100), button_font, start_game)
    framerate_button = Button("Change Framerate", (center_x - 125, center_y - 40), button_font, change_framerate)
    quit_button = Button("Quit", (center_x - 125, center_y + 20), button_font, quit_game)

    # Draw buttons
    start_button.draw(display)
    framerate_button.draw(display)
    quit_button.draw(display)

road_y = 0
road_width = 300

# Load car image
car = pygame.image.load("car.png")
car_aspect_ratio = car.get_height() / car.get_width()
car_scaling_factor = 0.6  # Adjust this value to scale down the car height
# Limit car size based on road width
car_width = min(road_width // 3, car.get_width() * car_scaling_factor)
car_height = car_width * car_aspect_ratio
# Scale the car image to fit within the maximum width and height
car_scaled = pygame.transform.scale(car, (car_width, car_height))

# Obstacles
star = pygame.image.load("star.png")
star_scaling_factor = 0.25  # Adjust this value to scale down the car height
star_scaled = pygame.transform.scale(star, (int(star.get_width() * star_scaling_factor), int(star.get_height() * star_scaling_factor)))
angle = 0

# Set up enemy variables
enemy_width = star_scaled.get_width()
enemy_height = star_scaled.get_height()

clock = pygame.time.Clock()

# Draw the speedometer
def draw_speedometer(display, displayed_speed):
    speedometer_width = 40
    speedometer_height = 200
    label_font_size = 20

    # Calculate the x-coordinate of the speedometer
    speedometer_x = display.get_width() * 3 / 4 - speedometer_width / 2

    # Calculate the y-coordinate of the speedometer
    speedometer_y = display.get_height() / 2 - speedometer_height / 2

    # Calculate the percentage of the car's speed relative to its maximum speed
    max_speed = 160  # Maximum speed in mph

    # Calculate the speed percentage to adjust the speedometer bar height
    speed_percentage = min(displayed_speed / max_speed, 1.0)

    # Calculate the height of the speedometer bar based on the speed percentage
    speedometer_bar_height = int(speedometer_height * speed_percentage)

    # Draw the background of the speedometer
    pygame.draw.rect(display, white, (speedometer_x, speedometer_y, speedometer_width, speedometer_height))

    # Draw the speedometer bar
    pygame.draw.rect(
        display,
        black,
        (speedometer_x, speedometer_y + speedometer_height - speedometer_bar_height, speedometer_width, speedometer_bar_height),
    )

    # Draw the tick marks and labels
    tick_length = 8
    label_font = pygame.font.Font(None, label_font_size)

    for i in range(10):
        # Calculate the y-coordinate of the tick mark
        tick_y = speedometer_y + speedometer_height - (i / 10) * speedometer_height

        # Draw the tick mark
        pygame.draw.line(display, black, (speedometer_x, tick_y), (speedometer_x + tick_length, tick_y))

        # Calculate the value of the speed label
        label_value = i * 20

        # Draw the speed label
        label_text = label_font.render(str(label_value), True, black)
        label_text_height = label_text.get_height()
        display.blit(label_text, (speedometer_x - 5 - label_text.get_width(), tick_y - label_text_height // 2))

    # Draw the current speed label
    current_speed_label = label_font.render(str(int(displayed_speed)) + " MPH", True, black)
    display.blit(current_speed_label, (speedometer_x + speedometer_width + 5, speedometer_y + speedometer_height - current_speed_label.get_height()))

    # Draw the dash at the top of the speedometer
    dash_width = 10
    dash_height = 2
    dash_x = speedometer_x + speedometer_width / 2 - dash_width / 2
    dash_y = speedometer_y + speedometer_height - speedometer_bar_height - dash_height
    pygame.draw.rect(display, black, (dash_x, dash_y, dash_width, dash_height))

# Generate initial enemy position
def generate_enemy() -> tuple[int, int]:
    enemy_x = random.randint(road_x, road_x + road_width - enemy_width)
    enemy_y = -enemy_height * 2
    return enemy_x, enemy_y

def initialize(display) -> None:
    global car_x, car_y, enemy_x, enemy_y, enemy_speed, road_x, road_y, road_height, score
    enemy_speed = 4
    car_x = display.get_width() // 2 - car_width // 2
    car_y = display.get_height() - car_height - 10
    road_x = display.get_width() // 2 - road_width // 2
    road_height = display.get_height()
    enemy_x, enemy_y = generate_enemy()
    score = 0

def show_main_menu(display) -> None:
    global car_speed, enemy_x, enemy_y, road_height, road_width, road_x, road_y, car_scaled, car_x, car_y, car_width, car_height
    center_x = display.get_width() // 2
    center_y = display.get_height() // 2

    car_speed = 3
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                start_button.handle_event(event)
                framerate_button.handle_event(event)
                quit_button.handle_event(event)


        display.fill(gray)

        # Calculate center positions based on display size
        center_x = display.get_width() // 2
        center_y = display.get_height() // 2

        # Define font sizes
        title_font_size = display.get_height() // 10
        menu_font_size = display.get_height() // 20

        # Set up fonts
        title_font = pygame.font.Font("fonts/Roboto-Bold.ttf", title_font_size)
        menu_font = pygame.font.Font("fonts/Roboto-Regular.ttf", menu_font_size)

        # Draw title
        title_text = title_font.render("Driving Simulator", True, black)
        title_text_rect = title_text.get_rect(center=(center_x, 100))
        display.blit(title_text, title_text_rect)

        draw_buttons()

        # Draw high score
        leaderboard = load_leaderboard()
        highscore = max(leaderboard) if leaderboard else 0
        highscore_text = menu_font.render(f"High Score: {str(highscore)}", True, black)
        highscore_text_rect = highscore_text.get_rect(center=(center_x, center_y + menu_font_size * 8))
        display.blit(highscore_text, highscore_text_rect)

        pygame.display.update()


def change_framerate() -> None:
    global framerate
    if framerate == 30:
        framerate = 60
    elif framerate == 60:
        framerate = 90
    elif framerate == 90:
        framerate = 120
    elif framerate == 120:
        framerate = 144
    elif framerate == 144:
        framerate = 30
    print(framerate)

def draw_entity(display, image, rect):
    display.blit(image, rect)

def rotate(image, x, y, angle) -> tuple[pygame.Surface, pygame.Rect]:
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    rect = pygame.Rect(x, y, image.get_width(), image.get_height())
    # Get a new rect with the center of the old rect.
    return new_image, new_image.get_rect(center=rect.center)

def check_collision() -> bool:
    if (car_x < enemy_x + enemy_width and car_x + car_width > enemy_x and
            car_y < enemy_y + enemy_height and car_y + car_height > enemy_y):
        return True
    return False

def update_score(display, score) -> None:
    score_text = title_font.render("Score: " + str(score), True, black)
    display.blit(score_text, (10, 10))

def game_over(display) -> None:
    global car_speed, score
    car_speed = 3
    leaderboard = load_leaderboard()
    leaderboard.append(score)
    leaderboard.sort(reverse=True)
    leaderboard = leaderboard[:5]  # Keep only the top 5 scores
    save_leaderboard(leaderboard)
    score = 0
    initialize(display)
    show_main_menu(display)

def load_leaderboard() -> list[int]:
    try:
        with open("leaderboard.txt", "r") as file:
            leaderboard = [int(line.strip()) for line in file]
    except FileNotFoundError:
        leaderboard = []
    return leaderboard

def save_leaderboard(leaderboard) -> None:
    with open("leaderboard.txt", "w") as file:
        for score in leaderboard:
            file.write(str(score) + "\n")

def display_leaderboard(display) -> None:
    leaderboard = load_leaderboard()
    display.fill(white)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Leaderboard", True, black)
    display.blit(title_text, (display.get_width() // 2 - title_text.get_width() // 2, 50))

    font = pygame.font.Font(None, 24)
    for i, score in enumerate(leaderboard):
        score_text = font.render(str(i+1) + ". " + str(score), True, black)
        display.blit(score_text, (display.get_width() // 2 - score_text.get_width() // 2, 100 + i*30))

    pygame.display.update()

def game_loop(display) -> None:
    global car_x, car_y, car_speed, enemy_x, enemy_y, enemy_speed, road_x, road_y, road_height, car_width, car_height, car, angle, score
    score = 0
    displayed_speed = 5
    # Dashed stripe variables
    stripe_width = 10
    stripe_height = 40
    stripe_spacing = 80
    stripe_y = 0
    last_time = time.time()

    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                initialize(display)  # Recreate the buttons when the display is resized
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_main_menu(display)
            elif event.type == pygame.VIDEORESIZE:
                display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                road_x = display.get_width() // 2 - road_width // 2
                road_height = display.get_height()

        # Handle car movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x -= dt * car_speed
        if keys[pygame.K_RIGHT]:
            car_x += dt * car_speed

        # Check collision
        if check_collision():
            game_over(display)

        # Update enemy position
        enemy_y += dt * enemy_speed

        # Update stripe position
        stripe_y += dt * (enemy_speed - 2)  # Move the dashed line downwards

        # Reset stripe position once it reaches the bottom of the display
        if stripe_y > stripe_spacing:
            stripe_y = 0

        stripe_offset = stripe_y

        # Calculate road_x based on screen width
        road_x = display.get_width() // 2 - road_width // 2

        # Calculate road_y and road_height based on screen height
        road_height = display.get_height()

        # Limit car_x within the road
        car_x = max(road_x, min(car_x, road_x + road_width - car_width))
        car_y = display.get_height() - car_height - 10

        # Spawn a new enemy if the previous one has moved off the screen
        if enemy_y > display.get_height():
            enemy_x_min = road_x
            enemy_x_max = road_x + road_width - enemy_width
            enemy_x = random.randint(enemy_x_min, enemy_x_max)
            enemy_y = -enemy_height
            enemy_speed += .5
            car_speed += .3
            displayed_speed = (displayed_speed * 1.05) + 1
            score += 1
 
        # Update the display
        display.fill(green)

        # Draw the road
        pygame.draw.rect(display, gray, (road_x, road_y, road_width, road_height))

        # Draw the dashed stripe
        while stripe_offset < road_height:
            pygame.draw.rect(display, yellow,
                            (road_x + road_width // 2 - stripe_width // 2, road_y + stripe_offset,
                            stripe_width, stripe_height))
            stripe_offset += stripe_spacing

        # Draw the car
        draw_entity(display, car_scaled, pygame.Rect(car_x, car_y, car_width, car_height))

        # Draw the enemy
        draw_entity(display, *rotate(star_scaled, enemy_x, enemy_y, angle))
        angle += 5 * dt

        # Update and display score
        update_score(display, score)

        # Draw the speedometer
        draw_speedometer(display, displayed_speed)

        pygame.display.update()
        clock.tick(framerate)

# Start the game
show_main_menu(display)