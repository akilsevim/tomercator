import csv
from shapely import wkt
import re
import math
from pyproj import Proj
import sys
from functools import partial
import pyproj
from shapely.ops import transform

csv.field_size_limit(sys.maxsize)

RADIUS = 6378137.0


def y2lat(a):
    return 180.0 / math.pi * (2.0 * math.atan(math.exp(a * math.pi / 180.0)) - math.pi / 2.0)


def lat2y(a):
    return 180.0 / math.pi * math.log(math.tan(math.pi / 4.0 + a * (math.pi / 180.0) / 2.0))


def lon2x(a):
    return a * RADIUS

def merc_x(lon):
  r_major=6378137.000
  return r_major*math.radians(lon)

def merc_y(lat):
  if lat>89.5:lat=89.5
  if lat<-89.5:lat=-89.5
  r_major=6378137.000
  r_minor=6356752.3142
  temp=r_minor/r_major
  eccent=math.sqrt(1-temp**2)
  phi=math.radians(lat)
  sinphi=math.sin(phi)
  con=eccent*sinphi
  com=eccent/2
  con=((1.0-con)/(1.0+con))**com
  ts=math.tan((math.pi/2-phi)/2)/con
  y=0-r_major*math.log(ts)
  return y


with open('cemetery_edited.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    with open('cemetery_converted.csv', 'w') as output:
        for row in csv_reader:
            # pat = re.compile(r'''(-*\d+\.\d+ -*\d+\.\d+),*''')
            # matches = pat.findall(row[0])
            # if matches:
            #     lst = [tuple(map(float, m.split())) for m in matches]
            #     for a in lst:
            #         print(a[0])
            #         print(merc_x(a[0]))
            #         break

             P = wkt.loads(row[0])
             project = partial(
                 pyproj.transform,
                 pyproj.Proj(init='epsg:4326'),  # source coordinate system
                 pyproj.Proj(init='epsg:3857'))  # destination coordinate system
             g2 = transform(project, P)  # apply projection
             #print(str(g2)+'\t'+'\t'.join(row[1:])+'\n')
             output.write(str(g2)+'\t'+'\t'.join(row[1:])+'\n')

    output.close()

        # pat = re.compile(r'''(-*\d+\.\d+ -*\d+\.\d+),*''')
        # #s = "POLYGON ((-47.158846224312285 -21.349760242365733;-47.158943117468695 -21.349706412900805;-47.159778541623055 -21.349008036758804))"
        #
        # matches = pat.findall(row[0])
        # if matches:
        #     lst = [tuple(map(float, m.split())) for m in matches]
        #     for a in lst:
        #         print(a)

