'''
Program to print a table needed to cut a spherical shape of a desired
radius using the approximate-step method.

This function calculates and prints the ball turning coordinates.  The
strategy is to calculate how far to feed the longitudinal feed for a
desired crossfeed.  Thus, the steps you'll follow to turn a hemisphere
are:

    1.  Center a square cutting toolbit (I use a cutoff tool and take
        light cuts).  I assume all material to the right of the tool 
        is at the diameter of the hemisphere.
    2.  Suppose you're feeding towards the tailstock.  Place the left
        edge of the cutoff tool at the longitudinal position of the
        hemisphere's center.
    3.  Move the carriage to the right a distance of x1.  Then feed
        the crossfeed in a distance of 2*dy.  Cut to the right end of
        the hemisphere, then return to the starting position.
    4.  Move right to x2, feed the crossfeed again in a distance of 
        2*dy from where it was, then cut to the right end.
    5.  Repeat steps 3 and 4 until you've finished with the last yk.

I use a 2" dial indicator to measure the position of the carriage,
so it's easy to move the carriage to the next required position.

The Cartesian coordinate system put onto the lathe has the X direction
parallel to the axis of rotation and the Y direction is in the direction
of movement of the cross slide.

The algorithm uses the equation for a circle in Cartesian coordinates
in the first quadrant:

    x*x + y*y = r*r

This is solved for x:
    
    x = sqrt(r*r - y*y)

    where r is given and 0 <= y <= r.

The formulas for the calculations are as follows.

    xk = the kth ordinate (here, ordinate = longitudinal feed)
    yk = the kth abscissa (here, abscissa = cross feed)
    r  = the radius of the ball
    dy = the increment in y
    n  = number of desired steps

    yk = r - k*dy   for k = 0, 1, 2, ..., n
    xk = sqrt(2*r*k*dy-k*k*dy*dy)

The table that gets printed is then:
    column 1:  k
    column 2:  xk
    column 3:  2*yk   (the 2 corrects from radius to diameter)

-----------------------------------------------------------------
Copyright (C) 2012 Don Peterson
Contact:  gmail.com@someonesdad1

The Wide Open License (WOL)

Permission to use, copy, modify, distribute and sell this
software and its documentation for any purpose is hereby granted
without fee, provided that the above copyright notice and this
license appear in all source copies.  THIS SOFTWARE IS PROVIDED
"AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY OF ANY KIND. See
http://www.dspguru.com/wide-open-license for more information.
'''

from __future__ import division
import sys, os, getopt
from math import sqrt

in2mm = 25.4

def out(*v, **kw):
    sep = kw.setdefault("sep", " ")
    nl  = kw.setdefault("nl", True)
    stream = kw.setdefault("stream", sys.stdout)
    stream.write(sep.join([str(i) for i in v]))
    if nl:
        stream.write("\n")

def Usage(status=1):
    path, name = os.path.split(sys.argv[0])
    out('''
Usage:  {name} OD num_steps
  Print a table to cut a spherical shape on the lathe.  Dimensions are
  given in inches and mm.
'''[1:-1].format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-m"] = False     # Print out in mm
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "m")
    except getopt.GetoptError as str:
        msg, option = str
        out(msg + nl)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-m":
            d["-m"] = True
    if len(args) != 2:
        Usage()
    return args

def main():
    d = {} # Options dictionary
    args = ParseCommandLine(d)
    D = float(args[0])
    n = int(args[1])
    r = D/2
    dy = r/n
    out("Ball diameter  = %.3f inches = %.2f mm" % (D, in2mm*D))
    out("Crossfeed step = %.3f inches = %.2f mm\n" % (dy, in2mm*dy))
    out("         Longitudinal            Crossfeed")
    out("Num     inches     mm         inches     mm")
    out("---     ------   ------       ------   ------")
    for i in range(1, n+1):
        yi = r-i*dy;
        xi = sqrt(2*r*i*dy-i*i*dy*dy);
        f = "%9.3f"
        fm = "%9.2f"
        out("%3d  " % i, nl=False)
        out(f % xi, nl=False)
        out(fm % (in2mm*xi), nl=False)
        out("    ", nl=False)
        y = 2*(r-yi)
        out(f % y, nl=False)
        out(fm % (in2mm*y))

main()
