from common import *
import images


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
    def __init__(self, pos, velocity, acceleration, rate, particle_lifetime, painter_factory):
        super().__init__(pos)
        self.velocity = velocity
        self.acceleration = acceleration
        self.rate = rate
        self.particle_lifetime = particle_lifetime
        self.painter_factory = painter_factory

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

            new_particles.append(MovingParticle(self.pos, lifetime, velocity, acceleration, painter))

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

