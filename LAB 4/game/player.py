import pygame

SPEED=4
LANE_W=80
HOP=40          # vertical distance per forward/back hop
MOVE_COOLDOWN=10  # frames between moves (was: no cooldown on vertical -> 8px every frame)

class Player:
    def __init__(self, x, y):
        self.rect=pygame.Rect(x-20,y-30,40,60)
        self.color=(60,160,220)
        self.move_cooldown=0

    def move(self, keys, min_x, max_x, max_y=None):
        if self.move_cooldown>0:
            self.move_cooldown-=1
            return
        dx=dy=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx=-LANE_W
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx=LANE_W
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy=-HOP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy=HOP
        if dx:
            self.rect.x=max(min_x,min(max_x-self.rect.width,self.rect.x+dx))
        if dy:
            ny=max(0,self.rect.y+dy)
            if max_y is not None: ny=min(max_y,ny)
            self.rect.y=ny
        if dx or dy:
            self.move_cooldown=MOVE_COOLDOWN

    def snap_to_lane(self, max_x):
        lane=max(0,min(max_x//LANE_W-1,self.rect.centerx//LANE_W))
        self.rect.centerx=lane*LANE_W+LANE_W//2

    def draw(self,screen):
        # car body
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        # windows
        pygame.draw.rect(screen,(180,220,240),pygame.Rect(self.rect.x+6,self.rect.y+8,28,18),border_radius=4)
        # wheels
        for wx in [self.rect.x+4,self.rect.right-12]:
            for wy in [self.rect.y+4,self.rect.bottom-14]:
                pygame.draw.rect(screen,(30,30,30),pygame.Rect(wx,wy,8,10),border_radius=3)
