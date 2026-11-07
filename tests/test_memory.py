import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from scenes.memory_scene import PERFECT_MOVES, MemoryScene
from settings import (MEMORY_HINTS, MEMORY_MATCH_POINTS, MEMORY_MISMATCH_DELAY,
                      MEMORY_PAIRS_PER_ROUND, MEMORY_PERFECT_BONUS,
                      MEMORY_PREVIEW_MS, MEMORY_STREAK_BONUS,
                      MEMORY_STREAK_MAX)


class DummySound:
    def play_click(self):
        pass

    def play_correct(self):
        pass

    def play_error(self):
        pass

    def play_win(self):
        pass


class DummyGame:
    def __init__(self):
        self.sound = DummySound()
        self.total_score = 0
        self.lesson = None

    def add_score(self, points):
        self.total_score += points
        return self.total_score


class DummyButton:
    enabled = True


def make_scene():
    """MemoryScene na walang display/buttons - ang logic lang ang sinusubok."""
    scene = MemoryScene.__new__(MemoryScene)
    scene.game = DummyGame()
    scene.best_moves = None
    scene.back_btn = DummyButton()
    scene.restart_btn = DummyButton()
    scene.hint_btn = DummyButton()
    scene.new_round()
    return scene


def end_preview(scene):
    scene.update(MEMORY_PREVIEW_MS + 1)


def card_pair(scene, pair_id):
    return [c for c in scene.cards if c.pair_id == pair_id]


def match_pair(scene, pair_id):
    a, b = card_pair(scene, pair_id)
    scene.flip(a)
    scene.flip(b)


class MemoryRoundTests(unittest.TestCase):
    def test_round_deals_two_cards_per_pair(self):
        scene = make_scene()

        self.assertEqual(len(scene.cards), MEMORY_PAIRS_PER_ROUND * 2)
        self.assertEqual(scene.pair_count, MEMORY_PAIRS_PER_ROUND)
        for pair_id in range(scene.pair_count):
            kinds = sorted(c.kind for c in card_pair(scene, pair_id))
            self.assertEqual(kinds, ["def", "term"])

    def test_preview_shows_every_card_then_hides_them(self):
        scene = make_scene()

        self.assertTrue(all(c.face_up for c in scene.cards))

        end_preview(scene)

        self.assertFalse(any(c.face_up for c in scene.cards))
        self.assertEqual(scene.preview_timer, 0)

    def test_cards_cannot_be_flipped_during_the_preview(self):
        scene = make_scene()

        scene.flip(scene.cards[0])

        self.assertEqual(scene.moves, 0)
        self.assertEqual(scene.open_cards, [])

    def test_timer_only_runs_after_the_preview(self):
        scene = make_scene()

        scene.update(500)
        self.assertEqual(scene.elapsed, 0)

        end_preview(scene)
        scene.update(1000)

        self.assertEqual(scene.elapsed, 1000)


class MemoryScoringTests(unittest.TestCase):
    def test_first_match_awards_the_base_points(self):
        scene = make_scene()
        end_preview(scene)

        match_pair(scene, 0)

        self.assertEqual(scene.pairs_found(), 1)
        self.assertEqual(scene.moves, 1)
        self.assertEqual(scene.score, MEMORY_MATCH_POINTS)
        self.assertEqual(scene.game.total_score, MEMORY_MATCH_POINTS)

    def test_streak_bonus_grows_and_is_capped(self):
        scene = make_scene()
        end_preview(scene)

        for pair_id in range(MEMORY_STREAK_MAX + 2):
            match_pair(scene, pair_id)

        expected = 0
        for streak in range(1, MEMORY_STREAK_MAX + 3):
            expected += MEMORY_MATCH_POINTS + MEMORY_STREAK_BONUS * min(streak - 1, MEMORY_STREAK_MAX)
        self.assertEqual(scene.score, expected)
        self.assertEqual(scene.best_streak, MEMORY_STREAK_MAX + 2)

    def test_mismatch_hides_the_cards_and_resets_the_streak(self):
        scene = make_scene()
        end_preview(scene)
        match_pair(scene, 0)
        a = card_pair(scene, 1)[0]
        b = card_pair(scene, 2)[0]

        scene.flip(a)
        scene.flip(b)

        self.assertEqual(scene.streak, 0)
        self.assertTrue(a.wrong and b.wrong)
        self.assertEqual(scene.moves, 2)

        scene.update(MEMORY_MISMATCH_DELAY + 1)

        self.assertFalse(a.face_up or b.face_up)
        self.assertFalse(a.wrong or b.wrong)
        self.assertEqual(scene.open_cards, [])

    def test_no_flips_are_accepted_while_a_mismatch_is_showing(self):
        scene = make_scene()
        end_preview(scene)
        scene.flip(card_pair(scene, 0)[0])
        scene.flip(card_pair(scene, 1)[0])

        scene.flip(card_pair(scene, 2)[0])

        self.assertEqual(scene.moves, 1)

    def test_perfect_round_adds_the_efficiency_bonus(self):
        scene = make_scene()
        end_preview(scene)

        for pair_id in range(scene.pair_count):
            match_pair(scene, pair_id)

        self.assertTrue(scene.won)
        self.assertLessEqual(scene.moves, PERFECT_MOVES)
        self.assertEqual(scene.best_moves, scene.moves)
        self.assertEqual(scene.score, scene.game.total_score)
        self.assertIn(str(MEMORY_PERFECT_BONUS), scene.message)

    def test_no_flips_are_accepted_after_the_round_is_won(self):
        scene = make_scene()
        end_preview(scene)
        for pair_id in range(scene.pair_count):
            match_pair(scene, pair_id)
        moves = scene.moves

        scene.flip(scene.cards[0])

        self.assertEqual(scene.moves, moves)


class MemoryHintTests(unittest.TestCase):
    def test_hint_reveals_one_pair_and_resets_the_streak(self):
        scene = make_scene()
        end_preview(scene)
        match_pair(scene, 0)

        scene.use_hint()

        self.assertEqual(len(scene.hint_cards), 2)
        self.assertTrue(all(c.face_up for c in scene.hint_cards))
        self.assertEqual(scene.hints_left, MEMORY_HINTS - 1)
        self.assertEqual(scene.streak, 0)
        self.assertEqual(scene.moves, 1)

        scene.update(scene.hint_timer + 1)

        self.assertEqual(scene.hint_cards, [])
        self.assertEqual(scene.pairs_found(), 1)

    def test_hint_never_reveals_an_already_matched_pair(self):
        scene = make_scene()
        end_preview(scene)
        match_pair(scene, 0)

        scene.use_hint()

        self.assertNotEqual(scene.hint_cards[0].pair_id, 0)

    def test_hints_run_out(self):
        scene = make_scene()
        end_preview(scene)

        for _ in range(MEMORY_HINTS):
            scene.use_hint()
            scene.update(scene.hint_timer + 1)
        scene.use_hint()

        self.assertEqual(scene.hints_left, 0)
        self.assertEqual(scene.hint_cards, [])

    def test_restart_resets_the_round(self):
        scene = make_scene()
        end_preview(scene)
        match_pair(scene, 0)
        scene.use_hint()

        scene.new_round()

        self.assertEqual(scene.moves, 0)
        self.assertEqual(scene.score, 0)
        self.assertEqual(scene.streak, 0)
        self.assertEqual(scene.hints_left, MEMORY_HINTS)
        self.assertEqual(scene.pairs_found(), 0)
        self.assertFalse(scene.won)


if __name__ == "__main__":
    unittest.main()
