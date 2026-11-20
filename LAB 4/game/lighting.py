import pygame

PHASE_FRAMES=30*60   # switch day <-> night every 30 s at 60 FPS
FADE_FRAMES=60       # 1 s dusk/dawn transition
NIGHT_ALPHA=185      # how dark the night overlay gets
NIGHT_BEAM=260       # headlight reach at night (px ahead of the car)

class DayNight:
    def __init__(self):
        self.t=0

    def update(self):
        self.t+=1

    @property
    def is_night(self):
        return (self.t//PHASE_FRAMES)%2==1

    def darkness(self):
        """0 (full day) .. NIGHT_ALPHA (full night), with a fade at each switch."""
        k=min(1.0,(self.t%PHASE_FRAMES)/FADE_FRAMES)
        if self.t<PHASE_FRAMES: k=1.0  # first day starts fully lit
        return int(NIGHT_ALPHA*(k if self.is_night else 1-k))

    def seconds_to_switch(self):
        return (PHASE_FRAMES-self.t%PHASE_FRAMES)//60

    def draw(self, screen, cars, player_rect):
        a=self.darkness()
        if a<=0: return
        w,h=screen.get_size()
        dark=pygame.Surface((w,h),pygame.SRCALPHA)
        dark.fill((5,5,25,a))
        glow=pygame.Surface((w,h),pygame.SRCALPHA)
        beam=int(NIGHT_BEAM*a/NIGHT_ALPHA)
        for c in cars:
            cx=c.rect.centerx
            fy=c.rect.bottom if c.direction==1 else c.rect.top
            far=fy+beam*c.direction
            cone=[(cx-24,fy),(cx+24,fy),(cx+60,far),(cx-60,far)]
            # punch the cone (and the car body) out of the darkness, add warm light
            pygame.draw.polygon(dark,(5,5,25,a//5),cone)
            pygame.draw.rect(dark,(5,5,25,a//3),c.rect.inflate(10,10),border_radius=10)
            pygame.draw.polygon(glow,(255,230,140,int(45*a/NIGHT_ALPHA)),cone)
        pygame.draw.circle(dark,(5,5,25,a//3),player_rect.center,55)
        screen.blit(dark,(0,0))
        screen.blit(glow,(0,0))

def draw_icon(screen, x, y, night):
    if night:
        pygame.draw.circle(screen,(230,230,250),(x,y),9)
        pygame.draw.circle(screen,(20,20,20),(x+4,y-3),8)
    else:
        pygame.draw.circle(screen,(255,210,60),(x,y),8)
