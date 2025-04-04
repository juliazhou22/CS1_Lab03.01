'''Jag ville bara ha en stol!!'''
__author__ = "Julia Zhou"
__version__ = "4/3/2025"

'''Flint Sessions:'''
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/5da931e7-652f-4d30-90ff-7d49e46fd9bd
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/8d1c6d8f-c233-4437-8684-c1499432ad96
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/86d743a7-fcb8-496e-b381-ac9e8bcd0da5
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/a68ad478-fd4a-448f-b480-3e2566b81948

import pygame
import random
from items import *
from employees import *
from high_scores import *
from score_display import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
IKEA_BLUE = (12,110,183)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)


class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


import random

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls """

    def __init__(self, x, y):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0

    def reset_speed(self):
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def move(self, walls):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Room(object):
    """ Base class for all rooms. """

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        #self.transition_areas = []
        self.employees = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.respawn_timer = 0  # Timer for respawning items
        self.respawn_delay = 0  # Random delay before respawning
        self.needs_respawn = False  # Flag to indicate items need to respawn
        self.last_item_types = set()  # Keep track of previous item types

    def spawn_items(self, num_items = 5):
        if self.items.sprites() == []:
            self.last_item_types = set()

        spawned = 0

        # Try to spawn the requested number of items
        for _ in range(num_items):
            # Generate a valid position
            x, y = Item.generate_valid_position(self, self.items)

            if x is not None and y is not None:
                # Choose an item type that wasn't recently used if possible
                available_types = list(range(len(Item.ITEM_TYPES)))
                if len(self.last_item_types) < len(available_types):
                    # Filter out recently used types
                    new_types = [t for t in available_types if t not in self.last_item_types]
                    item_type = random.choice(new_types)
                else:
                    # If we've used all types, just pick randomly
                    item_type = random.randint(0, len(Item.ITEM_TYPES) - 1)

                # Create the item and add it to the group
                item = Item(x, y, item_type)
                self.items.add(item)

                # Remember this type was used
                self.last_item_types.add(item_type)
                # Keep the set from growing too large
                if len(self.last_item_types) > 10:
                    self.last_item_types.pop()

                spawned += 1

        return spawned

    def update(self):
        """Update room state, handle item respawning"""
        # If items need to respawn and the timer is active
        if self.needs_respawn:
            self.respawn_timer += 1

            # Check if it's time to respawn
            if self.respawn_timer >= self.respawn_delay:
                # Respawn items - Fix the Room2 check
                if isinstance(self, Room1):
                    num_to_spawn = 1
                elif isinstance(self, Room2):
                    num_to_spawn = 1
                elif isinstance(self, Room3):
                    num_to_spawn = 1
                else:
                    num_to_spawn = 1

                # Add debug print to verify the room type
                print(f"Attempting to spawn {num_to_spawn} items in {self.__class__.__name__}")

                # Call spawn_items and store the result
                spawned = self.spawn_items(num_to_spawn)

                # Reset timer and flag
                self.respawn_timer = 0
                self.needs_respawn = False
                print(f"Items respawned in {self.__class__.__name__}: {spawned} items added")

    def trigger_respawn(self):
        """Start the respawn timer with a random delay"""
        if not self.needs_respawn:
            # Set a random delay between 5-15 seconds (at 60 FPS)
            self.respawn_delay = random.randint(200, 300)  # 5-15 seconds at 60 FPS
            self.respawn_timer = 0
            self.needs_respawn = True
            print(f"Items will respawn in {self.respawn_delay / 60:.1f} seconds in {self.__class__.__name__}")


class Room1(Room):
    """This creates all the walls in room 1"""

    def __init__(self):
        super().__init__()
        # Make the walls. (x_pos, y_pos, width, height)

        # This is a list of walls. Each is in the form [x, y, width, height]
        walls = [[0, 0, 10, 750, WHITE], #left side
                 [790, 0, 10, 600, WHITE], #right side
                 [10, 0, 790, 10, WHITE], #top
                 [10, 590, 40, 10, WHITE], #bottom piece
                 [50, 590, 100, 10, IKEA_BLUE], #blocking entrance
                 [160, 590, 640, 10, WHITE], #bottom side
                 [205, 480, 10, 120, WHITE], #near entrance
                 [470, 400, 10, 200, WHITE], #next to restaurant
                 [400, 400, 70, 10, WHITE], #corner
                 [150, 280, 180, 10, WHITE], #divided shortcut
                 [390, 280, 340, 10, WHITE],
                 [470, 290, 10, 20, WHITE], #wardrobe
                 [250, 290, 10, 210, WHITE], #right of near entrance
                 [260, 450, 90, 10, WHITE], #corner
                 [620, 290, 10, 210, WHITE], #left of bedroom
                 [540, 450, 90, 10, WHITE], #corner
                 [525, 190, 10, 90, WHITE], #shortcut 2
                 [525, 80, 10, 65, WHITE],
                 [480, 80, 175, 10, WHITE],
                 [670, 165, 180, 10, WHITE],
                 [215, 140, 10, 140, WHITE], #next to living room
                 [200, 95, 70, 10, WHITE],
                 [350, 10, 10, 180, WHITE],
                 [300, 190, 130, 10, WHITE]

                 ]
        self.transition_areas = [[300, 550, 30, 30, 1, 750, 550]]

        employee1 = Employee(200, 200, image_name = "worker1.png")
        employee2 = Employee(500, 300, image_name = "worker2.png")
        self.employees.add(employee1)
        self.employees.add(employee2)

        self.spawn_items(6)

        # Loop through the list. Create the wall, add it to the list
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Room2(Room):
    """This creates all the walls in room 2"""

    def __init__(self):
        super().__init__()

        walls = [[0, 0, 10, 750, WHITE], #left side
                 [790, 0, 10, 40, WHITE], #right side
                 [790, 100, 10, 500, WHITE],
                 [790, 40, 10, 60, IKEA_BLUE],
                 [10, 0, 790, 10, WHITE], #top
                 [10, 590, 790, 10, WHITE], #bottom
                 [10, 140, 60, 10, WHITE],
                 [130, 140, 180, 10, WHITE],
                 [360, 140, 450, 10, WHITE],
                 [10, 270, 60, 10, WHITE],
                 [10, 400, 60, 10, WHITE],
                 [250, 10, 10, 30, WHITE],
                 [250, 100, 10, 40, WHITE],
                 [400, 10, 10, 30, WHITE],
                 [400, 100, 10, 40, WHITE],
                 [360, 150, 10, 50, WHITE],
                 [360, 250, 10, 130, WHITE],
                 [360, 310, 260, 10, WHITE],
                 [730, 310, 60, 10, WHITE],
                 [520, 260, 10, 60, WHITE],
                 [550, 320, 10, 150, WHITE],
                 [510, 460, 40, 10, WHITE],
                 [500, 460, 10, 150, WHITE],#go back here
                 [200, 150, 10, 210, WHITE],
                 [210, 350, 40, 10, WHITE],
                 [170, 400, 30, 10, WHITE],
                 [200, 400, 10, 70, WHITE],
                 [200, 460, 210, 10, WHITE],
                 [295, 460, 10, 40, WHITE],
                 [295, 560, 10, 40, WHITE]
                 ]

        self.transition_areas = [
            [750, 550, 30, 30, 0, 350, 550],  # Spawn player away from transitions in Room1
            [790, 40, 10, 60, 2, 50, 300]  # Transition to Room3
        ]

        # This flag will be checked in the main function
        self.initial_setup = True

        # Add employees only during initial setup
        if self.initial_setup:
            employee1 = Employee(300, 300, image_name="worker1.png")
            employee2 = Employee(400, 400, image_name="worker2.png")
            employee3 = Employee(500, 500, image_name="worker3.png")
            '''self.employees.add(employee1)
            self.employees.add(employee2)
            self.employees.add(employee3)'''

        self.spawn_items(5)

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

class Room3(Room):
#this creates the walls in room 3
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 10, 750, WHITE],  # left side
                 [790, 0, 10, 600, WHITE],  # right side
                 [10, 0, 790, 10, WHITE],  # top
                 [10, 590, 790, 10, WHITE],  # bottom

                 [100, 100, 10, 200, WHITE],  # Vertical shelf 1
                 [100, 100, 200, 10, WHITE],  # Horizontal shelf 1
                 [300, 100, 10, 300, WHITE],  # Vertical shelf 2
                 [300, 400, 200, 10, WHITE],  # Horizontal shelf 2
                 [500, 200, 10, 200, WHITE],  # Vertical shelf 3
                 [500, 200, 200, 10, WHITE],  # Horizontal shelf 3
                 [200, 300, 100, 10, WHITE],  # Small shelf 1
                 [400, 150, 10, 150, WHITE],  # Small shelf 2
                 [600, 400, 10, 100, WHITE],  # Small shelf 3
                 [100, 450, 100, 10, WHITE],  # Small shelf 4
                 [700, 100, 10, 300, WHITE],  # Long vertical shelf
                 [400, 500, 300, 10, WHITE],  # Long horizontal shelf
                ]

        self.transition_areas = [
            [0, 250, 10, 100, 1, 700, 300]  # Spawn player away from transitions in Room2
        ]

        # Add employees (more challenging in the warehouse)
        employee1 = Employee(200, 200, image_name="worker1.png")
        employee2 = Employee(600, 300, image_name="worker3.png")
        employee3 = Employee(400, 450, image_name="worker4.png")
        employee4 = Employee(150, 500, image_name="cook.png")
        self.employees.add(employee1)
        self.employees.add(employee2)
        self.employees.add(employee3)
        self.employees.add(employee4)

        # Make warehouse employees slightly faster
        for emp in [employee1, employee2, employee3, employee4]:
            emp.speed = 2.5  # Slightly faster than default
            self.employees.add(emp)

        # Spawn more items in the warehouse (it's where the products are stored!)
        self.spawn_items(8)

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

def show_level_complete(screen, level, score_bonus):
    """Display level completion message"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Level complete text
    font_large = pygame.font.SysFont('Arial', 64)
    level_text = font_large.render(f'Level {level} Complete!', True, (255, 255, 255))
    level_rect = level_text.get_rect(center=(400, 200))
    screen.blit(level_text, level_rect)

    # Bonus points text
    font_medium = pygame.font.SysFont('Arial', 36)
    bonus_text = font_medium.render(f'Bonus: +{score_bonus} points', True, (255, 215, 0))
    bonus_rect = bonus_text.get_rect(center=(400, 280))
    screen.blit(bonus_text, bonus_rect)

    # Next level text
    font_small = pygame.font.SysFont('Arial', 24)
    next_text = font_small.render('Get ready for the next level!', True, (255, 255, 255))
    next_rect = next_text.get_rect(center=(400, 350))
    screen.blit(next_text, next_rect)

    # Update display and pause
    pygame.display.flip()
    pygame.time.delay(1500)  # Show for 3 seconds

def main():
    """ Main Program """
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    #loading in sound files
    sounds = {
        'collect':
            pygame.mixer.Sound('sounds/collect.wav'),
        'level_up':
            pygame.mixer.Sound('sounds/level-up.wav')
    }

    sounds['collect'].set_volume(0.5)

    # Create the screen (only once)
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Jag ville bara ha en stol!')

    high_score_manager = HighScoreManager()
    score_display = HighScoreScreen(screen, high_score_manager)

    game_state = "playing"

    # Create game objects
    player = Player(95, 570)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    # Create rooms
    rooms = []
    room = Room1()
    rooms.append(room)
    room = Room2()
    rooms.append(room)
    room = Room3()
    rooms.append(room)

    for room in rooms:
        if hasattr(room, 'initial_setup'):
            room.initial_setup = False

    current_room_no = 0
    current_room = rooms[current_room_no]
    previous_room_no = current_room_no  # Track previous room for respawn triggering

    current_level = 1
    level_complete = False
    items_collected_this_level = 0
    items_needed_for_level = 5
    level_transition_in_progress = False

    transition_cooldown = 0
    score_bonus = current_level * 20

    # Game state variables
    game_over = False
    collected_items = []
    score = 0
    level_start_scores = [0]
    last_level = 1
    font = pygame.font.SysFont('Arial', 18)

    # Clock for controlling frame rate
    clock = pygame.time.Clock()

    # Main game loop
    done = False
    while not done:
        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Handle key presses if game is not over
            if game_state == "playing":
                if not game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            player.changespeed(-5, 0)
                        if event.key == pygame.K_RIGHT:
                            player.changespeed(5, 0)
                        if event.key == pygame.K_UP:
                            player.changespeed(0, -5)
                        if event.key == pygame.K_DOWN:
                            player.changespeed(0, 5)
                        if event.key == pygame.K_SPACE:
                            # Cycle through rooms
                            current_room_no = (current_room_no + 1) % len(rooms)
                            current_room = rooms[current_room_no]

                            # Reset player position when switching rooms
                            if current_room_no == 0:
                                player.rect.x = 95
                                player.rect.y = 570
                            elif current_room_no == 1:
                                player.rect.x = 750
                                player.rect.y = 550

                    '''if transition_cooldown <= 0:  # Only check for transitions if cooldown is over
                        for area in current_room.transition_areas:
                            area_rect = pygame.Rect(area[0], area[1], area[2], area[3])
                            if player.rect.colliderect(area_rect):
                                print(f"Transitioning to room {area[4]}")

                                # Trigger respawn in the room we're leaving
                                rooms[current_room_no].trigger_respawn()

                                # Change rooms
                                previous_room_no = current_room_no
                                current_room_no = area[4]
                                current_room = rooms[current_room_no]

                                # Use specified spawn coordinates if available
                                if len(area) >= 7:
                                    player.rect.x = area[5]
                                    player.rect.y = area[6]
                                else:
                                    # Default spawn position
                                    player.rect.x = 50
                                    player.rect.y = 50

                                # Set a cooldown to prevent immediate transitions back
                                transition_cooldown = 30  # Half a second at 60 FPS

                                # Break out of the loop after transitioning
                                break
                    else:
                        # Decrease cooldown timer
                        transition_cooldown -= 1
'''
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            player.changespeed(5, 0)
                        if event.key == pygame.K_RIGHT:
                            player.changespeed(-5, 0)
                        if event.key == pygame.K_UP:
                            player.changespeed(0, 5)
                        if event.key == pygame.K_DOWN:
                            player.changespeed(0, -5)

                    def reset_rooms_for_new_level(rooms, level):
                        """Reset rooms with increased difficulty for a new level"""
                        for room in rooms:
                            # Clear existing items and employees
                            room.items.empty()
                            room.employees.empty()

                            # Add employees based on level and room type
                            if isinstance(room, Room1):
                                num_employees = 2
                            elif isinstance(room, Room2):
                                num_employees = 3
                            elif isinstance(room, Room3):
                                num_employees = 4
                            else:
                                num_employees = 2

                            # Employee image names
                            employee_images = ["worker1.png", "worker2.png", "worker3.png", "worker4.png", "cook.png"]

                            # Keep track of employee positions to ensure they're not too close to each other
                            employee_positions = []

                            for i in range(num_employees):
                                # Generate positions away from player spawn points and other employees
                                valid_position = False
                                attempts = 0

                                while not valid_position and attempts < 100:  # Increased attempts
                                    attempts += 1
                                    x = random.randint(100, 700)
                                    y = random.randint(100, 500)

                                    # Check distance from player spawn points (increased safe distance)
                                    too_close_to_spawn = False

                                    # Room 1 spawn point
                                    if abs(x - 95) < 150 and abs(y - 570) < 150:  # Increased from 100
                                        too_close_to_spawn = True

                                    # Room 2 spawn point (now at 700, 550 after our changes)
                                    if abs(x - 700) < 150 and abs(y - 550) < 150:  # Increased from 100
                                        too_close_to_spawn = True

                                    # Room 3 spawn point
                                    if abs(x - 50) < 150 and abs(y - 300) < 150:  # Increased from 100
                                        too_close_to_spawn = True

                                    # Check distance from other employees
                                    too_close_to_other_employee = False
                                    for pos in employee_positions:
                                        if abs(x - pos[0]) < 100 and abs(
                                                y - pos[1]) < 100:  # Ensure employees are spread out
                                            too_close_to_other_employee = True
                                            break

                                    if not too_close_to_spawn and not too_close_to_other_employee:
                                        valid_position = True
                                        employee_positions.append((x, y))  # Remember this position

                                # If we couldn't find a valid position, use a default that's different for each employee
                                if not valid_position:
                                    x = 200 + (i * 100) % 400
                                    y = 200 + (i * 100) % 300
                                    print(
                                        f"Using fallback position for employee in {room.__class__.__name__}: ({x}, {y})")
                                    employee_positions.append((x, y))

                                # Create employee with increasing difficulty
                                image_name = employee_images[i % len(employee_images)]
                                employee = Employee(x, y, image_name=image_name)

                                # Scale difficulty based on level
                                employee.speed = min(2 + (level * 0.15), 3.5)  # Cap speed at 3.5
                                employee.detection_radius = min(150 + (level * 10), 250)  # Cap detection at 250

                                room.employees.add(employee)
                                print(f"Added employee at ({x}, {y}) in {room.__class__.__name__}")

                            # Spawn items with increasing count based on level and room type
                            if isinstance(room, Room1):
                                base_items = 6
                            elif isinstance(room, Room2):
                                base_items = 8
                            elif isinstance(room, Room3):
                                base_items = 8
                            else:
                                base_items = 5

                            # Add more items as levels increase (but cap it)
                            num_items = min(base_items + (level // 2), 12)
                            spawned = room.spawn_items(num_items)
                            print(f"Spawned {spawned} items in {room.__class__.__name__}")



            elif game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset the game
                        game_state = "playing"
                        game_over = False
                        player.reset_speed()

                        # Determine which room to restart in based on the last level
                        if last_level == 1:
                            current_room_no = 0  # Room 1
                            player.rect.x = 95
                            player.rect.y = 570
                        elif last_level == 2:
                            current_room_no = 1  # Room 2
                            player.rect.x = 700  # Use the fixed position we discussed earlier
                            player.rect.y = 550
                        else:  # Level 3 or higher
                            current_room_no = 2  # Room 3
                            player.rect.x = 50
                            player.rect.y = 300

                        current_room = rooms[current_room_no]
                        current_level = last_level  # Restore the level

                        # Safely restore the score from the beginning of the current level
                        previous_level_index = current_level - 1
                        if 0 <= previous_level_index < len(level_start_scores):
                            score = level_start_scores[previous_level_index]
                            print(f"Restored score {score} from level {previous_level_index + 1}")
                        else:
                            score = 0  # Fallback if we don't have a stored score
                            print(f"No stored score for level {previous_level_index + 1}, using 0")

                        # Reset other game state
                        collected_items = []
                        items_collected_this_level = 0

                        # Reset player speed to zero
                        player.change_x = 0
                        player.change_y = 0

                        # Respawn items in all rooms
                        for room in rooms:
                            if hasattr(room, 'items'):
                                room.items.empty()
                                room.spawn_items(8 if isinstance(room, Room1) else 5)

                    elif event.key == pygame.K_q:
                        done = True

                    elif event.key == pygame.K_h:
                        game_state = "high_scores"



            elif game_state == "high_scores":
                if score_display.show_high_scores():
                    game_state = "game_over"

                else:
                    done = True


        # --- Game Logic ---
        if not game_over:
            # Move player
            player.move(current_room.wall_list)

            # Update all rooms (for respawning)
            for room in rooms:
                room.update()

            '''# Check for room transitions by walking into transition areas
            for area in current_room.transition_areas:
                area_rect = pygame.Rect(area[0], area[1], area[2], area[3])
                if player.rect.colliderect(area_rect):
                    # Only allow transitions if not in a level transition
                    if not level_transition_in_progress:
                        print(f"Transitioning to room {area[4]}")

                    # Trigger respawn in the room we're leaving
                    rooms[current_room_no].trigger_respawn()

                    # Change rooms
                    previous_room_no = current_room_no
                    current_room_no = area[4]
                    current_room = rooms[current_room_no]

                    # Use specified spawn coordinates if available
                    if len(area) >= 7:
                        player.rect.x = area[5]
                        player.rect.y = area[6]
                    else:
                        # Default spawn position
                        player.rect.x = 50
                        player.rect.y = 50
                    # Break out of the loop after transitioning to avoid multiple transitions
                    break'''

            # Check for item collisions
            if hasattr(current_room, 'items'):
                item_collisions = pygame.sprite.spritecollide(player, current_room.items, True)
                for item in item_collisions:
                    # Add item to collected list
                    collected_items.append(item.name)
                    # Increase score
                    score += 10
                    print(f"Collected {item.name}! Score: {score}")

                    sounds['collect'].play()

                    # Track items collected for level progression
                    items_collected_this_level += 1

                    rooms[current_room_no].trigger_respawn()

                    # When level is complete
                    if items_collected_this_level >= items_needed_for_level and not level_complete:
                        level_transition_in_progress = True
                        print(f"Level complete triggered!")
                        print(f"Current Level Before: {current_level}")

                        level_complete = True
                        score_bonus = current_level * 20  # Bonus points for completing level
                        score += score_bonus

                        sounds['level_up'].play()

                        # Store the current score as the starting score for the next level
                        # Use append() to safely add to the list
                        if current_level >= len(level_start_scores):
                            level_start_scores.append(score)  # Add for the next level
                        else:
                            level_start_scores[current_level] = score  # Update existing entry

                        print(f"Stored score {score} for level {current_level + 1}")

                        while len(level_start_scores) <= current_level:
                            level_start_scores[current_level] = score

                        # Pause the game and show level complete screen
                        level_complete_surface = pygame.Surface((800, 600))
                        level_complete_surface.fill(IKEA_BLUE)
                        screen.blit(level_complete_surface, (0, 0))
                        pygame.display.flip()

                        # Show level completion message
                        show_level_complete(screen, current_level, score_bonus)

                        # Advance to next level
                        current_level += 1
                        print(f"Current Level After: {current_level}")

                        # Increase items needed for next level
                        items_needed_for_level += 5

                        # Reset items collected counter
                        items_collected_this_level = 0

                        print(f"Attempting to switch to Room 2")
                        print(f"Rooms available: {len(rooms)}")

                        print("rooms:",rooms)
                        print("current level:",current_level)

                        # Reset rooms for new level
                        reset_rooms_for_new_level(rooms, current_level)


                        # EXPLICITLY set room and player position for level 2
                        if current_level == 2:
                            print("Trying to set Room 2")
                            current_room_no = 1  # Room 2
                            current_room = rooms[current_room_no]
                            player.rect.x = 700  # Spawn point for Room 2
                            player.rect.y = 550
                            print(f"Room set to: {current_room}")

                        # EXPLICITLY set room and player position for level 3 and beyond
                        elif current_level >= 3:
                            print("Trying to set Room 3")
                            current_room_no = 2  # Room 3
                            current_room = rooms[current_room_no]
                            player.rect.x = 50  # Spawn point for Room 3
                            player.rect.y = 300
                            print(f"Room set to: {current_room}")

                        # Reset key states and movement
                        pygame.event.clear()
                        keys = pygame.key.get_pressed()
                        player.reset_speed()
                        player.change_x = 0
                        player.change_y = 0
                        keys_to_reset = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
                        for key in keys_to_reset:
                            pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': key}))

                        # Reset level complete flag
                        level_complete = False
                        level_transition_in_progress = False

                        print(
                            f"After transition: level_transition_in_progress={level_transition_in_progress}, current_room_no={current_room_no}")

            # Update employees if they exist
            if hasattr(current_room, 'employees'):
                for employee in current_room.employees:
                    employee.update(player, current_room.wall_list)

                # Check for collisions with employees
                employee_collisions = pygame.sprite.spritecollide(player, current_room.employees, False)
                if employee_collisions:
                    game_over = True
                    game_state = "game_over"
                    last_level = current_level

                    if high_score_manager.is_high_score(score):
                        player_name=score_display.show_name_entry(score)
                        high_score_manager.add_score(player_name,score)

        if game_state == "playing":
            # --- Drawing ---
            screen.fill(IKEA_BLUE)

            # Draw walls and player
            current_room.wall_list.draw(screen)
            movingsprites.draw(screen)

            # Draw items if they exist
            if hasattr(current_room, 'items'):
                current_room.items.draw(screen)

            # Draw employees if they exist
            if hasattr(current_room, 'employees'):
                current_room.employees.draw(screen)

            # Display score and collected items
            score_text = font.render(f'Score: {score}', True, WHITE)
            screen.blit(score_text, (10, 10))

            # Display level information
            level_text = font.render(f'Level: {current_level}', True, WHITE)
            screen.blit(level_text, (10, 30))

            # Display level progress
            progress_text = font.render(f'Items: {items_collected_this_level}/{items_needed_for_level}', True, WHITE)
            screen.blit(progress_text, (10, 50))

            '''for area in current_room.transition_areas:
                transition_surface = pygame.Surface((area[2], area[3]))
                transition_surface.set_alpha(100)  # More visible for debugging
                transition_surface.fill((0, 255, 0))  # Green indicator
                screen.blit(transition_surface, (area[0], area[1]))'''

        # Draw game over screen
        elif game_over or game_state == "game_over":
            # Draw overlay
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            # Game over text
            font_large = pygame.font.SysFont('Arial', 64)
            game_over_text = font_large.render('GAME OVER', True, WHITE)
            text_rect = game_over_text.get_rect(center=(400, 200))
            screen.blit(game_over_text, text_rect)

            # Subtitle
            subtitle_font = pygame.font.SysFont('Arial', 24)
            subtitle = subtitle_font.render('An IKEA employee found you!', True, WHITE)
            subtitle_rect = subtitle.get_rect(center=(400, 270))
            screen.blit(subtitle, subtitle_rect)

            # Final score
            score_font = pygame.font.SysFont('Arial', 36)
            final_score = score_font.render(f'Final Score: {score}', True, WHITE)
            score_rect = final_score.get_rect(center=(400, 320))
            screen.blit(final_score, score_rect)

            # Collected items
            if collected_items:
                items_font = pygame.font.SysFont('Arial', 18)
                items_title = items_font.render('Items Collected:', True, WHITE)
                screen.blit(items_title, (300, 360))

                # Show up to 5 most recent items
                for i, item in enumerate(collected_items[-5:]):
                    item_text = items_font.render(f'- {item}', True, WHITE)
                    screen.blit(item_text, (320, 385 + i * 20))

            # Restart instructions
            restart_font = pygame.font.SysFont('Arial', 18)
            restart_text = restart_font.render('Press R to restart or Q to quit', True, WHITE)
            restart_rect = restart_text.get_rect(center=(400, 500))
            screen.blit(restart_text, restart_rect)

            # Add high score option
            high_score_font = pygame.font.SysFont('Arial', 18)
            high_score_text = high_score_font.render('Press H to view high scores', True, WHITE)
            high_score_rect = high_score_text.get_rect(center=(400, 530))
            screen.blit(high_score_text, high_score_rect)

        elif game_state == "high_scores":
        # Use the existing show_high_scores method from HighScoreScreen
        # If it returns True, go back to game_over state
        # If it returns False, exit the game
            if score_display.show_high_scores():
                game_state = "game_over"
            else:
                done = True

        # Update the screen
        pygame.display.flip()

        # Limit to 60 frames per second
        clock.tick(60)

    # Only call pygame.quit() once at the end
    pygame.quit()


# This ensures main() is only called when the script is run directly
if __name__ == "__main__":
    main()