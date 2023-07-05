# Eikonal Solver
This repository uses the Eikonal equation to compute the distance of each point in a 3D geometry from an `inlet` boundary and the `walls` boundary. It can be used for fast approximations of mold filling simulations [1].

## How to use this repo?

### Mesh Preparation 
1. Open a CAD model in the Gmsh [2] GUI.
2. Add a physical Volume group named `domain` that contains the entire part volume. End the selection process with pressing key `e`.
3. Add a physical Surface Group named `walls` that contains all surfaces of the part. Use `CTRL + mouse click` for window selection.
4. Add a physical Surface Group named `inlet` that contains the surface for the inlet boundary.
5. Set the mesh size via `Tools` -> `Options` -> `Mesh` -> `General` -> `Element size factor`.
6. Create `1D`, `2D`, and `3D` meshes by clicking these entries subsequently.
7. Export `*.msh` file by clicking `Save`.

### Solve equations 
Edit the input mesh in the Notebook `solver.ipynb` in this line
```python
mesh_name = os.path.join("meshes", "control_arm_hole.msh")
```
and run all cells. The nutils [3] based solver computes the properties `D_i` and `D_w` representing the distance to the inlet surface and the next wall, respectively. 

### Postprocessing 
The results are exported as `*.vtk` file. These can be visualized e.g. with ParaView [4].


## Eikonal equation
The solution of the Eikonal equation $u(\mathbf{x})$ can be interpreted as the shortest path to travel from a boundary $\partial \Omega$ to an inner point $\mathbf{x} \in \Omega$. It is given by 

$$
    |\nabla u(\mathbf{x}) | = \frac{1}{f(\mathbf{x})} \quad \mathbf{x} \in \Omega 
$$

and 

$$
    u(\mathbf{x}) = u_0(\mathbf{x}) \quad \mathbf{x} \in \partial \Omega , 
$$

where $f(\mathbf{x})>0$ denotes the speed of travel. For $f \equiv 1$, it computes the distance to the boundary.

## Modified Eikonal equation
Unfortunately, the norm in the original formualtion is not friendly for the numerical solution. Hence, Fares and Schröder [5] derived the formulation 

$$
    \nabla G(\mathbf{x}) \cdot  \nabla  G(\mathbf{x}) + \sigma G(\mathbf{x}) \Delta G(\mathbf{x}) = (1 + 2\sigma)G^4(\mathbf{x}) \quad \mathbf{x} \in \Omega
$$

for the inverse wall distance $G(\mathbf{x})$. The weak form of this equation is 

$$
    (1-\sigma) \int_\Omega \nabla G(\mathbf{x}) \cdot  \nabla G(\mathbf{x}) H(\mathbf{x}) dV - \sigma \int_V G(\mathbf{x}) \nabla G(\mathbf{x}) \cdot \nabla H(\mathbf{x}) dV - (1+2\sigma) \int_\Omega G^4(\mathbf{x}) H(\mathbf{x}) dV = 0 \quad \forall H(\mathbf{x})
$$

assuming $\nabla G(\mathbf{x}) = 0$ on the Neumann boundary.

[1] Ospald, F., Herzog, R. (2018). SIMP based Topology Optimization for Injection Molding of SFRPs, *12th World Congress on Structural and Multidisciplinary Optimization*, Braunschweig, Germany. https://doi.org/10.1007/978-3-319-67988-4_65

[2] https://gmsh.info

[3] https://nutils.org

[4] https://www.paraview.org

[5] Fares, E., Schröder, W. (2002). A differential equation for approximate wall distance. *International Journal for Numerical Methods in Fluids*, *39*(8), 743–762. https://doi.org/10.1002/fld.348

[5] https://www.comsol.de/blogs/tips-using-wall-distance-interface/