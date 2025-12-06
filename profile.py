import numpy as np
import matplotlib.pyplot as plt

def calculate_gear_profile(a, b, e, z, resolution=2000):
    """
    Calculates the profile of a rolling element eccentric gear.
    
    Parameters:
    a (float): Radius of the crank [cite: 382]
    b (float): Radius of the rolling elements [cite: 382]
    e (float): Eccentricity of the crank [cite: 382]
    z (int):   Teeth count / Number of curve sections (z = |i - 1|) [cite: 157, 382]
    resolution (int): Number of points to generate
    
    Returns:
    tuple: (gear_x, gear_y, path_x, path_y)
    """
    
    # Validation constraint from paper: e < b/2 [cite: 81]
    if e >= b / 2:
        print(f"Warning: Eccentricity e={e} is not smaller than b/2 ({b/2}). "
              "This may violate geometric constraints.")

    # Beta ranges from 0 to 2*pi*z to complete a full rotation of the gear 
    # (Since alpha = beta/z, and alpha needs to go 0->2pi)
    beta = np.linspace(0, 2 * np.pi * z, resolution)
    
    # 1. Calculate scalar distance c(beta) [cite: 108, 109]
    # c = e*cos(beta) + sqrt((a+b)^2 - e^2*sin^2(beta))
    term_sqrt = np.sqrt((a + b)**2 - e**2 * np.sin(beta)**2)
    c = e * np.cos(beta) + term_sqrt
    
    # 2. Calculate the path of rolling element centers vec_c 
    # The paper uses polar coordinates converted to Cartesian
    # The angle is beta/z
    angle_z = beta / z
    path_x = c * np.cos(angle_z)
    path_y = c * np.sin(angle_z)
    
    # 3. Calculate the normal vector vec_n 
    # This vector determines the direction to offset the path to find the gear surface.
    # From Eq 25:
    # vec_n = (c/z) * [cos, sin] + e*sin(beta)*(1 + e*cos(beta)/sqrt_term) * [-sin, cos]
    
    # Radial component vector (cos(angle_z), sin(angle_z))
    # Tangential component vector (-sin(angle_z), cos(angle_z))
    
    factor_tangential = e * np.sin(beta) * (1 + (e * np.cos(beta)) / term_sqrt)
    
    nx = (c / z) * np.cos(angle_z) + factor_tangential * (-np.sin(angle_z))
    ny = (c / z) * np.sin(angle_z) + factor_tangential * (np.cos(angle_z))
    
    # Normalize normal vector N [cite: 207]
    norm_n = np.sqrt(nx**2 + ny**2)
    Nx = nx / norm_n
    Ny = ny / norm_n
    
    # 4. Calculate final gear profile vec_r 
    # r = c + b * N (using q=b as per Eq 29)
    gear_x = path_x + b * Nx
    gear_y = path_y + b * Ny
    
    return gear_x, gear_y, path_x, path_y

# --- Configuration Parameters [cite: 55] ---
# Example values inspired by Figure 1 in the paper
# i = -10 implies z = |-10 - 1| = 11? 
# Wait, Fig 1 caption says i=-10. 
# Eq 13: z = |i - 1|. If i = -10, z = |-11| = 11.
# Let's try a standard configuration.
a_val = 25.0   # Crank radius
b_val = 3.0    # Rolling element radius
e_val = 1.2    # Eccentricity (must be < b/2)
z_val = 10     # Teeth count

# Generate profiles
gx, gy, px, py = calculate_gear_profile(a_val, b_val, e_val, z_val)

# Plotting
plt.figure(figsize=(10, 10))
plt.plot(gx, gy, label='Outer Gear Profile (Equidistant)', color='blue', linewidth=2)
plt.plot(px, py, label='Rolling Element Center Path', color='red', linestyle='--', alpha=0.7)

# Visualizing rolling elements at intervals
num_elements = z_val - 1 # Just an example number of elements to show
indices = np.linspace(0, len(px)-1, num_elements, dtype=int)
for i in indices:
    circle = plt.Circle((px[i], py[i]), b_val, color='gray', alpha=0.3)
    plt.gca().add_patch(circle)

plt.axis('equal')
plt.title(f"Rolling Element Eccentric Drive Geometry\nz={z_val}, e={e_val}, a={a_val}, b={b_val}")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()