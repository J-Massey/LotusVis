import unittest
from os
from lotusvis.assign_props import AssignProps
from lotusvis.flow_field import ReadIn


def func(x):
    return x + 1


def read(sim_dir):
    sim = ReadIn(sim_dir, "fluid", 4096, ext="vti")
    return sim.snaps(save=False)


def assign_props(snaps):
    snap = AssignProps(snaps)
    return snap.U[0]


def norms(snaps):
    snap = AssignProps(snaps[0])
    nx, ny = snap.norm_vecs()
    return nx


class TestIO(unittest.TestCase):

    def test_func(self):
        self.assertTrue(func(3) == 4)

    def test_read(self):
        self.assertTrue(read(f"{os.getcwd()}/pytests/test_data").shape == (1, 4, 103, 97, 1))

    def test_assign(self):
        self.assertTrue(assign_props(read(f"{os.getcwd()}/pytests/test_data")).shape  == (103, 97, 1))
    
    def test_norms(self):
        self.assertTrue(norms(read(f"{os.getcwd()}/pytests/test_data")).shape  == (97,))

if __name__ == '__main__':
    unittest.main()

# if __name__ == "__main__":
#     print(norms(read(f"{os.getcwd()}/pytests/test_data")).shape)