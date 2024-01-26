import sys
from common import *
import particles, images

TARGET_FPS = 60


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.load_image(r"kenney\ufo\shipGreen_manned.png")
        self.rect = self.image.get_rect()

    def update(self, mouse_pos):
        self.rect.topleft = mouse_pos


def main():
    # these initializations must happen before loading assets
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)

    black = 0, 0, 0

    particle_system = particles.ParticleSystem()
    spark_image_names = [r"kenney\particles\star_01.png",
                         r"kenney\particles\star_04.png",
                         r"kenney\particles\star_06.png",
                         r"kenney\particles\star_07.png",
                         r"kenney\particles\star_08.png",
                         r"kenney\particles\star_09.png"
                         ]
    painter_factory = particles.ImagePainterFactory(spark_image_names, (32, 32), images.RAINBOW)
    spray = particles.SprayEmitter((0, 0), [(-200, 200), 0], (0, 500), 7,
                                   (0.8, 1.5), painter_factory)
    particle_system.add_emitter(spray)

    cursor = Cursor()
    sprites = pygame.sprite.RenderPlain()
    sprites.add(cursor)
    clock = pygame.time.Clock()

    pygame.key.set_repeat(100)  # held keys will generate repeated inputs this often
    # note: this logic seems to be buggy if you hold two keys at once and then release one of them

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE]:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    spray.enable()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    spray.disable()

        sprites.update(mouse_pos=mouse_pos)
        particle_system.update(1 / TARGET_FPS)  # better way?
        spray.move((mouse_pos[0] + 50, mouse_pos[1] + 110))

        screen.fill(black)
        sprites.draw(screen)
        particle_system.draw(screen)
        pygame.display.flip()

        clock.tick(TARGET_FPS)


if __name__ == '__main__':
    main()
