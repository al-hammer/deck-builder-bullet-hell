import pygame.sprite


class Animation(object):
    def __init__(self, cancellable):
        self.cancellable = cancellable

    def update(self, sprite, dt):
        pass


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation = None

    def update_animation(self, dt):
        if self.animation is not None:
            self.animation.update(self, dt)

    def set_animation(self, new_animation):
        if (self.animation is None) or self.animation.cancellable:
            self.animation = new_animation

    def cancel_animation(self, animation):
        if self.animation == animation:
            self.animation = None


class Movement(Animation):
    def __init__(self, travel_origin, travel_target, travel_time):
        super().__init__(cancellable=True)
        self.travel_origin = travel_origin
        self.travel_target = travel_target
        self.travel_time = travel_time
        self.current_time = 0.0

    def update(self, sprite, dt):
        self.current_time += dt

        if self.current_time >= self.travel_time:
            sprite.cancel_animation(self)
            return

        # good old linear interpolation
        a = self.current_time / self.travel_time
        b = 1.0 - a
        pos = (self.travel_origin[0] * b + self.travel_target[0] * a,
               self.travel_origin[1] * b + self.travel_target[1] * a)
        sprite.rect.topleft = pos
