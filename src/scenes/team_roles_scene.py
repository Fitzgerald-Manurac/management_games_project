"""Game 5: Team Role Matching (task/empleyado -> tamang departamento)."""

import random

import pygame

from entities.button import Button
from entities.dept_logo import draw_dept_logo
from scenes.base_scene import Scene
from settings import (ACCENT, BAD, BG, GOLD, GOOD, MUTED, PANEL,
                      ROLE_CORRECT_POINTS, ROLE_FEEDBACK_DELAY,
                      ROLE_TASKS_PER_ROUND, TEXT, WIDTH)
from utils.data import ROLE_DEPARTMENTS, ROLE_TASKS, filter_by_lesson
from utils.helpers import draw_text, draw_wrapped, get_font

CARD_RECT = (120, 130, 760, 150)
DEPT_W, DEPT_H, DEPT_GAP = 520, 56, 12
DEPT_Y = 312


class TeamRolesScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.back_btn = Button((WIDTH - 130, 18, 110, 44), "Back", lambda: game.change_scene("menu"), bg=PANEL, fg=TEXT, size=20)
        self.restart_btn = Button((WIDTH - 255, 18, 115, 44), "Restart", self.new_round, bg=GOLD, size=20)

        cx = WIDTH // 2
        self.dept_buttons = []
        for i, dept in enumerate(ROLE_DEPARTMENTS):
            rect = (cx - DEPT_W // 2, DEPT_Y + i * (DEPT_H + DEPT_GAP), DEPT_W, DEPT_H)
            icon = lambda surface, box, d=dept: draw_dept_logo(surface, d, box)
            self.dept_buttons.append(Button(rect, dept, lambda d=dept: self.assign(d), bg=(76, 198, 190), size=24, icon=icon))

        self.new_round()

    def new_round(self):
        pool = filter_by_lesson(ROLE_TASKS, self.game.lesson)
        if not pool:
            pool = list(ROLE_TASKS)
        self.tasks = random.sample(pool, min(ROLE_TASKS_PER_ROUND, len(pool)))
        self.index = 0
        self.correct = 0
        self.wrong = 0
        self.feedback = ""
        self.feedback_color = TEXT
        self.feedback_dept = None
        self.feedback_ok = False
        self.feedback_timer = 0
        self.finished = False

    def current_task(self):
        if self.finished or self.index >= len(self.tasks):
            return None
        return self.tasks[self.index]

    def assign(self, dept):
        task = self.current_task()
        if task is None or self.feedback_timer > 0:
            return
        answer = task[1]
        self.feedback_dept = dept
        if dept == answer:
            self.correct += 1
            self.feedback_ok = True
            self.feedback = "Correct! Good delegation."
            self.feedback_color = GOOD
            self.game.add_score(ROLE_CORRECT_POINTS)
            self.game.sound.play_correct()
        else:
            self.wrong += 1
            self.feedback_ok = False
            self.feedback = f"Wrong. {answer} should handle this."
            self.feedback_color = BAD
            self.game.sound.play_error()
        self.feedback_timer = ROLE_FEEDBACK_DELAY

    def next_task(self):
        self.index += 1
        self.feedback = ""
        self.feedback_dept = None
        if self.index >= len(self.tasks):
            self.finished = True
            if self.correct > self.wrong:
                self.game.sound.play_win()
            else:
                self.game.sound.play_lose()

    def handle_event(self, event):
        if self.back_btn.handle_event(event) or self.restart_btn.handle_event(event):
            return
        if self.finished or self.feedback_timer > 0:
            return
        for btn in self.dept_buttons:
            if btn.handle_event(event):
                return

    def update(self, dt):
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.feedback_timer = 0
                self.next_task()

    def dept_color(self, dept):
        if self.feedback_dept is None:
            return (76, 198, 190)
        task = self.current_task()
        if task is not None and dept == task[1]:
            return GOOD
        if dept == self.feedback_dept:
            return BAD
        return PANEL

    def draw(self, surface):
        surface.fill(BG)
        draw_text(surface, "Team Role Matching", get_font(34, True), ACCENT, (30, 14))
        draw_text(surface, "Organizing, Delegation and Structure: who should handle the task?", get_font(18), TEXT, (32, 66))
        stats = f"Task: {min(self.index + 1, len(self.tasks))}/{len(self.tasks)}    Correct: {self.correct}    Wrong: {self.wrong}    Score: {self.game.total_score}"
        draw_text(surface, stats, get_font(20, True), GOLD, (WIDTH - 20, 88), "topright")

        card = pygame.Rect(CARD_RECT)
        pygame.draw.rect(surface, PANEL, card, border_radius=10)
        pygame.draw.rect(surface, ACCENT, card, 3, border_radius=10)
        task = self.current_task()
        if task is not None:
            draw_text(surface, "Who should handle this?", get_font(20, True), MUTED, (card.centerx, card.y + 18), "midtop")
            body = card.inflate(-60, -70).move(0, 14)
            draw_wrapped(surface, task[0], get_font(26, True), TEXT, body)
        else:
            draw_wrapped(surface, "Round finished.", get_font(26, True), MUTED, card)

        for btn in self.dept_buttons:
            color = self.dept_color(btn.text)
            btn.bg = color
            btn.hover_color = GOLD if self.feedback_dept is None else color
            btn.draw(surface)

        if self.feedback:
            draw_text(surface, self.feedback, get_font(22, True), self.feedback_color, (WIDTH // 2, 660), "center")

        self.back_btn.draw(surface)
        self.restart_btn.draw(surface)

        if self.finished:
            overlay = pygame.Surface((600, 190), pygame.SRCALPHA)
            overlay.fill((16, 32, 46, 235))
            rect = overlay.get_rect(center=(WIDTH // 2, 420))
            surface.blit(overlay, rect)
            pygame.draw.rect(surface, ACCENT, rect, 3, border_radius=6)
            draw_text(surface, "Round Complete!", get_font(38, True), GOLD, (rect.centerx, rect.y + 45), "center")
            draw_text(surface, f"Correct: {self.correct}/{len(self.tasks)}   Wrong: {self.wrong}", get_font(24), TEXT, (rect.centerx, rect.y + 100), "center")
            draw_text(surface, "Press Restart for a new set", get_font(18), MUTED, (rect.centerx, rect.y + 150), "center")
