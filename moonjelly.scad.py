#!/usr/bin/env python3

'''Basic Solid Python setup for openscad.
Make a moon jellyfish
'''


import solid2 as sd
import numpy as np




def parseArguments():
    # Argument parsing
    import argparse
    parser = argparse.ArgumentParser(
        description='Generate SCAD for object')
    parser.add_argument('-l', action='store', default='30', dest='length',
        type=float, help='Length of object.')
    parser.add_argument('--gap', action='store', default='1', dest='gap',
        type=float, help='Tolerance gap between pieces.')
    parser.add_argument('-n', action='store', default='128', dest='fn',
        type=int, help='Curvature parameter. Number of sides on circle.')
    parser.add_argument('-s', action='store', default='1', dest='fs',
        type=int, help='Curvature parameter. Straightline distance on curves in mm.')
    return parser.parse_args()

def moonjelly(R=50, r=15):
    body = sd.sphere(50)
    body = sd.scale([1,1,.75])(body)
    body = sd.translate([0,0,R/4])(body)
    upper = sd.cube(1000, center=True)
    upper = sd.translate([0,0,500])(upper)
    body &= upper
    node = sd.sphere(1.5*r)
    node += sd.union()(*[sd.rotate([0,0,i*90])(sd.translate([1.5*r,0,0])(node)) for i in range(4)])
    # node += sd.rotate([0,0,45])(node)
    body += sd.translate([0,0,.6*R])(node)
    body -= sd.translate([0,0,.9*R])(upper)
    tent = sd.cylinder(r=.95*R, h=.4*r)
    tent = sd.rotate([180,0,0])(tent)
    leg = sd.cylinder(r=1, h=.7*r)
    leg = sd.rotate([180,0,0])(leg)
    leg = sd.hull()(leg, sd.translate([R,0,0])(leg))
    leg = sd.translate([.8*R,0,0])(leg)
    leg = sd.union()(*[sd.rotate([0,0,i*4])(leg) for i in range(90)])
    tent -= leg
    body += tent
    body = sd.rotate([180,0,0])(body)
    body = sd.translate([0,0,.9*R])(body)
    # hole = sd.cylinder(r=2,h=.4)
    # hole = sd.translate([10,0,0])(hole)
    # body -= sd.union()(*[sd.rotate([0,0,i*90])(hole) for i in range(4)])
    arc = sd.cylinder(h=1,r=.9*r)-sd.cylinder(h=1.1, r=.7*r)
    arc -= sd.cube(R)
    arc = sd.rotate([0,0,-45])(arc)
    arc = sd.translate([-1.5*r,0,0])(arc)
    arc = sd.union()(*[sd.rotate([0,0,i*90])(arc) for i in range(4)])
    body -= arc
    return body

if __name__ == '__main__':
    args = parseArguments()
    parameters = vars(args)  # Makes a dictionary from argument keywords
    final = moonjelly()
    # print(sd.scad_render(final, file_header=f'$fs={args.fs};'))
    print(sd.scad_render(final, file_header=f'$fn={args.fn};'))
