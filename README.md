# Eikonal solver
This repository uses the eikonal equation to compute the distance of each point in a 3D geometry from an `inlet` boundary and the `walls` boundary. It may be used (among many other applications) for fast approximations of mold filling simulations [1].

## Theory
The solution of the eikonal equation $u(\mathbf{x})$ can be interpreted as the shortest path to travel from a boundary $\partial \Omega$ to an inner point $\mathbf{x} \in \Omega$. The boundary value problem is given by 

$$
    \begin{aligned}
    |\nabla u(\mathbf{x}) | &= \frac{1}{f(\mathbf{x})} \quad \mathbf{x} \in \Omega  \\
    u(\mathbf{x}) &= u_0(\mathbf{x}) \quad \mathbf{x} \in \partial \Omega , 
    \end{aligned}
$$

where $f(\mathbf{x})>0$ denotes the speed of travel. For $f \equiv 1$, it computes the geodesic distance to the boundary.

## Methods

### FEM solution (Fares & Schröder)
Unfortunately, the norm in the original formualtion is not friendly for the numerical solution. Hence, Fares and Schröder [2,3] derived the formulation 

$$
    \nabla G(\mathbf{x}) \cdot  \nabla  G(\mathbf{x}) + \sigma G(\mathbf{x}) \Delta G(\mathbf{x}) = (1 + 2\sigma)G^4(\mathbf{x}) \quad \mathbf{x} \in \Omega
$$

for the inverse wall distance $G(\mathbf{x})$. The weak form of this equation is 

$$
    (1-\sigma) \int_\Omega \nabla G(\mathbf{x}) \cdot  \nabla G(\mathbf{x}) H(\mathbf{x}) dV - \sigma \int_V G(\mathbf{x}) \nabla G(\mathbf{x}) \cdot \nabla H(\mathbf{x}) dV - (1+2\sigma) \int_\Omega G^4(\mathbf{x}) H(\mathbf{x}) dV = 0 \quad \forall H(\mathbf{x})
$$

assuming $\nabla G(\mathbf{x}) = 0$ on the Neumann boundary.

To use this method, edit the input mesh in the Notebook `fares_schroeder.ipynb` in this line
```python
mesh_name = os.path.join("meshes", "control_arm_hole.msh")
```
and run all cells. The nutils [4] based solver computes the properties `D_i` and `D_w` representing the distance to the inlet surface and the next wall, respectively. 

### Fast iterative method for tetragonal meshes
An alternative to the FEM based solution approach are iterative methods, e.g. the Fast Marching Method [5] or Fast Sweeping Method [6]. For parallel execution on tetragonal domains, Fu et al. [7] suggest the tetragonal Fast Iterative Method, which is very suitable for the solution in this case.

To use this method, edit the input mesh in the Notebook `fim.ipynb` in this line
```python
mesh_name = os.path.join("meshes", "control_arm_hole.msh")
```
and run all cells. The solver computes (among some other propeties) the properties `D_i` and `D_w` representing the distance to the inlet surface and the next wall, respectively.

## Postprocessing 
The results are exported as `*.vtu` file. These can be visualized e.g. with ParaView [9].

## References

[1] Ospald, F., Herzog, R. (2018). SIMP based Topology Optimization for Injection Molding of SFRPs, *12th World Congress on Structural and Multidisciplinary Optimization*, Braunschweig, Germany. https://doi.org/10.1007/978-3-319-67988-4_65

[2] Fares, E., Schröder, W. (2002). A differential equation for approximate wall distance. *International Journal for Numerical Methods in Fluids*, *39*(8), 743–762. https://doi.org/10.1002/fld.348

[3] https://www.comsol.de/blogs/tips-using-wall-distance-interface/

[4] https://nutils.org

[5] Kimmel, R., Sethian, J. A. (1998). Computing geodesic paths on manifolds, *Proceedings of the National Academy of Sciences of the United States of America* *95*(15) 8431–8435. https://doi.org/10.1073/pnas.95.15.8431.

[6] Zhao, H. (2004). A fast sweeping method for eikonal equations, *Mathematics of Computation* *74*(250) 603–627. https://doi.org/10.1090/s0025-5718-04-
01678-3.

[7] Fu, Z., Kirby, R. M., Whitaker, R. T. (2013). A fast iterative method for solving the eikonal equation on tetrahedral domains, *SIAM Journal on Scientific Computing* *35*(5) 473–494. https://doi.org/10.1137/120881956.

[8] Grandits, T. (2021) A fast iterative method python package, *Journal of Open Source Software* *6* (66) 3641. https://doi.org/10.21105/joss.03641.

[9] https://www.paraview.org

