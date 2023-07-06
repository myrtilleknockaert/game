import pygame


class SoundManager:
    def __init__(self):
        self.sounds = {
            "click": pygame.mixer.Sound("assets/sounds/click.ogg"),
            "comet": pygame.mixer.Sound("assets/sounds/meteorite.ogg"),
            "shot": pygame.mixer.Sound("assets/sounds/tir.ogg"),
            "game_over": pygame.mixer.Sound("assets/sounds/game_over.ogg"),
        }

    def play(self, name):
        self.sounds[name].play()
