"""Main menu: pumili ng lesson at ng laro."""

import pygame

from entities.button import Button
from scenes.base_scene import Scene
from settings import ACCENT, BG, GOLD, MUTED, PANEL, TEXT, WIDTH
from utils.data import LESSON_NAMES
from utils.helpers import draw_text, draw_wrapped, get_font


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        cx = WIDTH // 2
        self.sound_btn = Button((cx + 170, 170, 170, 44), "Sound: On", lambda: game.toggle_sound(), bg=PANEL, fg=TEXT, size=20)
        self.reset_btn = Button((cx - 95, 190, 190, 44), "Reset Score", lambda: game.reset_scores(), bg=(96, 112, 128), fg=TEXT, size=20)
        self.buttons = [
            self.sound_btn,
            self.reset_btn,
            Button((cx - 210, 262, 420, 58), "Memory Match", lambda: game.change_scene("memory"), bg=(76, 198, 190), fg=(10, 27, 38), size=28),
            Button((cx - 210, 332, 420, 58), "Sliding Puzzle", lambda: game.change_scene("sliding"), bg=(76, 198, 190), fg=(10, 27, 38), size=28),
            Button((cx - 210, 402, 420, 58), "Team Role Matching", lambda: game.change_scene("roles"), bg=(76, 198, 190), fg=(10, 27, 38), size=28),
            Button((cx - 210, 472, 420, 58), "Word Scramble", lambda: game.change_scene("scramble"), bg=(76, 198, 190), fg=(10, 27, 38), size=28),
            Button((cx - 210, 542, 420, 58), "Hangman", lambda: game.change_scene("hangman"), bg=(76, 198, 190), fg=(10, 27, 38), size=28),
            Button((cx - 210, 618, 420, 52), "Exit", game.quit, bg=PANEL, fg=TEXT, size=22),
        ]

    def lesson_label(self):
        return "All Lessons (1-4)"

    def handle_event(self, event):
        for btn in self.buttons:
            if btn.handle_event(event):
                return

    def draw(self, surface):
        surface.fill(BG)
        cx = WIDTH // 2

        self.sound_btn.text = "Sound: On" if self.game.sound.enabled else "Sound: Off"
        self.sound_btn.bg = GOLD if self.game.sound.enabled else PANEL

        draw_text(surface, "Management and Organization Concepts", get_font(40, True), (70, 214, 208), (cx, 70), "center")
        draw_text(surface, "Review Games", get_font(26), (255, 191, 105), (cx, 122), "center")
        draw_text(surface, f"Total Score: {self.game.total_score}   Best: {self.game.best_score}", get_font(22, True), (255, 191, 105), (cx, 165), "center")
        draw_text(surface, "Tip: Press F11 or use the window buttons to switch display mode. The window can also be resized.", get_font(16), MUTED, (cx, 698), "center")

        for btn in self.buttons:
            btn.draw(surface)
