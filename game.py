from superwires import games, color
import pygame
import random

class Pan(games.Sprite):

    def __init__(self, image):
        super().__init__(image, x = games.mouse.x, bottom = games.screen.height)
        self.score = games.Text(value = 0, size = 25, color = color.black, top = 5, right = games.screen.width - 10)
        games.screen.add(self.score)
    
    def update(self):
        self.x = games.mouse.x
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        self.check_catch()
    
    def check_catch(self):
        for pizza in self.overlapping_sprites:
            self.score.value += 10
            self.score.right = games.screen.width - 10
            pizza.handle_catch()

class Pizza(games.Sprite):
    
    speed = 1.5
    def __init__(self, x, y = 90):
        image = games.load_image("pizza.png")
        image = pygame.transform.scale(image, (100, 100))
        super().__init__(image = image, x = x, y = y, dy = Pizza.speed)
    
    def update(self):
        if self.bottom > games.screen.height:
            self.end_game()
            self.destroy()
    
    def handle_catch(self):
        # self.end_game()
        self.destroy()
    
    def end_game(self):
        end_message = games.Message(value = "Game Over", size = 90, color = color.red, x = games.screen.width/2, y = games.screen.height/2, lifetime = 250, after_death = games.screen.quit)
        games.screen.add(end_message)

class Chef(games.Sprite):

    def __init__(self, y = 55, speed = 2, odds_change = 200):
        image = games.load_image("chef.png")
        image = pygame.transform.scale(image, (300, 235))
        super().__init__(image = image, x = games.screen.width/2, y = y, dx= speed)
        self.odds_change = odds_change
        self.time_til_drop = 0
    
    def update(self):
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx
        self.check_drop()
    
    def check_drop(self):
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_pizza = Pizza(x = self.x)
            games.screen.add(new_pizza)
            self.time_til_drop = int(new_pizza.height * 1.3 / Pizza.speed) + 1


def main():
    # games.init(screen_width = 368, screen_height = 480, fps = 50)
    games.init(screen_width = 368*2, screen_height = 480, fps = 50, )
    wall_image = games.load_image("wall1.jpg", transparent = False)
    games.screen.background = wall_image
    the_chef = Chef()
    games.screen.add(the_chef)
    image = games.load_image("pan.png")
    image = pygame.transform.scale(image, (120, 120))
    the_pan = Pan(image=image)
    games.screen.add(the_pan)
    games.mouse.is_visible = False
    games.screen.event_grab = True
    games.screen.mainloop()

main()