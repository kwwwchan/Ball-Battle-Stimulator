import pygame
import math
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Weapon:
    all_weapon = []
    
    def __init__(self,circle,width,length,image_path,r_speed,angle,damage):
        self.circle = circle
        self.width = width
        self.length = length
        self.r_speed = r_speed
        self.angle = angle
        self.damage = damage
        
        original_image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(original_image, (length,width))
        self.image = self.scaled_image
        self.rect = self.image.get_rect()   
        self.update_position()
        
        Weapon.all_weapon.append(self)

    def update_position(self): 
        self.image = pygame.transform.rotate(self.scaled_image,-math.degrees(self.angle))
        self.rect = self.image.get_rect()
        self.rect.center = (self.circle.x + (self.circle.radius + self.length) * math.cos(self.angle),
                             self.circle.y + (self.circle.radius + self.width)* math.sin(self.angle))
       

    def update(self):
        if self.angle > 2*math.pi:
            self.angle %= 2*math.pi
        self.angle += self.r_speed
        self.update_position()

    def check_collision(self,other):
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery  
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            distance = 1
        if distance < self.width + other.width:
            overlap = self.width + other.width - distance
            self.rect.centerx += dx / distance * overlap/2
            self.rect.centery += dy/distance * overlap/2
            other.rect.centerx -= dx / distance * overlap/2
            other.rect.centery -= dy/distance * overlap/2


            self.circle.x_speed, other.circle.x_speed = other.circle.x_speed, self.circle.x_speed
            self.circle.y_speed, other.circle.y_speed = other.circle.y_speed, self.circle.y_speed
            self.r_speed *= -1
            other.r_speed *= -1

    def draw(self,screen):
        screen.blit(self.image,self.rect)