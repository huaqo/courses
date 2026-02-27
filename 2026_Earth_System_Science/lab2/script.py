import math
import matplotlib.pyplot as plt

def calculation(what, rho_f, rho_s, g, a, mu):
    """
    rho_f Medium density: kg/m³
    rho_s Object density: kg/m³
    g Gravity: m/s²
    a Radius: m
    mu Viscosity of medium: Pa·s    
    """
    U_ms = abs(2 * (rho_f - rho_s) * g * a**2 / (9 * mu))
    U_kmh = U_ms * 3.6
    U_cmyr = U_ms * 100 * 60 * 60 * 24 * 365.25
    Re = rho_f * U_ms * (2 * a) / mu

    return [what, f"{mu:.1e}", f"{a:.2e}", f"{U_ms:.3e}", f"{U_kmh:.3e}", f"{U_cmyr:.3e}", f"{Re:.3e}"]

# Original objects
objects = [
    calculation("Subducted slab", 3300, 3400, 9.81, 100e3, 1e21),
    calculation("Mantle plume", 3300, 3250, 9.81, 50e3, 1e20),
    calculation("Magma through crust", 2700, 2600, 9.81, 10, 1e3),
    calculation("Rain drop", 1.2, 1000, 9.81, 0.001, 1.8e5),
    calculation("Human fall", 1.2, 1000, 9.81, 0.5, 1.8e5)
]

# _becca version with slightly different inputs
objects_becca = [
    calculation("Subducted slab", 3300, 3350, 9.81, 120e3, 1.1e21),
    calculation("Mantle plume", 3300, 3280, 9.81, 55e3, 9e19),
    calculation("Magma through crust", 2700, 2620, 9.81, 12, 1.2e3),
    calculation("Rain drop", 1.2, 1020, 9.81, 0.002, 2e5),
    calculation("Human fall", 1.2, 980, 9.81, 0.6, 2e5)
]

# Column labels
columns = ["Object", "Viscosity (Pa·s)", "Radius (m)", "Velocity (m/s)", "Velocity (km/h)", "Velocity (cm/yr)", "Reynolds number"]

def create_table_and_plot(objects, filename_suffix, color):
    # Table
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.axis('off')  # Hide axes
    table = ax.table(cellText=objects, colLabels=columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(columns))))
    plt.tight_layout()
    plt.savefig(f"velocity_table_{filename_suffix}.png", dpi=300)
    plt.show()

    # Bar plot (exactly like original)
    names = [obj[0] for obj in objects]
    U_ms = [obj[3] for obj in objects]
    U_kmh = [obj[4] for obj in objects]
    U_cmyr = [obj[5] for obj in objects]

    plt.figure(figsize=(10,6))
    plt.bar(names, U_ms, color=color)
    plt.ylabel("Velocity (m/s)")
    plt.title(f"Comparison of Velocities")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"velocities_{filename_suffix}.png", dpi=300)
    plt.show()

# Generate outputs for both students
create_table_and_plot(objects, "", 'skyblue')
create_table_and_plot(objects_becca, "becca", 'green')
