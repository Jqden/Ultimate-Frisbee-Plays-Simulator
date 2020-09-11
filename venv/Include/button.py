import pygame


# Defines a button which swaps between the colors red and blue when clicked.
class Button(pygame.sprite.Sprite):

    # Setup a square surface of user-defined location and size.
    def __init__(self, xy, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size, size])  # a square
        self.o_color = (200, 0, 0)  # red, the color of offensive players
        self.d_color = (0, 0, 200)  # blue, the color of defensive players
        self.image.fill(self.o_color)
        self.rect = self.image.get_rect()

        self.rect.x = xy[0]
        self.rect.y = xy[1]
        self.color = self.o_color

    def update(self):
        self.pressed()

    def pressed(self):
        if self.color == self.o_color:
            self.color = self.d_color
            self.image.fill(self.d_color)
        else:
            self.color = self.o_color
            self.image.fill(self.o_color)
