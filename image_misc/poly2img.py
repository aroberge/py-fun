'''simple converter from "dna" into an image file - PIL figures out
the required image type from the extension.'''
import sys

import aggdraw
import Image # from PIL

class DNA(object):
    def __init__(self):
        self.polygons = None
        self.edges = None
        self.genes = []

class Drawing(object):
    def __init__(self):
        self.background = None
        self.dna = DNA()

def open_and_read_dna_file(filename):
    items = open(filename).read().split()
    drawing = Drawing()
    drawing.background = items[0]
    drawing.dna.polygons = int(items[1])
    drawing.dna.edges = int(items[2])
    nb_coords = 2*drawing.dna.edges
    nb_subitems = nb_coords + 4  # 4 color values per polygon
    offset = 3  # first 3 values are excluded
    drawing.dna.genes = []
    for i in range(drawing.dna.polygons):
        coords = []
        color = []
        for j in range(nb_coords):
            coords.append(int(items[offset+i*nb_subitems + j]))
        for j in range(4):
            color.append(int(items[offset+i*nb_subitems + nb_coords + j]))
        drawing.dna.genes.append([coords, color])
    return drawing

def draw_and_save(drawing, filename):
    w = h = 0
    for gene in drawing.dna.genes:
        for x in gene[0][::2]:
            if x > w:
                w = x
        for y in gene[0][1::2]:
            if y > h:
                h = y
    img = Image.new("RGBA", (w, h), drawing.background)
    context = aggdraw.Draw(img)
    brush = aggdraw.Brush(drawing.background, opacity=255)
    context.rectangle((0, 0, w, h), brush)
    for gene in drawing.dna.genes:
        brush = aggdraw.Brush(tuple(gene[1][0:3]), opacity=gene[1][3])
        context.polygon(gene[0], brush)
    s = context.tostring()
    Image.fromstring('RGBA', (w, h), s).save(filename)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage = """
Usage:
    python poly2img.py polygon_file image_file.ext

The image file format is determined by PIL using the image file extension.
"""
        print usage

        sys.exit()
    drawing = open_and_read_dna_file(sys.argv[1])
    draw_and_save(drawing, sys.argv[2])