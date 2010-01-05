###############################################
## adapted from http://www.uselesspython.com

from Tkinter import Tk, Canvas
import time

n = 40
width = 600
height = 600
start = -3 + 1.5j
stop  = 1 - 1.5j
step = abs(start.real - stop.real) / width
points = []


def phi(point):
    ''' converts a screen point into a complex number '''
    x, y = point
    a = start.real + x*step
    b = start.imag - y*step
    return complex(a, b)

def mandelbrot():
    ''' the mandelbrot algorithm '''
    for i in range(0, width):
        for j in range(0, height):
            z = phi((i, j))
            c = z
            cnt = 0
            while abs(z) < 2.0 and cnt < n:
                z = z*z + c
                cnt = cnt + 1
            if abs(z) < 2.0:
                points.append((i, j))

begin = time.time()
mandelbrot()
time1 = time.time() - begin
print("Time taken for calculating points = %s" % time1)

root = Tk()
root.title("The Mandelbrot set")
cv = Canvas(root,width=width,height=height)

begin = time.time()
for point in points:
    x, y = point
    cv.create_line(x, y, x+1, y+1)

time2 = time.time() - begin
print("Time taken for drawing = %s" % time2)

print("Total time = %s" % (time1 + time2))

cv.pack()
root.mainloop()
