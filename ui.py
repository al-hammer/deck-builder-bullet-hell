import pygame
import images

pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont("Candara", 50)
DEFAULT_TEXT_COLOR = images.WHITE


# TODO design + implement
class Button(pygame.sprite.Sprite):
    # on_click_cb(button)
    # hover_update_cb(button, hovering)
    def __init__(self, rect, hover_update_cb=None, on_click_cb=None,
                 bg_color=images.TRANSPARENT,
                 image=None, image_offset=None, use_image_size=False,
                 text=None, text_color=DEFAULT_TEXT_COLOR, text_bg_color=None,
                 text_offset=(0, 0), font=DEFAULT_FONT, text_width=0):
        pygame.sprite.Sprite.__init__(self)
        self.hovering = False
        self.hover_update_cb = hover_update_cb
        self.on_click_cb = on_click_cb

        self.rect = pygame.Rect(rect)  # button position and size
        if use_image_size and image is not None:
            self.rect.size = image.get_size()
        self.bg_color = bg_color  # background color for the entire button

        self.button_image = image
        self.button_image_offset = image_offset

        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_bg_color = text_bg_color
        self.text_offset = text_offset
        self.text_width = text_width

        self.image = pygame.surface.Surface(self.rect.size)
        self.draw()  # update image

    # update .image here (call only when needed)
    def draw(self):
        self.image.fill(self.bg_color)
        # draw image
        if self.button_image is not None:
            self.image.blit(self.button_image, self.button_image.get_rect(topleft=self.button_image_offset))
        # draw text
        if self.text is not None:
            text_image = self.font.render(self.text, True, self.text_color, self.text_bg_color, self.text_width)
            self.image.blit(text_image, text_image.get_rect(topleft=self.text_offset))

    def update(self, mouse_pos, clicking, *args, **kwargs):
        collides = self.rect.collidepoint(*mouse_pos)

        if not collides and self.hovering:
            self.hovering = False
            if self.hover_update_cb is not None:
                self.hover_update_cb(self, self.hovering)

        if collides:
            if not self.hovering:
                self.hovering = True
                if self.hover_update_cb is not None:
                    self.hover_update_cb(self, self.hovering)
            if clicking:
                if self.on_click_cb is not None:
                    self.on_click_cb(self)


