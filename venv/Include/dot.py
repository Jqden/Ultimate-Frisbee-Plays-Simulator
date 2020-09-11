import pygame

SIZE = 4


class Dot(pygame.sprite.Sprite):

    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([SIZE, SIZE])
        self.image.fill((200, 0, 0))  # darker red
        self.rect = self.image.get_rect()

        self.rect.x = xy[0] - SIZE / 2
        self.rect.y = xy[1] - SIZE / 2
