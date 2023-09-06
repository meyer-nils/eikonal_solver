import meshio
import numpy as np

mesh = meshio.moldflow.read(
    "control_arm.pat",
    scale=1000.0,
    xml_filenames=["fill_time.xml", "fiber_orientation.xml"],
)

for label in mesh.point_data:
    point_data = mesh.point_data[label]
    if point_data.ndim > 1:
        mesh.point_data[label] = np.hstack([point_data, point_data[:, 3:6]])

mesh.cell_data = {}

meshio.gmsh.write("control_arm.msh", mesh, binary=True)
