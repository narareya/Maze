from pygame import *

class GameSprite(sprite.Sprite): #class untuk sprite game yang lain spt tembok dan final sprite
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): #class untuk pemain / player
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self): # untuk memasukkan bullet
        bullet = Bullet('Game/images/bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite): # class untuk enemy/musuhnya
    side = "left"
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed 
        else:
            self.rect.x += self.speed

class Bullet(GameSprite): # berisi kode untuk bullet / peluru
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self): #method untuk mengupdate
        self.rect.x += self.speed
        if self.rect.x > win_width +10:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Maze")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)

barriers = sprite.Group() # menyatukan barrier yang sudah dimasukkan dalam satu grup
bullets = sprite.Group() # menyatukan bullet/peluru dalam satu grup
monsters = sprite.Group() # menggabungkan musuh ke dalam satu grup

w1 = GameSprite('Game/images/platform2.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('Game/images/platform2_v.png', 370, 100, 50, 400)

barriers.add(w1) # menambahkan barrier 1 ke group barriers
barriers.add(w2) # menambahkan barrier 2 ke group barriers

# mengatur posisi, gambar, ukuran, dan speed dari sprite yang sudah dimasukkan
packman = Player('Game/images/hero.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('Game/images/pac-1.png', win_width - 85, win_height - 100, 80, 80)
monster1 = Enemy('Game/images/cyborg.png', win_width - 80, 180, 80, 80, 5)
monster2 = Enemy('Game/images/cyborg.png', win_width - 80, 230, 80, 80, 5)
monsters.add(monster1)
monsters.add(monster2)

finish = False
run = True

while run:
    time.delay(50)
    # untuk memasukkan event dari output ke input
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

    if not finish:
        window.fill(back)
        packman.update() # untuk mengupdate sprite packman dst.
        monsters.update()
        packman.reset()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        barriers.draw(window)
        final_sprite.reset()
        sprite.groupcollide(monsters, bullets, True, True) # jika sprite monster bertemu/bertabrakan dengan bullets keduanya akan hilang karena keduanya bernilai True
        sprite.groupcollide(bullets, barriers, True, False) # jika sprite bullets bertemu/bertabrakan dengan barriers maka bulletsnya akan hilang tetapi barriernya tidak hilang

        # kondisi menang kalah
        if sprite.spritecollide(packman, monsters, False): # jika sprite packman bersentuhan dengan sprite monsters, maka packman akan hilang dan kalah
            finish = True
            img = image.load('Game/images/game-over_1.png') # kalau kalah keluar gambar game over
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width*d, win_height)), (0,0))

        if sprite.collide_rect(packman, final_sprite): # jika sprite packman bersentuhan dengan sprite harta karun maka akan menjadi menang
            finish = True
            img = image.load('Game/images/thumb.jpg') # kalau menang keluar gambar jempol
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))

    display.update()