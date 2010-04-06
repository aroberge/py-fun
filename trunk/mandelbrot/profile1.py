# profile1.py

import pstats
import cProfile

from viewer3 import tk, FancyViewer

def main():
    root = tk.Tk()
    app = FancyViewer(root)
    app.nb_iterations = 1000
    for i in range(10):
        app.draw_fractal()

if __name__ == "__main__":
    cProfile.run("main()", "Profile.prof")
    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats(14)