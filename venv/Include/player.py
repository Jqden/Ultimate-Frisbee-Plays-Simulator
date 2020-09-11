import pygame


# Parent class for the Offender and Defender classes. Creates the player
# surface on the screen and defines shared behavior for altering the color
# of players. Inherits the Sprite class so it easy to draw on the screen and
# implement hit detection and group updates.
class Player(pygame.sprite.Sprite):

    # Creates a square surface in a user-specified spot on the field.
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.size = 10
        self.image = pygame.Surface([self.size, self.size])  # a 10x10 square
        self.rect = self.image.get_rect()
        self.rect.x = xy[0] - self.size / 2  # adjusts the input location so that the middle of the square is where
        self.rect.y = xy[1] - self.size / 2  # the user clicked, instead of the top right corner

        self.color_locked = False
        self.main_color = None
        self.off_color = None

    def set_main_color(self):
        if not self.color_locked:
            self.image.fill(self.main_color)

    def set_off_color(self):
        if not self.color_locked:
            self.image.fill(self.off_color)

    # Sets player color to off color, then locks the color so it cannot be changed by "set_off/main_color" methods
    def lock_off_color(self):
        self.image.fill(self.off_color)
        self.color_locked = True

    # Unlocks player color so it can be changed by "set_off/main_color" methods, sets player color to main color
    def unlock_main_color(self):
        self.color_locked = False
        self.image.fill(self.main_color)
