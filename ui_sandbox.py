import sys
import pygame
import images
import ui


# initializations
pygame.init()
pygame.mixer.init()
pygame.font.init()


TARGET_FPS = 60


def main():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.key.set_repeat(100)
    clock = pygame.time.Clock()

    sprites = pygame.sprite.RenderUpdates()

    def on_click(button):
        button.text = "Clicked!"
        button.draw()

    def hover_update(button, hovering):
        if hovering:
            button.text = "Hovering..."
            button.draw()
        else:
            button.text = "Gone"
            button.draw()

    button = ui.Button((0, 0, 300, 100), on_click_cb=on_click, hover_update_cb=hover_update, text="Click me!",
                       text_color=images.RED, bg_color=images.BLUE, text_offset=(30, 30))
    sprites.add(button)

    while True:
        # tick() returns a value in ms, we want a fractional second
        dt = clock.tick(TARGET_FPS) / 1000

        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        clicking=False

        for e in events:
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == pygame.BUTTON_LEFT:
                    clicking = True
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == pygame.BUTTON_LEFT:
                    clicking = False

        sprites.update(dt=dt, mouse_pos=mouse_pos, clicking=clicking)

        # render stuff
        screen.fill(images.BLACK)
        sprites.draw(screen)

        pygame.display.flip()


if "__main__" == __name__:
    main()
