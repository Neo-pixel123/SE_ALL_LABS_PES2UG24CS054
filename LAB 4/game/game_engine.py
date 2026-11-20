import pygame
import random
from game.player import Player,LANE_W
from game.traffic import Car,make_car
from game.river import River
from game.highscores import HighScores
from game.daynight import DayNight

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
BG=(60,60,60)

START_LIVES=3
INVULN_FRAMES=90      # 1.5 s of blinking after losing a life
WIN_BONUS=5000        # +500 displayed points for reaching the top

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.small_font=pygame.font.SysFont("monospace",20,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.highscores=HighScores()
        self.reset()

    def reset(self):
        self.player=Player(WIDTH//2,HEIGHT-80)
        self.cars=[]
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.game_over=False
        self.won=False
        # Task 1: lives
        self.lives=START_LIVES
        self.invuln=0
        self.flash_text=""
        self.flash_timer=0
        # Task 2: river with moving logs
        self.river=River(WIDTH)
        # Task 4: day/night cycle
        self.daynight=DayNight(FPS)
        # Task 3: high score bookkeeping for this run
        self.recorded=False
        self.new_rank=None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def display_score(self):
        return self.score//10

    def finish(self):
        """Record the run in the high score table exactly once."""
        if not self.recorded:
            self.new_rank=self.highscores.submit(self.display_score())
            self.recorded=True

    def lose_life(self,reason):
        self.lives-=1
        if self.lives<=0:
            self.lives=0
            self.game_over=True
            self.end_reason=reason
            self.finish()
            return
        # Respawn at the start with a short grace period.
        self.player=Player(WIDTH//2,HEIGHT-80)
        self.invuln=INVULN_FRAMES
        self.flash_text=f"{reason}  -1 LIFE"
        self.flash_timer=60

    def update(self):
        if self.game_over or self.won: return
        self.daynight.update()
        if self.invuln>0: self.invuln-=1
        if self.flash_timer>0: self.flash_timer-=1
        keys=pygame.key.get_pressed()
        self.player.move(keys,0,WIDTH)
        self.player.rect.bottom=min(self.player.rect.bottom,HEIGHT)
        self.river.update()
        self.timer+=1
        if self.timer>=self.spawn_interval:
            lane=random.randint(0,LANES-1)
            self.cars.append(make_car(lane,HEIGHT,self.speed))
            self.timer=0
            self.spawn_interval=max(22,self.spawn_interval-0.2)
        for c in self.cars:
            c.update()
        self.cars=[c for c in self.cars if not c.off_screen(HEIGHT)]

        center=self.player.rect.center
        if self.river.contains(center):
            # Cars pass under the river, so only the water matters here.
            log=self.river.log_under(center)
            if log is None:
                self.lose_life("SPLASH!")
                return
            self.player.rect.x+=log.speed
            if not 0<=self.player.rect.centerx<=WIDTH:
                self.lose_life("SWEPT AWAY!")
                return
        elif self.invuln==0:
            for c in self.cars:
                if c.rect.colliderect(self.player.rect):
                    self.lose_life("CRASHED!")
                    return

        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)
        if self.player.rect.top<=10:
            self.won=True
            self.score+=WIN_BONUS
            self.finish()

    def draw(self):
        self.screen.fill(BG)
        # road markings
        for i in range(LANES+1):
            pygame.draw.line(self.screen,(100,100,100),(i*LANE_W,0),(i*LANE_W,HEIGHT),2)
        for y in range(0,HEIGHT,60):
            for i in range(LANES):
                pygame.draw.rect(self.screen,(200,200,100),pygame.Rect(i*LANE_W+LANE_W//2-3,y,6,30))
        # sidewalks
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,HEIGHT-50,WIDTH,50))
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,0,WIDTH,30))
        for c in self.cars: c.draw(self.screen)
        self.river.draw(self.screen)
        # Blink while invulnerable after losing a life.
        if self.invuln==0 or (self.invuln//6)%2==0:
            self.player.draw(self.screen)
        self.daynight.draw(self.screen,self.cars,self.player,[self.river.rect])
        self._draw_hud()
        if self.flash_timer>0 and not (self.game_over or self.won):
            f=self.font.render(self.flash_text,True,(255,90,90))
            self.screen.blit(f,(WIDTH//2-f.get_width()//2,HEIGHT//2-f.get_height()//2))
        if self.game_over:
            self._msg("GAME OVER",(220,60,60))
        if self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        pygame.display.flip()

    def _draw_hud(self):
        hud=pygame.Rect(0,0,WIDTH,30)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        s=self.small_font.render(f"Score: {self.display_score()}",True,(220,220,220))
        self.screen.blit(s,(6,5))
        # Lives as hearts
        lx=s.get_width()+24
        for i in range(START_LIVES):
            color=(230,60,80) if i<self.lives else (80,80,80)
            self._heart(lx+i*24,15,color)
        best=max(self.highscores.best(),self.display_score())
        phase="NIGHT" if self.daynight.night else "DAY"
        r=self.small_font.render(f"Best: {best}  {phase} {self.daynight.seconds_left()}s",True,(220,220,220))
        self.screen.blit(r,(WIDTH-r.get_width()-6,5))

    def _heart(self,x,y,color):
        pygame.draw.circle(self.screen,color,(x-4,y-2),5)
        pygame.draw.circle(self.screen,color,(x+4,y-2),5)
        pygame.draw.polygon(self.screen,color,[(x-9,y),(x+9,y),(x,y+9)])

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,170))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        y=110
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,y))
        sc=self.font.render(f"Final score: {self.display_score()}",True,(240,240,240))
        self.screen.blit(sc,(WIDTH//2-sc.get_width()//2,y+60))
        # Task 3: top-5 high score table
        t=self.font.render("TOP 5 HIGH SCORES",True,(250,210,90))
        self.screen.blit(t,(WIDTH//2-t.get_width()//2,y+120))
        for i,e in enumerate(self.highscores.entries):
            new=(i==self.new_rank)
            line=f"{i+1}. {e['score']:>6}   {e['date']}" + ("  NEW!" if new else "")
            c=(120,240,120) if new else (220,220,220)
            row=self.small_font.render(line,True,c)
            self.screen.blit(row,(WIDTH//2-150,y+160+i*28))
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,y+320))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
