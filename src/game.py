"""Main Game class: window, loop, at scene manager."""

import json
import os

import pygame

from scenes.hangman_scene import HangmanScene
from scenes.memory_scene import MemoryScene
from scenes.menu_scene import MenuScene
from scenes.scramble_scene import ScrambleScene
from scenes.sliding_puzzle_scene import SlidingPuzzleScene
from scenes.team_roles_scene import TeamRolesScene
from settings import FPS, HEIGHT, TITLE, WIDTH
from utils.audio import AudioManager
from utils.helpers import set_mouse_transform

LEADERBOARD_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "leaderboard.json")

SCENES = {
    "menu": MenuScene,
    "memory": MemoryScene,
    "scramble": ScrambleScene,
    "hangman": HangmanScene,
    "sliding": SlidingPuzzleScene,
    "roles": TeamRolesScene,
}


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.fullscreen = False
        self.windowed_size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.windowed_size, pygame.RESIZABLE)
        # Lahat ng scene ay gumuguhit sa fixed na canvas; ito ang ini-scale sa window.
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.view_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.view_scale = 1.0
        self._update_viewport()
        set_mouse_transform(self.to_canvas)
        self.clock = pygame.time.Clock()
        self.running = True

        # Combined lesson mode: lahat ng lesson na isang set
        self.lesson_options = [None]
        self.lesson_index = 0
        self.total_score = 0
        self.best_score = 0
        self.leaderboard = self.load_leaderboard()
        self.sound = AudioManager()
        self.sound.play_background_music()

        self.scene = None
        self.change_scene("menu")

    def load_leaderboard(self):
        try:
            with open(LEADERBOARD_PATH, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, list):
                return sorted(data, key=lambda item: item.get("score", 0), reverse=True)[:5]
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return []

    def save_leaderboard(self):
        with open(LEADERBOARD_PATH, "w", encoding="utf-8") as fh:
            json.dump(self.leaderboard, fh)

    def sync_leaderboard(self):
        if self.best_score <= 0:
            return
        entry = {"name": "Player", "score": self.best_score}
        scores = self.leaderboard + [entry]
        self.leaderboard = sorted(scores, key=lambda item: item.get("score", 0), reverse=True)[:5]
        self.save_leaderboard()

    @property
    def lesson(self):
        return self.lesson_options[self.lesson_index]

    def add_score(self, points):
        self.total_score += points
        if self.total_score > self.best_score:
            self.best_score = self.total_score
            self.sync_leaderboard()
        return self.total_score

    def reset_scores(self):
        self.total_score = 0
        self.best_score = 0
        self.leaderboard = []
        self.save_leaderboard()

    def toggle_sound(self):
        self.sound.toggle()
        return self.sound.enabled

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.windowed_size, pygame.RESIZABLE)
            self.fullscreen = False
        else:
            self.windowed_size = self.screen.get_size()
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            self.fullscreen = True
        self._update_viewport()
        return self.fullscreen

    # ---------- scaling ng window ----------

    def _update_viewport(self):
        """Panatilihin ang 1000x720 aspect ratio sa loob ng kasalukuyang window."""
        win_w, win_h = self.screen.get_size()
        self.view_scale = min(win_w / WIDTH, win_h / HEIGHT)
        view_w = max(1, int(WIDTH * self.view_scale))
        view_h = max(1, int(HEIGHT * self.view_scale))
        self.view_rect = pygame.Rect((win_w - view_w) // 2, (win_h - view_h) // 2, view_w, view_h)

    def to_canvas(self, pos):
        """Window coords -> canvas coords para tama pa rin ang pag-click."""
        if self.view_scale <= 0:
            return pos
        x = (pos[0] - self.view_rect.x) / self.view_scale
        y = (pos[1] - self.view_rect.y) / self.view_scale
        return int(x), int(y)

    def _scaled_event(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            attrs = dict(event.__dict__)
            attrs["pos"] = self.to_canvas(event.pos)
            if "rel" in attrs and self.view_scale > 0:
                rel = attrs["rel"]
                attrs["rel"] = (int(rel[0] / self.view_scale), int(rel[1] / self.view_scale))
            return pygame.event.Event(event.type, attrs)
        return event

    def change_scene(self, name):
        self.scene = SCENES[name](self)

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.windowed_size = (max(400, event.w), max(288, event.h))
                        self.screen = pygame.display.set_mode(self.windowed_size, pygame.RESIZABLE)
                    self._update_viewport()
                else:
                    self.scene.handle_event(self._scaled_event(event))
            self.scene.update(dt)
            self.scene.draw(self.canvas)
            self.screen.fill((0, 0, 0))
            if self.view_rect.size == (WIDTH, HEIGHT):
                self.screen.blit(self.canvas, self.view_rect)
            else:
                self.screen.blit(pygame.transform.smoothscale(self.canvas, self.view_rect.size), self.view_rect)
            pygame.display.flip()
        pygame.quit()
