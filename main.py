import pygame
import json

pygame.init()
size = 800
width = size
height = size
game_over=0
level=1
lives=3
score=0
sound_coin=pygame.mixer.Sound("sounds/coin.wav")
max_level=4
sound_jump=pygame.mixer.Sound("sounds/jump.wav")
sound_game_over=pygame.mixer.Sound("sounds/game_over.wav")
def reset_level():
    player1.rect.x=100
    player1.rect.y=height-130
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    with open(f"levels/level{level}.json", "r") as file:
        world_data = json.load(file)
    return World(world_data)

def drawtext(text,x,y,color="black",size=24):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("game")
background = pygame.image.load("images/bg6.png")
bg_rect = background.get_rect()
tile_size = size / 20
with open("levels/level1.json", "r") as file:
    world_data = json.load(file)
    # print(world_data)

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img=pygame.image.load("images/lava.png")
        self.image= pygame.transform.scale(img,(tile_size,tile_size//2))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
lava_group=pygame.sprite.Group()

class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img=pygame.image.load("images/door2.png")
        self.image= pygame.transform.scale(img,(tile_size,tile_size*1.5))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
exit_group=pygame.sprite.Group()

class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img=pygame.image.load("images/coin.png")
        self.image= pygame.transform.scale(img,(tile_size//2,tile_size//2))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

coin_group=pygame.sprite.Group()



class World:
    def __init__(self, data):
        dirt_img = pygame.image.load('images/dirt.png')
        grass_img = pygame.image.load('images/grass.png')
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    images = {
                        1: dirt_img,
                        2: grass_img
                    }
                    img = pygame.transform.scale(images[tile], (tile_size, tile_size))
                    # print(img)
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = [img, img_rect]
                    self.tile_list.append(tile)
                elif tile==3:
                    lava=Lava(col_count*tile_size,
                              row_count*tile_size+(tile_size//2))
                    lava_group.add(lava)
                elif tile==5:
                    exit1=Exit(col_count*tile_size,
                              row_count*tile_size-(tile_size//2))
                    exit_group.add(exit1)
                elif tile==6:
                    coin = Coin(col_count * tile_size+(tile_size//2),
                                 row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)


                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0],tile[1])
world1=World(world_data)

class Button:
    def __init__(self,image,x,y):
        self.image=pygame.image.load(image)
        self.rect=self.image.get_rect(center=(x,y))
    def draw(self):
        action=False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
          if pygame.mouse.get_pressed()[0]==1:
              action=True

        display.blit(self.image, self.rect)
        return action

restart=Button("images/restart_btn 2.png",x=600,y=380)
start=Button("images/start_btn 2.png",x=400,y=350)
exit=Button("images/exit_btn 2.png",x=400,y=300)





class Player:
    def __init__(self, banana="images/player1.png"):
        self.gravity = 0
        self.jumped = False
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        self.ghost=pygame.image.load("images/ghost.png")
        for num in range(1, 5):
            img_right = pygame.image.load(f'images/player{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect.x = 50
        self.rect.y = height - 300

    def respawn(self):
        self.rect.x = 100
        self.rect.y = height - 130
        self.gravity = 0
        self.jumped = False

    def update(self):
        global game_over
        x = 0
        y = 0
        walk_speed = 10
        if game_over==0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -15
                self.jumped=True
                sound_jump.play()
            if key[pygame.K_LEFT]:
                x -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_RIGHT]:
                x += 5
                self.direction = 1
                self.counter += 1
            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]
            self.gravity += 1
            y += self.gravity
            if self.gravity > 10:
                self.gravity = 10
            if self.rect.bottom > height:
                self.rect.bottom = height
                self.gravity = 0

            for tile in world1.tile_list:
                if tile[1].colliderect(self.rect.x+x,self.rect.y,self.width,self.height):
                    x=0
                if tile[1].colliderect(self.rect.x, self.rect.y+y, self.width, self.height):
                    if self.gravity<0:
                        y=tile[1].bottom-self.rect.top
                        self.gravity=0
                    elif self.gravity>=0:
                        y=tile[1].top-self.rect.bottom
                        self.gravity=0
                        self.jumped=False

            self.rect.x += x

            self.rect.y += y

            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.right > width:
                self.rect.right = width

            if self.rect.top < 0:
                self.rect.top = 0
            # if pygame.sprite.spritecollide(self,lava_group,False):
            #     global lives, game_over

            if pygame.sprite.spritecollide(self, lava_group, False):
                # lives -= 1
                # if lives > 0:
                #     self.respawn()
                # else:
                    game_over = -1
                    sound_game_over.play()
            if pygame.sprite.spritecollide(self,exit_group,False):
                game_over=1
        elif game_over==-1:
            self.image=self.ghost
            if self.rect.y>=0:
                self.rect.y = self.rect.y - 4




        display.blit(self.image, self.rect)



player1 = Player()


class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_car(self):
        info = f"автомобиль {self.make} {self.model} {self.year}"
        # print(info)
        return info


car1 = Car("Toyota", "Camry", 2020)
car2 = Car("Mercedes", "amg", 2026)
car1.display_car()
car2.display_car()
main_menu=True

clock = pygame.time.Clock()
fps = 60
run = True
while run:
    clock.tick(fps)
    display.blit(background, bg_rect)
    if main_menu:
        if start.draw():
            score=0
            main_menu=False
            level=1
            lives=3
            world1=reset_level()

    else:

        world1.draw()
        drawtext(f"score: {str(score)}",10,10)
        drawtext(f"lives: {str(lives)}", 10, 40)
        coin_group.draw(display)
        lava_group.draw(display)
        lava_group.update()
        exit_group.draw(display)
        exit_group.update()
        player1.update()
        if pygame.sprite.spritecollide(player1,coin_group,True):
            score+=1
            sound_coin.play()
            print(score)
        if game_over==-1:
            if restart.draw():
                lives=lives-1
                if lives==0:
                    main_menu=True
                player1=Player()
                world1=reset_level()
                game_over=0
            if exit.draw():
                run=False
        if game_over==1:
            game_over=0
            if level<max_level:
                level+=1
                world1=reset_level()
            else:
                main_menu=True
                # pygame.quit()



    for event in pygame.event.get():
        # print(event.type, pygame.QUIT)
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
