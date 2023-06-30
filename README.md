# Eikonal Solver

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
Unfortunately, the norm in the original formualtion is not friendly for the numerical solution. Hence, Fares and Schröder [1] derived the formulation 

$$
    \nabla G(\mathbf{x}) \cdot  \nabla  G(\mathbf{x}) + \sigma G(\mathbf{x}) \Delta G(\mathbf{x}) = (1 + 2\sigma)G^4(\mathbf{x}) \quad \mathbf{x} \in \Omega
$$

for the inverse wall distance $G(\mathbf{x})$. The weak form of this equation is 

$$
    (1-\sigma) \int_\Omega \nabla G(\mathbf{x}) \cdot  \nabla G(\mathbf{x}) H(\mathbf{x}) dV - \sigma \int_V G(\mathbf{x}) \nabla G(\mathbf{x}) \cdot \nabla H(\mathbf{x}) dV - (1+2\sigma) \int_\Omega G^4(\mathbf{x}) H(\mathbf{x}) dV = 0 \quad \forall H(\mathbf{x})
$$

assuming $\nabla G(\mathbf{x}) = 0$ on the Neumann boundary.


[1] Fares, E., Schröder, W. (2002). A differential equation for approximate wall distance. *International Journal for Numerical Methods in Fluids*, *39*(8), 743–762. https://doi.org/10.1002/fld.348

[2] https://www.comsol.de/blogs/tips-using-wall-distance-interface/