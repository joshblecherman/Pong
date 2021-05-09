import pygame
from random import (uniform, choice) 


pygame.init()

from pygame.locals import (
    K_UP, 
    K_DOWN, 
    K_s, 
    K_w, 
    K_SPACE, 
    QUIT
)

PADDLE_SPEED = 2
BALL_SPEED = 1
FRAME_RATE = 300

class Ball(pygame.sprite.Sprite): 
    def __init__(self, color, left, top): 
        pygame.sprite.Sprite.__init__(self) 
        radius = 20
        self.surface = pygame.Surface((radius * 2, radius * 2))
        self.surface.set_colorkey([255, 0, 255])
        self.surface.fill([255, 0, 255]) 
        self.rect = pygame.draw.circle(self.surface, color, (radius, radius), radius)
        self.mask = pygame.mask.from_surface(self.surface)
        self.old_rect = None 
        self.rect.x = left - radius
        self.rect.y = top - radius
        self.x_vel = None
        self.y_vel = None 
        self.x_pos = self.rect.left
        self.y_pos = self.rect.top 
    
    def start(self, pressed_keys):
        if pressed_keys[K_SPACE]: 
            signs = [-1, 1] 
            self.x_vel = BALL_SPEED * choice(signs) 
            self.y_vel = uniform(-BALL_SPEED, BALL_SPEED) 
            return True 
        return False 
        

    def move(self, screen, paddle1, paddle2, speed_factor):
        paddle_hit = 0 
        out_of_bounds = False 
        left_collision = pygame.sprite.collide_mask(paddle1, self)
        right_collision = pygame.sprite.collide_mask(paddle2, self) 
        if self.y_pos <= 5 or self.y_pos >= 710: 
            self.y_vel *= -1 
        elif left_collision or right_collision:  
            paddle_hit = 1 
            self.x_vel *= -1   
            if left_collision: 
                if left_collision[1] < 40: 
                    self.y_vel = - BALL_SPEED
                elif left_collision[1] > 80: 
                    self.y_vel = BALL_SPEED 
                else: 
                    self.y_vel = 0 
            elif right_collision: 
                if right_collision[1] < 40: 
                    self.y_vel = - BALL_SPEED
                elif right_collision[1] > 80: 
                    self.y_vel = BALL_SPEED
                else: 
                    self.y_vel = 0 
        self.x_pos += (self.x_vel * speed_factor) 
        self.y_pos += (self.y_vel * speed_factor)
        self.old_rect = self.rect.copy() 
        self.rect.topleft = self.x_pos, self.y_pos 
        screen.blit(self.surface, self.rect) 
        out_of_bounds = 1 if self.x_pos < 0 else 2 if self.x_pos > 1000 else 0 
        return paddle_hit, out_of_bounds

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, left, top): 
        pygame.sprite.Sprite.__init__(self) 
        width, height = 40, 120
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.mask = pygame.mask.from_surface(self.surface)
        self.old_rect = None 
        self.rect.x = left 
        self.rect.y = top 
        self.y_pos = self.rect.top

    def move(self, pressed_keys, keys, screen):
        dy = 0 
        l_bound, u_bound = 5, 750 - self.rect.height - 5 
        if pressed_keys[keys[0]] and self.rect.top > l_bound: 
            dy = - PADDLE_SPEED 
                
        if pressed_keys[keys[1]] and self.rect.top < u_bound: 
            dy = PADDLE_SPEED
 
        self.y_pos += dy
        self.old_rect = self.rect.copy()
        self.rect.top = self.y_pos  
        screen.blit(self.surface, self.rect)


class Main: 
    player1 = 0 
    player2 = 0 
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.height, self.width = 750, 1000
        self.screen = pygame.display.set_mode((self.width, self.height)) 
        pygame.display.set_caption("pong")
        blue = [0, 0, 255]
        red = [255, 0, 0]
        self.paddle1 = Paddle(blue, 30, self.height // 2) 
        self.paddle2 = Paddle(blue, 930, self.height // 2) 
        self.ball = Ball(red, self.width // 2, self.height // 2)
        self.speed = 1 
        self.paddle_hits = 0 
        self.round = 0 
        self.wait_for_space()
    
    def wait_for_space(self): 
        font = pygame.font.SysFont('abyssinicasil', 60) 
        text = font.render('Press Space To Begin!', True, [225, 0, 255])
        text_rect = text.get_rect() 
        text_rect.center = self.width // 2, self.height // 2 - 100
        score_string = '%s               %s' % (self.player1, self.player2)
        score = font.render(score_string, True, [255, 255, 255]) 
        score_rect = score.get_rect() 
        score_rect.center = self.width // 2, self.height // 2 - 300 
        waiting = True 
        while waiting: 
            self.screen.fill([0, 0, 0])
            self.screen.blit(self.paddle1.surface, self.paddle1.rect) 
            self.screen.blit(self.paddle2.surface, self.paddle2.rect) 
            self.screen.blit(self.ball.surface, self.ball.rect) 
            self.screen.blit(text, text_rect)
            self.screen.blit(score, score_rect) 
            for event in pygame.event.get():
                if event.type == QUIT: 
                    pygame.quit()
            pressed_keys = pygame.key.get_pressed()
            if self.ball.start(pressed_keys): 
                waiting = False 
                text.fill([0, 0, 0])
                self.screen.blit(text, text_rect)
                score.fill([0, 0, 0])
                self.screen.blit(score, score_rect)
            pygame.display.update()
            self.clock.tick(FRAME_RATE) 
        self.loop() 

    def loop(self): 
        running = True
        while running:
            self.screen.fill([0, 0, 0]) 
            for event in pygame.event.get():
                if event.type == QUIT: 
                    pygame.quit() 
            pressed_keys = pygame.key.get_pressed()
            self.paddle1.move(pressed_keys, [K_w, K_s], self.screen)
            self.paddle2.move(pressed_keys, [K_UP, K_DOWN], self.screen)
            ball_info = self.ball.move(self.screen, self.paddle1, self.paddle2, self.speed)
            self.paddle_hits += ball_info[0]
            running = False if (ball_info[1] == 1 or ball_info[1] == 2) else True 
            if self.paddle_hits // 10 > self.round: 
                self.speed *= 1.5 
                self.round += 1
            updates = [self.paddle1.rect, 
                       self.paddle1.old_rect,
                       self.paddle2.rect,
                       self.paddle2.old_rect, 
                       self.ball.rect, 
                       self.ball.old_rect]
            pygame.display.update(updates)
            self.clock.tick(FRAME_RATE)
        if ball_info[1] == 1: 
            Main.player2 += 1 
        else: 
            Main.player1 += 1 
        self.__init__() 

Main()