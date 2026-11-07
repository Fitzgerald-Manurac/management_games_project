import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from scenes.team_roles_scene import TeamRolesScene
from settings import ROLE_CORRECT_POINTS, ROLE_TASKS_PER_ROUND
from utils.data import ROLE_DEPARTMENTS, ROLE_TASKS


class DummySound:
    def play_correct(self):
        pass

    def play_error(self):
        pass

    def play_win(self):
        pass

    def play_lose(self):
        pass


class DummyGame:
    def __init__(self):
        self.sound = DummySound()
        self.total_score = 0
        self.lesson = None

    def add_score(self, points):
        self.total_score += points
        return self.total_score


def make_scene(tasks):
    scene = TeamRolesScene.__new__(TeamRolesScene)
    scene.game = DummyGame()
    scene.tasks = list(tasks)
    scene.index = 0
    scene.correct = 0
    scene.wrong = 0
    scene.feedback = ""
    scene.feedback_color = None
    scene.feedback_dept = None
    scene.feedback_ok = False
    scene.feedback_timer = 0
    scene.finished = False
    return scene


class TeamRolesDataTests(unittest.TestCase):
    def test_every_task_points_to_a_known_department(self):
        for task, dept, lesson in ROLE_TASKS:
            self.assertIn(dept, ROLE_DEPARTMENTS, task)
            self.assertIsInstance(lesson, int)

    def test_enough_tasks_for_one_full_round(self):
        self.assertGreaterEqual(len(ROLE_TASKS), ROLE_TASKS_PER_ROUND)

    def test_every_department_has_at_least_one_task(self):
        used = {dept for _task, dept, _lesson in ROLE_TASKS}
        self.assertEqual(used, set(ROLE_DEPARTMENTS))


class TeamRolesLogicTests(unittest.TestCase):
    def test_correct_assignment_scores(self):
        scene = make_scene([("Prepare the annual budget", "Finance", 1)])

        scene.assign("Finance")

        self.assertEqual(scene.correct, 1)
        self.assertEqual(scene.wrong, 0)
        self.assertEqual(scene.game.total_score, ROLE_CORRECT_POINTS)
        self.assertTrue(scene.feedback_ok)

    def test_wrong_assignment_does_not_score(self):
        scene = make_scene([("Prepare the annual budget", "Finance", 1)])

        scene.assign("Operations")

        self.assertEqual(scene.correct, 0)
        self.assertEqual(scene.wrong, 1)
        self.assertEqual(scene.game.total_score, 0)
        self.assertIn("Finance", scene.feedback)

    def test_second_click_ignored_while_feedback_is_showing(self):
        scene = make_scene([("Prepare the annual budget", "Finance", 1)])

        scene.assign("Finance")
        scene.assign("Finance")

        self.assertEqual(scene.correct, 1)
        self.assertEqual(scene.game.total_score, ROLE_CORRECT_POINTS)

    def test_round_finishes_after_the_last_task(self):
        scene = make_scene([
            ("Prepare the annual budget", "Finance", 1),
            ("Recruit new employees", "Human Resources", 1),
        ])

        scene.assign("Finance")
        scene.update(scene.feedback_timer)
        self.assertFalse(scene.finished)
        self.assertEqual(scene.index, 1)

        scene.assign("Human Resources")
        scene.update(scene.feedback_timer)

        self.assertTrue(scene.finished)
        self.assertEqual(scene.correct, 2)
        self.assertIsNone(scene.current_task())


if __name__ == "__main__":
    unittest.main()
