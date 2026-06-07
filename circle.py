import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from weapon import Weapon

class Circle:
    all_circle = []  
    def __init__(self,name,x,y,radius,image_path,x_speed,y_speed,hp):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        original_image = pygame.image.load(image_path).convert_alpha()
        size = (radius*2,radius*2)
        self.image = pygame.transform.scale(original_image, size)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.hp = hp
        self.weapon = None
        Circle.all_circle.append(self)

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        if self.x + self.radius > SCREEN_WIDTH:     #enforce strict bound to prevent
            self.x = SCREEN_WIDTH - self.radius     #double direction change due to collision
            self.x_speed *= -1
        if self.x < self.radius:
            self.x = self.radius
            self.x_speed *= -1
        if self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.y_speed *= -1    
        if self.y < self.radius:
            self.y = self.radius
            self.y_speed *= -1    
        self.weapon.x = self.x
        self.weapon.y = self.y

    def check_collision(self,other):
        dx = self.x - other.x
        dy = self.y - other.y  
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            distance = 1
        if distance < self.radius + other.radius:
            overlap = self.radius + other.radius - distance
            self.x += dx / distance * overlap/2
            self.y += dy/distance * overlap/2
            other.x -= dx / distance * overlap/2
            other.y -= dy/distance * overlap/2

            self.x_speed, other.x_speed = other.x_speed, self.x_speed
            self.y_speed, other.y_speed = other.y_speed, self.y_speed

    def check_collision2weapon(self,weapon):
        dx = self.x - weapon.rect.centerx
        dy = self.y - weapon.rect.centery
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            distance = 1
        if distance < self.radius + weapon.width:
            self.hp -= weapon.damage


    def draw(self,screen):
        display_image = self.image.copy()

        font = pygame.font.Font(None,32)
        number_text = font.render(str(self.hp),True,(100,255,100))
        text_rect = number_text.get_rect()
        display_image.blit(number_text,text_rect.center)

        rect = self.image.get_rect()
        rect.center = (self.x, self.y)
        screen.blit(display_image, rect)