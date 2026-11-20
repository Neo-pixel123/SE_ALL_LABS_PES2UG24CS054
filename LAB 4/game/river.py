import pygame

WATER=(40,90,170)
WATER_LINE=(80,140,210)
LOG_COLOR=(120,80,40)
LOG_DARK=(90,55,25)

class Log:
    def __init__(self, x, width, y, height):
        self.x=float(x)
        self.rect=pygame.Rect(int(x),y,width,height)

    def sync(self):
        self.rect.x=int(self.x)

class River:
    """A horizontal water band. Standing in it is only safe on a moving log."""
    def __init__(self, top, height, width, speed=1.6, direction=1):
        self.rect=pygame.Rect(0,top,width,height)
        self.width=width
        self.speed=speed
        self.direction=direction
        self.span=width+200  # logs wrap over this distance
        log_y,log_h=top+8,height-16
        self.logs=[Log(x,w,log_y,log_h) for x,w in [(0,200),(300,170),(560,190)]]

    @property
    def velocity(self):
        return self.speed*self.direction

    def update(self):
        for log in self.logs:
            log.x+=self.velocity
            if self.direction>0 and log.x>self.width: log.x-=self.span
            if self.direction<0 and log.x+log.rect.width<0: log.x+=self.span
            log.sync()

    def contains(self, prect):
        """True when the player is standing in the water row."""
        return abs(prect.centery-self.rect.centery)<20

    def log_under(self, prect):
        for log in self.logs:
            if log.rect.left<=prect.centerx<=log.rect.right:
                return log
        return None

    def draw(self, screen, tick=0):
        pygame.draw.rect(screen,WATER,self.rect)
        for i in range(0,self.width,40):
            x=(i+tick//2)%self.width
            pygame.draw.line(screen,WATER_LINE,(x,self.rect.y+6),(x+14,self.rect.y+6),2)
            pygame.draw.line(screen,WATER_LINE,(self.width-x,self.rect.bottom-6),(self.width-x+14,self.rect.bottom-6),2)
        for log in self.logs:
            pygame.draw.rect(screen,LOG_COLOR,log.rect,border_radius=14)
            for gx in range(log.rect.x+20,log.rect.right-10,35):
                pygame.draw.line(screen,LOG_DARK,(gx,log.rect.y+12),(gx+18,log.rect.y+12),2)
                pygame.draw.line(screen,LOG_DARK,(gx+8,log.rect.bottom-12),(gx+26,log.rect.bottom-12),2)
