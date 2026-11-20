import pygame

# Day/night cycle (Task 4): switch every 30 seconds; at night cars show long headlight beams.
CYCLE_SECONDS = 30
HEADLIGHT_LEN = 230
DARKNESS = (5, 5, 25, 185)
LIT_AREA = (5, 5, 25, 95)  # e.g. moonlit river, so logs stay readable
BEAM_DARKNESS = (5, 5, 25, 55)
BEAM_GLOW = (255, 240, 170, 50)


class DayNight:
    def __init__(self, fps):
        self.cycle_frames = CYCLE_SECONDS * fps
        self.fps = fps
        self.timer = 0
        self.night = False

    def update(self):
        self.timer += 1
        if self.timer >= self.cycle_frames:
            self.timer = 0
            self.night = not self.night

    def seconds_left(self):
        return (self.cycle_frames - self.timer + self.fps - 1) // self.fps

    @staticmethod
    def _beam(rect, direction):
        """Cone of light starting at the front of a vehicle (direction 1=down, -1=up)."""
        if direction == 1:
            y0, y1 = rect.bottom, rect.bottom + HEADLIGHT_LEN
        else:
            y0, y1 = rect.top, rect.top - HEADLIGHT_LEN
        return [(rect.left + 6, y0), (rect.right - 6, y0),
                (rect.right + 30, y1), (rect.left - 30, y1)]

    def draw(self, screen, cars, player, lit_rects=()):
        if not self.night:
            return
        w, h = screen.get_size()
        dark = pygame.Surface((w, h), pygame.SRCALPHA)
        dark.fill(DARKNESS)
        for r in lit_rects:
            pygame.draw.rect(dark, LIT_AREA, r)
        glow = pygame.Surface((w, h), pygame.SRCALPHA)
        lights = [(c.rect, c.direction) for c in cars] + [(player.rect, -1)]
        for rect, direction in lights:
            beam = self._beam(rect, direction)
            # draw.* overwrites alpha on SRCALPHA surfaces, punching a lighter hole in the dark.
            pygame.draw.polygon(dark, BEAM_DARKNESS, beam)
            pygame.draw.rect(dark, BEAM_DARKNESS, rect.inflate(8, 8), border_radius=8)
            pygame.draw.polygon(glow, BEAM_GLOW, beam)
        screen.blit(dark, (0, 0))
        screen.blit(glow, (0, 0))
        # Headlight bulbs.
        for rect, direction in lights:
            y = rect.bottom - 4 if direction == 1 else rect.top + 4
            for x in (rect.left + 10, rect.right - 10):
                pygame.draw.circle(screen, (255, 250, 200), (x, y), 4)
