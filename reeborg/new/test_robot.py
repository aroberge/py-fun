
import unittest
from robot import Robot
from world import World

class TestRobot(unittest.TestCase):

    def test_initial_position_in_empty_world(self):
        w = World()
        r = Robot(w)
        self.assertTrue(r.front_is_clear())
        self.assertFalse(r.right_is_clear())
        self.assertTrue(r.left_is_clear())
        self.assertTrue(r.facing_east())
        for t in [r.facing_north(), r.facing_south(), r.facing_west()]:
            self.assertFalse(t)

    def test_turn_left(self):
        w = World()
        r = Robot(w)
        r.turn_left()
        self.assertTrue(r.facing_north())
        r.turn_left()
        self.assertTrue(r.facing_west())
        r.turn_left()
        self.assertTrue(r.facing_south())
        r.turn_left()
        self.assertTrue(r.facing_east())

    def test_turn_right(self):
        w = World()
        r = Robot(w)
        r.turn_right()
        self.assertTrue(r.facing_south())
        r.turn_right()
        self.assertTrue(r.facing_west())
        r.turn_right()
        self.assertTrue(r.facing_north())
        r.turn_right()
        self.assertTrue(r.facing_east())

    def test_turn_around(self):
        w = World()
        r = Robot(w)
        r.turn_around()
        self.assertTrue(r.facing_west())
        r.turn_around()
        self.assertTrue(r.facing_east())
        r.turn_left()
        r.turn_around()
        self.assertTrue(r.facing_south())
        r.turn_around()
        self.assertTrue(r.facing_north())

    def test_build_wall(self):
        w = World()
        r = Robot(w)
        self.assertTrue(r.front_is_clear())
        r.build_wall()
        self.assertFalse(r.front_is_clear())

    def test_move(self):
        r = Robot(World())
        self.assertEqual(r.x, 1)
        self.assertEqual(r.y, 1)
        r.move()
        self.assertEqual(r.x, 2)
        self.assertEqual(r.y, 1)
        self.assertTrue(r.facing_east())
        r.turn_left()
        r.move()
        self.assertEqual(r.x, 2)
        self.assertEqual(r.y, 2)
        self.assertTrue(r.facing_north())
        r.turn_left()
        r.move()
        self.assertEqual(r.x, 1)
        self.assertEqual(r.y, 2)
        self.assertTrue(r.facing_west())
        r.turn_left()
        r.move()
        self.assertEqual(r.x, 1)
        self.assertEqual(r.y, 1)
        self.assertTrue(r.facing_south())



if __name__ == '__main__':
    unittest.main()