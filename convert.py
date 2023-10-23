from os.path import join

import meshio
import numpy as np

path = "control_arm"
file = "control_arm.pat"

mesh = meshio.moldflow.read(
    join(path, file),
    scale=1000.0,
    xml_filenames=[join(path, "fill_time.xml"), join(path, "fiber_orientation.xml")],
)

for label in mesh.point_data:
    point_data = mesh.point_data[label]
    if point_data.ndim > 1:
        mesh.point_data[label] = np.hstack([point_data, point_data[:, 3:6]])

mesh.cell_data = {}

meshio.gmsh.write(join(path, file.replace(".pat", ".msh")), mesh, binary=True)
