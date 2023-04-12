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
    x, y, nx, ny = snap.norm_vecs()
    return nx


def test_answer():
    assert func(3) == 4
    assert read(f"{Path.cwd()}/test_data").shape == (1, 7, 103, 97, 1)
    assert assign_props(read(f"{Path.cwd()}/test_data")).shape  == (103, 97, 1)
    assert norms(read(f"{Path.cwd()}/test_data")).shape  == (91,)

if __name__ == "__main__":
    sim_dir = f"{Path.cwd()}/pytests/test_data"
    # assign_props(read(sim_dir))
    print((read(sim_dir)).shape)