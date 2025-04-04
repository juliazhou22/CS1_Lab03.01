import os
import pygame
import random
from item_types import ITEM_TYPES


class Item(pygame.sprite.Sprite):
    """This class represents collectible items that the player can pick up"""

    ITEM_TYPES = ITEM_TYPES

    def __init__(self, x, y, item_type=None):
        """ Constructor function """
        # Call the parent's constructor
        super().__init__()

        # If no item type specified, choose random one
        if item_type is None:
            item_type = random.randint(0, len(self.ITEM_TYPES) - 1)

        # Get item properties
        item_props = self.ITEM_TYPES[item_type]
        self.name = item_props["name"]
        self.color = item_props["color"]
        self.item_type = item_type

        # Try to load an image
        try:
            # Construct the image path
            # Replace spaces with underscores for filename
            image_filename = f"{self.name.replace(' ', '_')}.png"
            image_path = os.path.join('img', image_filename)

            # Load the image
            original_image = pygame.image.load(image_path).convert_alpha()

            # Scale the image (adjust size as needed)
            self.image = pygame.transform.scale(original_image, (60, 60))

        except (pygame.error, FileNotFoundError) as e:
            # If image loading fails, fall back to colored rectangle
            print(f"Error loading image: {e}")
            self.image = pygame.Surface([60, 60], pygame.SRCALPHA)
            self.image.fill(self.color)

        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    @classmethod
    def generate_valid_position(cls, room, existing_items, max_attempts=100):
        """Generate a valid position for an item that doesn't overlap with walls or other items"""
        width, height = 800, 600  # Screen dimensions
        item_size = 10  # Size of the item
        padding = 20  # Additional padding from walls

        # Try to find a valid position
        for _ in range(max_attempts):
            # Generate random position with more strict boundaries
            x = random.randint(padding, width - padding - item_size)
            y = random.randint(padding, height - padding - item_size)

            # Create a temporary rect to check collisions
            temp_rect = pygame.Rect(x, y, item_size, item_size)

            # Check wall collisions
            wall_collision = False
            for wall in room.wall_list:
                wall_rect = pygame.Rect(
                    wall.rect.x - item_size,
                    wall.rect.y - item_size,
                    wall.rect.width + item_size * 2,
                    wall.rect.height + item_size * 2
                )

                if temp_rect.colliderect(wall_rect):
                    wall_collision = True
                    break

            if wall_collision:
                continue

            # Check item collisions
            item_collision = False
            for item in existing_items:
                item_buffer_rect = pygame.Rect(
                    item.rect.x - item_size,
                    item.rect.y - item_size,
                    item.rect.width + item_size * 2,
                    item.rect.height + item_size * 2
                )

                if temp_rect.colliderect(item_buffer_rect):
                    item_collision = True
                    break

            if item_collision:
                continue

            # If we get here, the position is valid
            return x, y

        # If we couldn't find a valid position after max attempts
        return None, None