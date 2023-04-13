import unittest
from pathlib import Path
from lotusvis.assign_props import AssignProps
from lotusvis.flow_field import ReadIn


def func(x):
    return x + 1


def read(sim_dir):
    sim = ReadIn(sim_dir, "body", 4096, ext="vti")
    return sim.snaps()


def assign_props(snaps):
    snap = AssignProps(snaps[0])
    return snap.p


def norms(snaps):
    snap = AssignProps(snaps[0])
    nx, ny = snap.norm_vecs()
    return nx


class TestIO(unittest.TestCase):

    def test_func(self):
        self.assertTrue(func(3) == 4)

    def test_read(self):
        self.assertTrue(read(f"{Path.cwd()}/pytests/test_data").shape == (1, 7, 103, 97, 1))

    def test_assign(self):
        self.assertTrue(assign_props(read(f"{Path.cwd()}/pytests/test_data")).shape  == (103, 97, 1))
    
    def test_norms(self):
        self.assertTrue(norms(read(f"{Path.cwd()}/pytests/test_data")).shape  == (91,))

if __name__ == '__main__':
    unittest.main()
# test_answer()

# if __name__ == "__main__":
#     sim_dir = f"{Path.cwd()}/pytests/test_data"
#     # assign_props(read(sim_dir))
#     print((read(sim_dir)).shape)