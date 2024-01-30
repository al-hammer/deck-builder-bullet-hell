from common import *
import images
import pygame
import pygame.gfxdraw


class Particle(object):
    def __init__(self, pos, lifetime):
        self.pos = [float(p) for p in pos]
        self.alive = True
        self.time = 0.0
        self.lifetime = lifetime

    # update state according to time,
    # update alive if necessary
    def update(self, delta_time_secs):
        self.time += delta_time_secs
        if self.time >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        pass


class Painter(object):
    def draw(self, surface, pos, time, lifetime):
        pass


class PixelPainter(Painter):
    def __init__(self, color):
        self.color = pygame.Color(color)

    def draw(self, surface, pos, time, lifetime):
        surface.set_at(pos, self.color)


class ImagePainter(Painter):
    def __init__(self, image):
        self.image = image

    def draw(self, surface, pos, time, lifetime):
        self.image.set_alpha(min(255, int(255 * (1.0 - (time / lifetime)))))
        surface.blit(self.image, pos)


# a flame particle is drawn a circle that shrinks and cools down
# in time according to the images.FIRE spectrum
class CartoonFlamePainter(Painter):
    FIRE_GRADIENT = [images.YELLOW, images.ORANGE, images.RED, images.BLACK]
    DEFAULT_RADIUS = 10
    STEPS = len(FIRE_GRADIENT)
    STEP_SIZE = 1.0/(STEPS - 1)

    def __init__(self, radius=DEFAULT_RADIUS):
        self.radius = radius

    def draw(self, surface, pos, time, lifetime):
        progress = min(1.0, time / lifetime)
        decay = 1.0 - progress
        # compute current temperature (i.e. color) from progress
        step = int(progress / CartoonFlamePainter.STEP_SIZE)
        step_progress = (progress - step * CartoonFlamePainter.STEP_SIZE) / CartoonFlamePainter.STEP_SIZE
        complement = 1.0 - step_progress
        if step == CartoonFlamePainter.STEPS:
            # last color
            color = CartoonFlamePainter.FIRE_GRADIENT[step]
        else:
            color = pygame.Color(int(CartoonFlamePainter.FIRE_GRADIENT[step].r * complement +
                                 CartoonFlamePainter.FIRE_GRADIENT[step + 1].r * step_progress),
                                 int(CartoonFlamePainter.FIRE_GRADIENT[step].g * complement +
                                 CartoonFlamePainter.FIRE_GRADIENT[step + 1].g * step_progress),
                                 int(CartoonFlamePainter.FIRE_GRADIENT[step].b * complement +
                                 CartoonFlamePainter.FIRE_GRADIENT[step + 1].b * step_progress))

        pygame.gfxdraw.filled_circle(surface, pos[0], pos[1], int(self.radius * decay), color)


class FancyFlamePainter(Painter):
    DEFAULT_RADIUS = 10
    FIRE_GRADIENT = [images.ORANGE, images.RED, images.BLACK]
    STEPS = len(FIRE_GRADIENT)
    STEP_SIZE = 1.0/(STEPS - 1)
    KERNEL_ALPHA = 32
    AURA_ALPHA = 16
    AURA_MULTIPLIER = 2.0

    def __init__(self, radius=DEFAULT_RADIUS):
        self.radius = radius
        self.aura_radius = int(radius * FancyFlamePainter.AURA_MULTIPLIER)
        self.surface = pygame.Surface((2 * self.aura_radius, 2 * self.aura_radius), flags=pygame.SRCALPHA)

    def draw(self, surface, pos, time, lifetime):
        self.surface.fill(images.TRANSPARENT)
        progress = min(1.0, time / lifetime)
        decay = 1.0 - progress
        # compute current temperature (i.e. color) from progress
        step = int(progress / FancyFlamePainter.STEP_SIZE)
        step_progress = (progress - step * FancyFlamePainter.STEP_SIZE) / FancyFlamePainter.STEP_SIZE
        complement = 1.0 - step_progress
        if step == FancyFlamePainter.STEPS:
            # last color
            color = FancyFlamePainter.FIRE_GRADIENT[step]
        else:
            color = pygame.Color(int(FancyFlamePainter.FIRE_GRADIENT[step].r * complement +
                                 FancyFlamePainter.FIRE_GRADIENT[step + 1].r * step_progress),
                                 int(FancyFlamePainter.FIRE_GRADIENT[step].g * complement +
                                 FancyFlamePainter.FIRE_GRADIENT[step + 1].g * step_progress),
                                 int(FancyFlamePainter.FIRE_GRADIENT[step].b * complement +
                                 FancyFlamePainter.FIRE_GRADIENT[step + 1].b * step_progress),
                                 FancyFlamePainter.KERNEL_ALPHA)
        # draw fire kernel
        pygame.gfxdraw.filled_circle(self.surface, self.aura_radius,
                                     self.aura_radius, int(self.radius * decay), color)
        # draw fire aura
        # color.a = FancyFlamePainter.AURA_ALPHA
        pygame.gfxdraw.filled_circle(self.surface, self.aura_radius,
                                     self.aura_radius, int(self.aura_radius * decay), color)
        surface.blit(self.surface, pos, special_flags=pygame.BLEND_RGBA_ADD)


class PainterFactory(object):
    def build(self, *args, **kwargs):
        pass


class PixelPainterFactory(PainterFactory):
    def __init__(self, colors):
        self.colors = [pygame.Color(c) for c in colors]

    def build(self, *args, **kwargs):
        color = random.choice(self.colors)
        return PixelPainter(color)


class ImagePainterFactory(PainterFactory):
    def __init__(self, image_names, target_size=None, colors=None):
        self.images = [images.load_image(im) for im in image_names]
        if target_size is not None:
            self.images = [pygame.transform.scale(im, target_size) for im in self.images]
        if colors is not None:
            recolored_images = []
            for image in self.images:
                for color in colors:
                    recolored_images.append(images.recolor_image(image, color))
            self.images = recolored_images

    def build(self, *args, **kwargs):
        return ImagePainter(random.choice(self.images))


class CartoonFlamePainterFactory(PainterFactory):
    def __init__(self, radius):
        self.radius = radius

    def build(self, *args, **kwargs):
        return CartoonFlamePainter(resolve_range(self.radius))


class FancyFlamePainterFactory(PainterFactory):
    def __init__(self, radius):
        self.radius = radius

    def build(self, *args, **kwargs):
        return FancyFlamePainter(resolve_range(self.radius))


# a particle with lifetime, velocity and acceleration
class MovingParticle(Particle):
    def __init__(self, pos, lifetime, velocity, acceleration, painter):
        super().__init__(pos, lifetime)
        self.velocity = list(velocity)  # need to mutate later
        self.acceleration = acceleration
        self.painter = painter

    def update(self, delta_time_secs):
        super().update(delta_time_secs)
        # might be irrelevant if particle is dead but that's ok
        self.velocity[0] += self.acceleration[0] * delta_time_secs
        self.velocity[1] += self.acceleration[1] * delta_time_secs
        self.pos[0] += self.velocity[0] * delta_time_secs
        self.pos[1] += self.velocity[1] * delta_time_secs

    def draw(self, surface):
        pos = [int(p) for p in self.pos]
        self.painter.draw(surface, pos, self.time, self.lifetime)


class Emitter(object):
    def __init__(self, pos):
        self.pos = [float(p) for p in pos]
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def move(self, pos):
        self.pos = [float(p) for p in pos]

    def update(self, delta_time_secs):
        pass

    def emit_if_enabled(self):
        if self.enabled:
            return self.emit()
        return []

    def emit(self):
        return []


# spray particles from pos with given velocity and acceleration,
# with a color chosen randomly from given colors and at given rate per frame
# rate, velocity and acceleration can contain tuples instead of values to specify
# a range of values
class SprayEmitter(Emitter):
    def __init__(self, pos, velocity, acceleration, rate, particle_lifetime, painter_factory, jitter=(0, 0)):
        super().__init__(pos)
        self.velocity = velocity
        self.acceleration = acceleration
        self.rate = rate
        self.particle_lifetime = particle_lifetime
        self.painter_factory = painter_factory
        self.jitter = jitter

    def emit(self):
        new_particles = []

        effective_rate = resolve_range(self.rate)
        for _ in range(effective_rate):
            painter = self.painter_factory.build()
            lifetime = resolve_range(self.particle_lifetime)

            velocity = list(self.velocity)
            velocity[0] = resolve_range(velocity[0])
            velocity[1] = resolve_range(velocity[1])

            acceleration = list(self.acceleration)
            acceleration[0] = resolve_range(acceleration[0])
            acceleration[1] = resolve_range(acceleration[1])

            pos = list(self.pos)
            pos[0] += resolve_range(self.jitter[0])
            pos[1] += resolve_range(self.jitter[1])

            new_particles.append(MovingParticle(pos, lifetime, velocity, acceleration, painter))

        return new_particles


class ParticleSystem(object):
    def __init__(self):
        self.particles = set()
        self.emitters = set()

    # add particle(s)
    def add_particles(self, particles):
        if hasattr(particles, "__iter__"):
            for p in particles:
                self.particles.update(particles)
        else:
            self.particles.add(particles)

    # register emitter
    def add_emitter(self, emitter):
        self.emitters.add(emitter)

    # deregister emitter
    def remove_emitter(self, emitter):
        self.emitters.remove(emitter)

    def update(self, delta_time_secs):
        # update emitters (and allow them to deregister)
        for e in self.emitters:
            e.update(delta_time_secs)

        # call emitters
        for e in self.emitters:
            self.add_particles(e.emit_if_enabled())

        # call update() on all particles
        for p in self.particles:
            p.update(delta_time_secs)

        # prune dead particles
        particles_to_remove = {p for p in self.particles if not p.alive}
        self.particles.difference_update(particles_to_remove)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

