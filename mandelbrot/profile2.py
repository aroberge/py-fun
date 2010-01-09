''' profiling utility

'''

import pstats, cProfile

import time
from mandel9 import tk, FancyViewer

def main():
    root = tk.Tk()
    app = FancyViewer(root)
    for i in range(10):
        app.draw_fractal()

if __name__ == "__main__":
    cProfile.run("main()", "Profile.prof")
    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats(8)