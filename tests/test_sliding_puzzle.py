import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import pygame

from scenes.sliding_puzzle_scene import SlidingPuzzleScene
from settings import SLIDING_BASE_POINTS, SLIDING_BONUS_POINTS, SLIDING_PAR_MOVES


class DummySound:
    def play_click(self):
        pass

    def play_win(self):
        pass


class DummyGame:
    def __init__(self):
        self.sound = DummySound()
        self.total_score = 0

    def add_score(self, points):
        self.total_score += points
        return self.total_score


def make_puzzle(board, moves=0):
    """Puzzle na walang pygame display - logic lang ang sinusubok."""
    puzzle = SlidingPuzzleScene.__new__(SlidingPuzzleScene)
    puzzle.size = 3
    puzzle.board = list(board)
    puzzle.moves = moves
    puzzle.elapsed_ms = 0
    puzzle.solved = False
    puzzle.auto_solved = False
    puzzle.last_points = 0
    puzzle.best_moves = None
    puzzle.anim = None
    puzzle.tile_rects = puzzle._build_rects()
    puzzle.game = DummyGame()
    return puzzle


class SlidingPuzzleLogicTests(unittest.TestCase):
    def test_can_move_empty_space_adjacent_tiles(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8])

        self.assertTrue(puzzle.can_move(8))
        self.assertFalse(puzzle.can_move(0))

    def test_move_tile_swaps_with_empty_space(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8])

        puzzle.move_tile(8)

        self.assertEqual(puzzle.board, [1, 2, 3, 4, 5, 6, 7, 8, 0])
        self.assertEqual(puzzle.moves, 1)

    def test_win_detects_ordered_board(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])

        self.assertTrue(puzzle.is_solved())

    def test_solving_awards_base_plus_bonus(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8], moves=5)

        puzzle.move_tile(8)

        self.assertTrue(puzzle.solved)
        self.assertEqual(puzzle.game.total_score, SLIDING_BASE_POINTS + SLIDING_BONUS_POINTS)
        self.assertEqual(puzzle.best_moves, 6)

    def test_many_moves_get_no_full_bonus(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8], moves=SLIDING_PAR_MOVES * 3)

        puzzle.move_tile(8)

        self.assertEqual(puzzle.game.total_score, SLIDING_BASE_POINTS)

    def test_auto_solve_marks_solved_without_points(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8])

        puzzle.auto_solve()

        self.assertEqual(puzzle.board, [1, 2, 3, 4, 5, 6, 7, 8, 0])
        self.assertTrue(puzzle.solved)
        self.assertTrue(puzzle.auto_solved)
        self.assertEqual(puzzle.game.total_score, 0)

    def test_no_more_moves_after_auto_solve(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8])
        puzzle.auto_solve()

        self.assertFalse(puzzle.move_tile(5))
        self.assertEqual(puzzle.game.total_score, 0)

    def test_arrow_key_slides_tile_into_the_gap(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8])

        self.assertTrue(puzzle.move_from_direction(pygame.K_LEFT))
        self.assertEqual(puzzle.board, [1, 2, 3, 4, 5, 6, 7, 8, 0])

    def test_arrow_key_outside_the_board_is_ignored(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])
        puzzle.solved = False

        self.assertFalse(puzzle.move_from_direction(pygame.K_LEFT))
        self.assertEqual(puzzle.moves, 0)

    def test_placed_count_follows_board(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 0, 7, 8, 6])

        self.assertEqual(puzzle.placed_count(), 7)
        self.assertTrue(puzzle.is_placed(0))
        self.assertFalse(puzzle.is_placed(5))
        self.assertFalse(puzzle.is_placed(8))

    def test_new_puzzle_is_shuffled_and_solvable(self):
        puzzle = make_puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])

        puzzle.new_puzzle()

        self.assertFalse(puzzle.is_solved())
        self.assertEqual(sorted(puzzle.board), list(range(9)))
        self.assertEqual(puzzle.moves, 0)
        self.assertEqual(len(puzzle.tile_labels), 8)


if __name__ == "__main__":
    unittest.main()
