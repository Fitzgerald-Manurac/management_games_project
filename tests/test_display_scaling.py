import os
import sys
import unittest

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import pygame

from game import Game
from settings import HEIGHT, WIDTH


class FakeScreen:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size


def make_game(window_size):
    """Game na walang display - ang viewport math lang ang sinusubok."""
    game = Game.__new__(Game)
    game.fullscreen = False
    game.windowed_size = (WIDTH, HEIGHT)
    game.screen = FakeScreen(window_size)
    game.view_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    game.view_scale = 1.0
    game._update_viewport()
    return game


class ViewportTests(unittest.TestCase):
    def test_default_window_is_one_to_one(self):
        game = make_game((WIDTH, HEIGHT))

        self.assertEqual(game.view_scale, 1.0)
        self.assertEqual(game.view_rect, pygame.Rect(0, 0, WIDTH, HEIGHT))
        self.assertEqual(game.to_canvas((250, 300)), (250, 300))

    def test_wide_screen_is_letterboxed_on_the_sides(self):
        game = make_game((1920, 1080))

        self.assertEqual(game.view_rect.height, 1080)
        self.assertLess(game.view_rect.width, 1920)
        self.assertEqual(game.view_rect.centerx, 960)

    def test_tall_screen_is_letterboxed_top_and_bottom(self):
        game = make_game((1000, 1200))

        self.assertEqual(game.view_rect.width, 1000)
        self.assertLess(game.view_rect.height, 1200)
        self.assertEqual(game.view_rect.centery, 600)

    def test_centre_of_the_view_maps_to_centre_of_the_canvas(self):
        game = make_game((1920, 1080))

        x, y = game.to_canvas(game.view_rect.center)

        self.assertAlmostEqual(x, WIDTH // 2, delta=2)
        self.assertAlmostEqual(y, HEIGHT // 2, delta=2)

    def test_mouse_event_position_is_converted_to_canvas_coords(self):
        game = make_game((1920, 1080))
        target = (500, 290)
        window_pos = (game.view_rect.x + int(target[0] * game.view_scale),
                      game.view_rect.y + int(target[1] * game.view_scale))

        event = game._scaled_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": window_pos, "button": 1}))

        self.assertAlmostEqual(event.pos[0], target[0], delta=2)
        self.assertAlmostEqual(event.pos[1], target[1], delta=2)

    def test_non_mouse_events_pass_through_unchanged(self):
        game = make_game((1920, 1080))
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})

        self.assertIs(game._scaled_event(event), event)


if __name__ == "__main__":
    unittest.main()
