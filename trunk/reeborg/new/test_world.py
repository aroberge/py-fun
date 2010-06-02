
import unittest
from world import World


class TestWorld(unittest.TestCase):

    def test_simple_world_creation(self):
        w = World(3, 2)
        self.assertEqual(w._nb_rows, 2)
        self.assertEqual(w._nb_cols, 3)
        self.assertEqual(w._east_walls, set([(3, 1), (3, 2)]))
        self.assertEqual(w._north_walls, set([(1, 2), (2, 2), (3,2)]))
        self.assertEqual(w._artifacts, {})
        self.assertEqual(w._robots, {})

    def test_is_clear_empty_world(self):
        w = World()
        self.assertTrue(w.is_clear(1, 1, "East"))
        self.assertFalse(w.is_clear(1, 1, "West"))
        self.assertTrue(w.is_clear(2, 1, "West"))
        self.assertTrue(w.is_clear(1, 1, "North"))
        self.assertFalse(w.is_clear(1, 1, "South"))
        self.assertTrue(w.is_clear(1, 2, "South"))

    def test_is_clear_square_world(self):
        w = World(3, 2)
        self.assertTrue(w.is_clear(1, 1, "East"))
        self.assertFalse(w.is_clear(1, 1, "West"))
        self.assertTrue(w.is_clear(2, 1, "West"))
        self.assertTrue(w.is_clear(1, 1, "North"))
        self.assertFalse(w.is_clear(1, 1, "South"))
        self.assertTrue(w.is_clear(1, 2, "South"))
        #
        self.assertFalse(w.is_clear(3, 2, "East"))
        self.assertTrue(w.is_clear(3, 2, "West"))
        self.assertFalse(w.is_clear(3, 2, "North"))
        self.assertTrue(w.is_clear(3, 2, "South"))

    def test_is_clear_exception(self):
        w = World()
        self.assertRaises(ValueError, w.is_clear, 1, 1, 'wrong')

    def test_build_east_wall_empty_world(self):
        w = World()
        self.assertTrue(w.is_clear(1, 1, "East"))
        self.assertTrue(w.build_wall(1, 1, 'East'))
        self.assertFalse(w.is_clear(1, 1, "East"))
        self.assertFalse(w.build_wall(1, 1, 'East'))
        self.assertFalse(w.is_clear(1, 1, "East"))
        self.assertFalse(w.is_clear(2, 1, "West"))

    def test_build_west_wall_empty_world(self):
        w = World()
        self.assertTrue(w.is_clear(3, 3, "West"))
        self.assertTrue(w.build_wall(3, 3, 'West'))
        self.assertFalse(w.is_clear(3, 3, "West"))
        self.assertFalse(w.build_wall(3, 3, 'West'))
        self.assertFalse(w.is_clear(3, 3, "West"))
        self.assertFalse(w.is_clear(2, 3, "East"))

    def test_build_north_wall_empty_world(self):
        w = World()
        self.assertTrue(w.is_clear(1, 1, "North"))
        self.assertTrue(w.build_wall(1, 1, 'North'))
        self.assertFalse(w.is_clear(1, 1, "North"))
        self.assertFalse(w.build_wall(1, 1, 'North'))
        self.assertFalse(w.is_clear(1, 1, "North"))
        self.assertFalse(w.is_clear(1, 2, "South"))

    def test_build_south_wall_empty_world(self):
        w = World()
        self.assertTrue(w.is_clear(3, 3, "South"))
        self.assertTrue(w.build_wall(3, 3, 'South'))
        self.assertFalse(w.is_clear(3, 3, "South"))
        self.assertFalse(w.build_wall(3, 3, 'South'))
        self.assertFalse(w.is_clear(3, 3, "South"))
        self.assertFalse(w.is_clear(3, 2, "North"))

    def test_build_wall_exception(self):
        w = World()
        self.assertRaises(ValueError, w.build_wall, 1, 1, 'wrong')

if __name__ == '__main__':
    unittest.main()