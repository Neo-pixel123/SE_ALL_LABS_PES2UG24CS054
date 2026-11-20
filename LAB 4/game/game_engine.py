import pygame
import random
from game.player import Player,LANE_W
from game.traffic import Car,make_car
from game.river import River
from game.highscores import load_scores,add_score
from game.lighting import DayNight,draw_icon

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
BG=(60,60,60)

START_LIVES=3
INVULN_FRAMES=90          # 1.5 s of blink/immunity after losing a life
START_X=(LANES//2)*LANE_W+LANE_W//2   # centre of a lane (WIDTH//2 sat on a lane line)
START_Y=HEIGHT-80
RIVER_TOP,RIVER_H=250,80

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.small_font=pygame.font.SysFont("monospace",20,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.reset()

    def reset(self):
        self.player=Player(START_X,START_Y)
        self.lives=START_LIVES
        self.invuln=0
        self.toast=("",0)
        self.cars=[]
        self.river=River(RIVER_TOP,RIVER_H,WIDTH)
        self.carry=0.0
        self.was_in_river=False
        self.daynight=DayNight()
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.game_over=False
        self.won=False
        self.scores_saved=False
        self.high_scores=load_scores()
        self.new_rank=None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    # --- Task 1: lives -------------------------------------------------
    def lose_life(self,reason):
        self.lives-=1
        self.toast=(reason,60)
        if self.lives<=0:
            self.game_over=True
            return
        self.player=Player(START_X,START_Y)
        self.carry=0.0
        self.was_in_river=False
        self.invuln=INVULN_FRAMES

    # --- Task 3: save score once when the run ends ---------------------
    def finish(self):
        if self.scores_saved: return
        self.scores_saved=True
        self.high_scores,self.new_rank=add_score(self.score//10)

    def update(self):
        if self.game_over or self.won:
            self.finish()
            return
        self.daynight.update()
        keys=pygame.key.get_pressed()
        self.player.move(keys,0,WIDTH,START_Y-30)  # can't back off the bottom sidewalk
        self.timer+=1
        if self.timer>=self.spawn_interval:
            lane=random.randint(0,LANES-1)
            self.cars.append(make_car(lane,HEIGHT,self.speed))
            self.timer=0
            self.spawn_interval=max(22,self.spawn_interval-0.2)
        if self.invuln>0: self.invuln-=1
        if self.toast[1]>0: self.toast=(self.toast[0],self.toast[1]-1)

        # --- Task 2: river row, must ride a log -------------------------
        self.river.update()
        in_river=self.river.contains(self.player.rect)
        if in_river:
            log=self.river.log_under(self.player.rect)
            if log is None:
                self.lose_life("SPLASH!")
                in_river=False
            else:
                self.carry+=self.river.velocity
                step=int(self.carry)
                self.carry-=step
                self.player.rect.x+=step
                if self.player.rect.left<0 or self.player.rect.right>WIDTH:
                    self.lose_life("SWEPT AWAY!")
                    in_river=False
        elif self.was_in_river:
            self.player.snap_to_lane(WIDTH)   # hopped off the log: back onto the lane grid
            self.carry=0.0
        self.was_in_river=in_river

        # cars pass under the river (culvert), so they can't hit you on the log
        for c in self.cars:
            c.update()
            if not in_river and self.invuln==0 and not self.game_over and c.rect.colliderect(self.player.rect):
                self.lose_life("HIT!")
        self.cars=[c for c in self.cars if not c.off_screen(HEIGHT)]
        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)
        if self.player.rect.top<=10 and not self.game_over:
            self.won=True

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
        self.river.draw(self.screen,self.daynight.t)
        if self.invuln==0 or (self.invuln//6)%2==0:
            self.player.draw(self.screen)
        # --- Task 4: night overlay with long headlight beams ---------------
        self.daynight.draw(self.screen,self.cars,self.player.rect)
        if self.toast[1]>0 and not self.game_over:
            t=self.big_font.render(self.toast[0],True,(255,90,90))
            self.screen.blit(t,(WIDTH//2-t.get_width()//2,HEIGHT//2-120))
        hud=pygame.Rect(0,0,WIDTH,30)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        s=self.font.render(f"Score: {self.score//10}  Lives: {self.lives}  Goal: top  R=Restart",True,(220,220,220))
        self.screen.blit(s,(6,4))
        draw_icon(self.screen,WIDTH-16,15,self.daynight.is_night)
        if self.game_over:
            self._msg("GAME OVER",(220,60,60))
        if self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,170))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        sub=self.font.render(f"Score: {self.score//10}   Press R to Restart",True,(200,200,200))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-150))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,HEIGHT//2-90))
        title=self.font.render("TOP 5",True,(240,200,80))
        self.screen.blit(title,(WIDTH//2-title.get_width()//2,HEIGHT//2-40))
        for i,e in enumerate(self.high_scores):
            mine=(i==self.new_rank)
            line=f"{i+1}. {e['score']:>5}   {e['date']}" + ("  NEW!" if mine else "")
            r=self.small_font.render(line,True,(120,240,120) if mine else (220,220,220))
            self.screen.blit(r,(WIDTH//2-150,HEIGHT//2+i*30))
        if not self.high_scores:
            r=self.small_font.render("(no scores yet)",True,(160,160,160))
            self.screen.blit(r,(WIDTH//2-r.get_width()//2,HEIGHT//2))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
