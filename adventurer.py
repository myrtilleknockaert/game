import pygame
from pygame import mixer
import random

pygame.init()
mixer.init()
pygame.mixer.set_num_channels(32)

pygame.display.set_caption("Jeu du Pic'asso")
screen = pygame.display.set_mode((1080, 450))


class SmokeCloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames = 0
        self.mean_radius = 10
        self.circles = [
            [
                self.mean_radius * 50 + random.randint(0, self.mean_radius * 4),  # x
                self.mean_radius * 50 + random.randint(0, self.mean_radius * 4),  # y
                random.randint(0, self.mean_radius),  # radius
                [200, 200, 200, 128],  # color
            ]
            for _ in range(20)
        ]
        self.dead = False

    def get_sprite(self):
        surface = pygame.Surface(
            (self.mean_radius * 100, self.mean_radius * 100), pygame.SRCALPHA
        )
        for circle in self.circles:
            pygame.draw.circle(
                surface,
                circle[3],
                (circle[0], circle[1]),
                circle[2],
            )
        return surface

    def blit(self, screen):
        screen.blit(
            self.get_sprite(),
            (self.x - self.mean_radius * 100 / 2, self.y - self.mean_radius * 100 / 2),
        )

    def animate(self):
        self.frames += 1
        # reduce radius and opacity
        for circle in self.circles:
            circle[2] -= 0.5
            circle[3][3] -= 1
        if all([circle[2] <= 0 or circle[3][3] <= 0 for circle in self.circles]):
            self.dead = True


class FX:
    def __init__(self):
        self.smoke_clouds = []

    def animate(self):
        for smoke_cloud in self.smoke_clouds:
            smoke_cloud.animate()
            if smoke_cloud.dead:
                self.smoke_clouds.remove(smoke_cloud)

    def blit(self, screen):
        for smoke_cloud in self.smoke_clouds:
            smoke_cloud.blit(screen)

    def add_smoke(self, x, y):
        self.smoke_clouds.append(SmokeCloud(x, y))

    def move_all(self, dx):
        for smoke_cloud in self.smoke_clouds:
            smoke_cloud.x += dx


class Adventurer:
    def __init__(self):
        self.animations = {
            "idle": {
                "left": [
                    pygame.transform.flip(
                        pygame.transform.scale_by(
                            pygame.image.load(
                                f"assets/adventurer/adventurer-idle-{i:02d}.png"
                            ),
                            4,
                        ),
                        flip_x=1,
                        flip_y=0,
                    )
                    for i in range(4)
                ],
                "right": [
                    pygame.transform.scale_by(
                        pygame.image.load(
                            f"assets/adventurer/adventurer-idle-{i:02d}.png"
                        ),
                        4,
                    )
                    for i in range(4)
                ],
            },
            "running": {
                "left": [
                    pygame.transform.flip(
                        pygame.transform.scale_by(
                            pygame.image.load(
                                f"assets/adventurer/adventurer-run-{i:02d}.png"
                            ),
                            4,
                        ),
                        flip_x=1,
                        flip_y=0,
                    )
                    for i in range(6)
                ],
                "right": [
                    pygame.transform.scale_by(
                        pygame.image.load(
                            f"assets/adventurer/adventurer-run-{i:02d}.png"
                        ),
                        4,
                    )
                    for i in range(6)
                ],
            },
            "jumping": {
                "left": [
                    pygame.transform.flip(
                        pygame.transform.scale_by(
                            pygame.image.load(
                                f"assets/adventurer/adventurer-jump-{i:02d}.png"
                            ),
                            4,
                        ),
                        flip_x=1,
                        flip_y=0,
                    )
                    for i in range(4)
                ],
                "right": [
                    pygame.transform.scale_by(
                        pygame.image.load(
                            f"assets/adventurer/adventurer-jump-{i:02d}.png"
                        ),
                        4,
                    )
                    for i in range(4)
                ],
            },
            "falling": {
                "left": [
                    pygame.transform.flip(
                        pygame.transform.scale_by(
                            pygame.image.load(
                                f"assets/adventurer/adventurer-fall-{i:02d}.png"
                            ),
                            4,
                        ),
                        flip_x=1,
                        flip_y=0,
                    )
                    for i in range(2)
                ],
                "right": [
                    pygame.transform.scale_by(
                        pygame.image.load(
                            f"assets/adventurer/adventurer-fall-{i:02d}.png"
                        ),
                        4,
                    )
                    for i in range(2)
                ],
            },
            "crouching": {
                "left": [
                    pygame.transform.flip(
                        pygame.transform.scale_by(
                            pygame.image.load(
                                f"assets/adventurer/adventurer-crouch-{i:02d}.png"
                            ),
                            4,
                        ),
                        flip_x=1,
                        flip_y=0,
                    )
                    for i in range(4)
                ],
                "right": [
                    pygame.transform.scale_by(
                        pygame.image.load(
                            f"assets/adventurer/adventurer-crouch-{i:02d}.png"
                        ),
                        4,
                    )
                    for i in range(4)
                ],
            },
        }
        self.animation_durations = {
            "idle": 10,
            "running": 5,
            "jumping": 5,
            "falling": 5,
            "crouching": 10,
        }
        self.animation = "idle"
        self.last_animation = self.animation
        self.direction = "right"
        self.sprite_index = 0
        self.frames_on_sprite = 0
        self.y = 0
        self.y_velocity = 0

    def get_sprite(self) -> pygame.Surface:
        return self.animations[self.animation][self.direction][self.sprite_index]

    def animate(self):
        self.frames_on_sprite += 1
        if self.frames_on_sprite >= self.animation_durations[self.animation]:
            self.sprite_index = (self.sprite_index + 1) % len(
                self.animations[self.animation][self.direction]
            )
            self.frames_on_sprite = 0

        # compute new y position
        if self.y + self.y_velocity < 0:
            if self.y_velocity < 0 and self.y_velocity + 1 == 0:
                self.animation = "falling"
                self.sprite_index = 0
                self.frames_on_sprite = 0
            self.y_velocity += 1
            self.y += self.y_velocity
            if self.y == 0:
                self.y_velocity = 0
                self.animation = self.last_animation
                self.sprite_index = 0
                self.frames_on_sprite = 0

    def jump(self) -> bool:
        if self.y != 0:
            return False
        self.last_animation = self.animation
        self.animation = "jumping"
        self.sprite_index = 0
        self.frames_on_sprite = 0
        self.y_velocity = -20
        return True


class MusicAnnouncer:
    def __init__(self):
        self.current_song = ""
        self.banner_displayed = False
        self.font = pygame.font.Font("assets/fonts/joystix monospace.otf", 16)
        self.title_font = pygame.font.Font("assets/fonts/ARCADECLASSIC.TTF", 32)
        self.banner_sprite = pygame.transform.scale_by(
            pygame.image.load("assets/song_banner.png"), 10
        )
        self.frames_on_banner = 0
        self.show_time = 120
        self.out_animation_t = 0

    def announce(self, song):
        self.current_song = song
        self.banner_displayed = True

    def blit(self, screen):
        if not self.banner_displayed:
            return
        screen.blit(self.banner_sprite, (1080 - 300 + self.out_animation_t, 0))
        text = self.font.render(self.current_song, True, (255, 255, 255))
        title = self.title_font.render("Now Playing", True, (255, 255, 255))
        screen.blit(text, (1080 - 300 + 40 + self.out_animation_t, 60))
        screen.blit(title, (1080 - 300 + 100 + self.out_animation_t, 20))
        self.frames_on_banner += 1
        if self.frames_on_banner >= self.show_time:
            self.out_animation_t += 4
        if self.out_animation_t >= 300:
            self.banner_displayed = False
            self.frames_on_banner = 0
            self.out_animation_t = 0


background = pygame.image.load("assets/adventurer_bg.png")
foreground = pygame.image.load("assets/adventurer_fg.png")

songs = [
    "1991 - Full Send",
    "Flume ft. Vera Blue - Rushing Back (Ekko & Sidetrack Bootleg)",
    "Maduk - Colours (ft. Diamond Eyes)",
    "Metrik - Gravity",
]
song_durations = {
    "1991 - Full Send": 180,
}
song_index = random.randint(0, len(songs) - 1)

running = True
clock = pygame.time.Clock()
adventurer = Adventurer()
fx = FX()
background_pos = 0
foreground_pos = 0
speed = 0
# start background music
mixer.music.load(f"assets/sounds/music/{songs[song_index]}.mp3")
mixer.music.play()
mixer.music.set_volume(0.1)
ma = MusicAnnouncer()
ma.announce(songs[song_index])

while running:
    screen.fill((100, 100, 100))
    # blit background three times for infinite scrolling
    screen.blit(background, (background_pos, 0))
    screen.blit(background, (background_pos + background.get_width(), 0))
    screen.blit(background, (background_pos - background.get_width(), 0))

    # blit black veil with opacity 128
    veil = pygame.Surface((1080, 450))
    veil.set_alpha(100)
    screen.blit(veil, (0, 0))

    # blit foreground three times for infinite scrolling
    screen.blit(foreground, (foreground_pos, 50))
    screen.blit(foreground, (foreground_pos + foreground.get_width(), 50))
    screen.blit(foreground, (foreground_pos - foreground.get_width(), 50))

    # blit adventurer
    screen.blit(adventurer.get_sprite(), (300, 250 + adventurer.y))

    # blit fx
    fx.blit(screen)

    # blit music announcer
    ma.blit(screen)

    # animate adventurer, fx and background
    adventurer.animate()
    fx.animate()
    background_pos -= speed
    foreground_pos -= speed * 8
    fx.move_all(-speed * 8)

    # reset background and foreground position
    if (
        background_pos <= -background.get_width()
        or background_pos >= background.get_width()
    ):
        background_pos = 0
    if (
        foreground_pos <= -foreground.get_width()
        or foreground_pos >= foreground.get_width()
    ):
        foreground_pos = 0

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_RIGHT, pygame.K_LEFT}:
                adventurer.animation = "running"
                adventurer.direction = (
                    "right" if event.key == pygame.K_RIGHT else "left"
                )
                adventurer.sprite_index = 0
                adventurer.frames_on_sprite = 0
                speed = 1 if event.key == pygame.K_RIGHT else -1
            elif event.key == pygame.K_UP:
                if adventurer.jump():
                    fx.add_smoke(
                        300 + adventurer.get_sprite().get_width() / 2 - 20,
                        250 + adventurer.get_sprite().get_height() - 30,
                    )
            elif event.key == pygame.K_DOWN:
                if adventurer.y == 0:
                    adventurer.animation = "crouching"
                    adventurer.sprite_index = 0
                    adventurer.frames_on_sprite = 0
                    speed = 0
        elif event.type == pygame.KEYUP:
            if event.key in {pygame.K_RIGHT, pygame.K_LEFT}:
                adventurer.animation = "idle"
                adventurer.sprite_index = 0
                adventurer.frames_on_sprite = 0
                speed = 0
            if event.key == pygame.K_DOWN and adventurer.animation == "crouching":
                adventurer.animation = "idle"
                adventurer.sprite_index = 0
                adventurer.frames_on_sprite = 0

    clock.tick(60)
