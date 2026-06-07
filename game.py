import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from settings import circle1,circle2,circle3,weapon1,weapon2,weapon3
from circle import Circle
from weapon import Weapon
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()

        c1 = Circle("Steve",100,100,45,circle1,5,5,100)
        c2 = Circle("Creeper",200,200,45,circle2,-5,5,100)
        c3 = Circle("Enderman",300,300,45,circle3,5,-5,100)
        c1.weapon = Weapon(c1,50,100,weapon1,0.08,0,1)
        c2.weapon = Weapon(c2,50,100,weapon2,0.08,120,1)
        c3.weapon = Weapon(c3,70,100,weapon3,0.08,240,1)

        all_circle_name = [c.name for c in Circle.all_circle]
        caption = " vs ".join(all_circle_name)
        pygame.display.set_caption(caption)

    def run(self):
        while self.running:
            self.handle_event()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        for c in Circle.all_circle:
            c.update()
            c.weapon.update()
        for i in range(len(Circle.all_circle)):
            for j in range(i+1, len(Circle.all_circle)):
                Circle.all_circle[i].check_collision(Circle.all_circle[j])
                Weapon.all_weapon[i].check_collision(Weapon.all_weapon[j])

        for i in range(len(Circle.all_circle)):
            for j in range(len(Circle.all_circle)):
                Circle.all_circle[i].check_collision2weapon(Weapon.all_weapon[j])
        self.check_game_over()

    def check_game_over(self):
        dead_circles = []
        for c in Circle.all_circle:
            if c.hp <= 0:
                dead_circles.append(c)
        for c in dead_circles:
            if c.weapon in Weapon.all_weapon:
                Weapon.all_weapon.remove(c.weapon)
            Circle.all_circle.remove(c)

        if dead_circles:
            if len(Circle.all_circle) == 1:
                winner_text = f"{Circle.all_circle[0].name} Wins!"
                self.display_game_over(winner_text)
                self.running = False
    def display_game_over(self, message):
        # Show game over screen
        self.screen.fill((0, 0, 0))  # Black background
        
        # Main message
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(text, text_rect)
        
        # "Press any key to quit" message
        small_font = pygame.font.Font(None, 36)
        sub_text = small_font.render("Press any key to quit...", True, (200, 200, 200))
        sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(sub_text, sub_rect)
        
        pygame.display.flip()
        
        # Wait for user to close or press key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False
                    self.running = False
    def draw(self):
        self.screen.fill((255,255,255))
        for c in Circle.all_circle:
            c.draw(self.screen)
            c.weapon.draw(self.screen)
        pygame.display.flip()
