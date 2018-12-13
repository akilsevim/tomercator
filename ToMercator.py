# Reads CSV file includes shapes and transform them into the desired projection

import csv
import sys
import pyproj
from shapely import wkt
from functools import partial
from shapely.ops import transform

csv.field_size_limit(sys.maxsize)

input_file = 'cemetery_edited.csv'
output_file = 'cemetery_converted.csv'

input_format = 'epsg:4326'
output_format = 'epsg:3857'

with open(input_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    with open(output_file, 'w') as output:
        for row in csv_reader:
            P = wkt.loads(row[0])
            project = partial(
                pyproj.transform,
                pyproj.Proj(init=input_format),  # source coordinate system
                pyproj.Proj(init=output_format))  # destination coordinate system
            g2 = transform(project, P)  # apply projection
            # print(str(g2)+'\t'+'\t'.join(row[1:])+'\n')
            output.write(str(g2) + '\t' + '\t'.join(row[1:]) + '\n')
    output.close()
