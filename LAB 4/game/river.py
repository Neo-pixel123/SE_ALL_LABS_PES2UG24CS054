import pygame

# Horizontal river band the player must cross on a moving log (Task 2).
RIVER_TOP = 250
RIVER_H = 80
LOG_H = 60
LOG_SPEED = 2
WATER = (40, 110, 190)
WATER_DARK = (30, 90, 160)
LOG_BROWN = (120, 80, 40)
LOG_RING = (90, 60, 30)


class Log:
    def __init__(self, x, length, speed):
        y = RIVER_TOP + (RIVER_H - LOG_H) // 2
        # Float x position so slow speeds stay smooth; rect is synced from it.
        self.x = float(x)
        self.rect = pygame.Rect(int(x), y, length, LOG_H)
        self.speed = speed

    def update(self, width):
        self.x += self.speed
        # Wrap around once fully off one side.
        if self.speed > 0 and self.x > width:
            self.x = -self.rect.width
        elif self.speed < 0 and self.x + self.rect.width < 0:
            self.x = width
        self.rect.x = int(self.x)

    def draw(self, screen):
        pygame.draw.rect(screen, LOG_BROWN, self.rect, border_radius=14)
        for i in range(1, self.rect.width // 40):
            x = self.rect.x + i * 40
            pygame.draw.line(screen, LOG_RING, (x, self.rect.y + 6), (x, self.rect.bottom - 6), 3)


class River:
    def __init__(self, width):
        self.width = width
        self.rect = pygame.Rect(0, RIVER_TOP, width, RIVER_H)
        # Three logs with gaps the player has to time.
        self.logs = [
            Log(0, 200, LOG_SPEED),
            Log(width * 0.45, 170, LOG_SPEED),
            Log(width * 0.85, 190, LOG_SPEED),
        ]
        self.ripple = 0

    def update(self):
        for log in self.logs:
            log.update(self.width)
        self.ripple = (self.ripple + 1) % 40

    def contains(self, point):
        return self.rect.collidepoint(point)

    def log_under(self, point):
        # Logs span the river's crossing path, so only horizontal overlap matters;
        # otherwise the thin water strip above/below a log would count as a splash.
        x = point[0]
        for log in self.logs:
            if log.rect.left <= x <= log.rect.right:
                return log
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, WATER, self.rect)
        for x in range(-40 + self.ripple, self.width, 40):
            pygame.draw.line(screen, WATER_DARK, (x, self.rect.y + 20), (x + 18, self.rect.y + 20), 2)
            pygame.draw.line(screen, WATER_DARK, (x + 20, self.rect.y + 55), (x + 38, self.rect.y + 55), 2)
        for log in self.logs:
            log.draw(screen)
