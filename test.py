import numpy as np
import matplotlib

#
# import matplotlib
# matplotlib.use('Agg')
#
# import pylab
# import os
# pylab.ion()
# x = pylab.arange( 0, 10, 0.1)
# y = pylab.sin(x)
# pylab.plot(x,y, 'ro-')
# pylab.show()
# pylab.savefig('temp.png')
import matplotlib
#matplotlib.use("Agg")

from matplotlib.pyplot import *
plot([1,2,3])
savefig("test.png", dpi=gcf().dpi)
show()