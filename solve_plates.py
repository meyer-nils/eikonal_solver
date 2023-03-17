import os

import numpy as np
import yaml
from nutils import export, function, mesh, solver
from nutils.expression_v2 import Namespace


def solve(domain, geom, l_ref, iloc):
    # Nutils namespace
    ns = Namespace()

    # Define the geometry variable x as well as gradients, normal and jacobians
    # on the domain.
    ns.x = geom
    ns.define_for("x", gradient="∇", normal="n", jacobians=("dV", "dS"))

    # Parameters in namesapce
    ns.G0 = 2.0 / l_ref
    ns.σ = 0.1

    # Basis
    ns.basis = domain.basis("std", degree=1)

    # Define residual
    ns.G = function.dotarg("lhs", ns.basis)
    res = domain.integral("(1 - σ) ∇_i(G) ∇_i(G) basis_n dV" @ ns, degree=2)
    res -= domain.integral("σ G ∇_i(G) ∇_i(basis_n) dV" @ ns, degree=2)
    res -= domain.integral("(1 + 2 σ) G^4 basis_n dV" @ ns, degree=2)

    # Dirichlet boundary for distance to injection
    idx = np.nonzero(iloc.eval(ns.basis)[0])
    inlet = np.nan * np.ones((len(ns.basis)))
    inlet[idx] = 2.0 / l_ref

    # Dirichlet boundary for distance to walls
    sqr = domain.boundary["walls"].integral("(G - G0)^2 dS" @ ns, degree=2)
    walls = solver.optimize("lhs", sqr, droptol=1e-15)

    # Initial values set to G_0
    sqr = domain.integral("(G - G0)^2 dV" @ ns, degree=2)
    lhs0 = solver.optimize("lhs", sqr, droptol=1e-15)

    # Solve non-linear equations with Newton solvers
    lhs_inlet = solver.newton("lhs", res, constrain=inlet, lhs0=lhs0).solve(tol=1e-10)
    lhs_walls = solver.newton("lhs", res, constrain=walls, lhs0=lhs0).solve(tol=1e-10)

    ns.D = "1 / G  - 1 / G0"
    bezier = domain.sample("vtk", 2)
    x, D_i = bezier.eval(["x_i", "D"] @ ns, lhs=lhs_inlet)
    D_w = bezier.eval("D" @ ns, lhs=lhs_walls)
    return bezier.tri, x, D_i, D_w


if __name__ == "__main__":
    # Open YAML file with meta data
    with open("models.yaml") as f:
        meta_data = yaml.safe_load(f)

    # Parse all plates
    for plate, plate_data in meta_data.items():
        print(f"Computing plate {plate}")

        # Get dimensions of plate
        dim_x, dim_y = plate_data["plate"]
        lf = max(dim_x, dim_y)

        # Iterate over injection points
        for loc, dir in plate_data["injection_locations"]:
            lx = int(loc[0])
            ly = int(loc[1])
            mesh_name = os.path.join("data", plate, f"{plate}_{lx}_{ly}_study.msh")

            # Prepare domain
            domain, geom = mesh.gmsh(mesh_name)
            domain = domain.withboundary(walls=domain.boundary)
            iloc = domain.locate(geom, [[loc[0], loc[1]]], tol=5.0)

            # Solve
            tri, x, D_i, D_w = solve(domain, geom, lf, iloc)

            # Export results to VTK
            export.vtk(mesh_name[:-4], tri, x, D_i=D_i, D_w=D_w)
