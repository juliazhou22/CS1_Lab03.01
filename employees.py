import os
import pygame
import random


class Employee(pygame.sprite.Sprite):
    """This class represents IKEA employees that chase the player"""

    # List of possible employee image filenames
    EMPLOYEE_IMAGES = [
        "worker1.png",
        "worker2.png",
        "worker3.png",
        "worker4.png",
        "cook.png"
    ]

    def __init__(self, x, y, color=(255, 255, 0), image_name=None):
        """ Constructor function """
        # Call the parent's constructor
        super().__init__()

        # Store the default color (as fallback)
        self.color = color

        # If no specific image is requested, choose a random one
        if image_name is None:
            image_name = random.choice(self.EMPLOYEE_IMAGES)

        # Try to load the employee image
        try:
            # Construct the image path
            image_path = os.path.join('img', image_name)

            # Load the image
            original_image = pygame.image.load(image_path).convert_alpha()

            # Scale the image (adjust size as needed)
            self.image = pygame.transform.scale(original_image, (65, 65))

        except (pygame.error, FileNotFoundError) as e:
            # If image loading fails, fall back to colored rectangle
            print(f"Error loading employee image: {e}")
            self.image = pygame.Surface([20, 20])
            self.image.fill(self.color)

        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement variables
        self.change_x = 0
        self.change_y = 0

        # AI behavior variables
        self.speed = 2  # Slower than player
        self.detection_radius = 150  # How far they can "see" the player
        self.wander_timer = 0  # For random movement
        self.wander_direction = 0  # Current direction when wandering

    def move(self, walls):
        """Move the employee, checking for wall collisions"""
        # Move left/right
        self.rect.x += self.change_x

        # Check for wall collisions
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check for wall collisions
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def update(self, player, walls):
        """Update employee behavior based on player position"""
        # Calculate distance to player
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # If player is within detection radius, move toward player
        if distance < self.detection_radius:
            # Calculate direction to player
            if distance > 0:  # Avoid division by zero
                self.change_x = (dx / distance) * self.speed
                self.change_y = (dy / distance) * self.speed
            else:
                self.change_x = 0
                self.change_y = 0
        else:
            # Random wandering behavior
            self.wander_timer += 1

            # Change direction occasionally
            if self.wander_timer > 60:  # Change direction every ~1 second
                self.wander_timer = 0
                self.wander_direction = random.randint(0, 3)  # 0=up, 1=right, 2=down, 3=left

            # Set movement based on wander direction
            if self.wander_direction == 0:
                self.change_x = 0
                self.change_y = -self.speed
            elif self.wander_direction == 1:
                self.change_x = self.speed
                self.change_y = 0
            elif self.wander_direction == 2:
                self.change_x = 0
                self.change_y = self.speed
            elif self.wander_direction == 3:
                self.change_x = -self.speed
                self.change_y = 0

        # Move based on current change_x and change_y
        self.move(walls)