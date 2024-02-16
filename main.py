import os
import sys
import pygame
import particles
import images
from common import *

TARGET_FPS = 60


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.load_image(r"kenney\ufo\shipGreen_manned.png")
        self.rect = self.image.get_rect()

    def update(self, mouse_pos, *args, **kwargs):
        self.rect.topleft = mouse_pos


def main():
    # these initializations must happen before loading assets
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)

    particle_system = particles.ParticleSystem()
    spark_image_names = [r"kenney\particles\star_01.png",
                         r"kenney\particles\star_04.png",
                         r"kenney\particles\star_06.png",
                         r"kenney\particles\star_07.png",
                         r"kenney\particles\star_08.png",
                         r"kenney\particles\star_09.png"
                         ]
    spark_painter_factory = particles.ImagePainterFactory(spark_image_names, (32, 32), images.RAINBOW)
    spray = particles.SprayEmitter((0, 0), [(-200, 200), 0], (0, 500), 7,
                                   (0.8, 1.5), spark_painter_factory)
    particle_system.add_emitter(spray)

    # flame_painter_factory = particles.FancyFlamePainterFactory((12, 16))
    flame_painter_factory = particles.CartoonFlamePainterFactory((12, 16))
    point_flame = particles.SprayEmitter((0, 0), [(-30, 20), (-160, -200)], (0, 0), 2,
                                         0.8, flame_painter_factory, jitter=((-10, 10), 0))
    particle_system.add_emitter(point_flame)
    fire_sfx = pygame.mixer.Sound(os.path.join(ASSETS_DIR, r"sfx\Fire-burning-sound-effect.mp3"))
    chime_sfx = pygame.mixer.Sound(os.path.join(ASSETS_DIR, r"sfx\Soothing-chime-effect.mp3"))

    cursor = Cursor()
    sprites = pygame.sprite.RenderUpdates()
    sprites.add(cursor)
    clock = pygame.time.Clock()

    pygame.key.set_repeat(100)  # held keys will generate repeated inputs this often
    # note: this logic seems to be buggy if you hold two keys at once and then release one of them

    while True:
        # tick() returns a value in ms, we want a fractional second
        dt = clock.tick(TARGET_FPS) / 1000

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # THIS IS ACTUALLY KINDA BACKWARDS, you can/should just check event.key
                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE]:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    spray.enabled = True
                    chime_sfx.play(loops=-1, fade_ms=500)
                elif event.button == pygame.BUTTON_RIGHT:
                    point_flame.enabled = True
                    fire_sfx.play()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    spray.enabled = False
                    chime_sfx.fadeout(800)
                elif event.button == pygame.BUTTON_RIGHT:
                    point_flame.enabled = False
                    fire_sfx.fadeout(800)

        sprites.update(dt=dt, mouse_pos=mouse_pos)
        particle_system.update(dt)
        spray.move((mouse_pos[0] + 50, mouse_pos[1] + 110))
        point_flame.move((mouse_pos[0] + 60, mouse_pos[1] - 20))

        screen.fill(images.BLACK)
        sprites.draw(screen)
        particle_system.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
