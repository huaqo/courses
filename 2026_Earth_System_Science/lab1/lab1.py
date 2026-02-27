import numpy as np
import matplotlib.pyplot as plt

planets = {
    "Earth": {"dist": 1.0, "albedo": 0.3, "GHE": 0.4},
    "Venus": {"dist": 0.72, "albedo": 0.80, "GHE": 0.99},
    "Mars":  {"dist": 1.52, "albedo": 0.22, "GHE": 0.09},
}

results = []

for planet in planets:
    L_S = 3.8e26           
    DE = 149.6e9
    DE *= planets[planet]["dist"]
    albedo = planets[planet]["albedo"]
    sigma = 5.670367e-8
    T_e= L_S / ( 4 * np.pi * DE**2)
    PEtop = T_e / 4
    PEsur = PEtop * (1 - albedo)
    TEsur = ( PEsur / sigma )**(1/4)
    TEsur_C = TEsur - 273.15
    PE = 2 * PEsur;
    TEsur_GH05 = ( PE / sigma )**(1/4)
    TEsur_GH05_C = TEsur_GH05 - 273.15
    GHE = planets[planet]["GHE"]
    PE = PEsur / (1 - GHE)
    TEsur_GH04 = ( PE / sigma )**(1/4)

    results.append([planet, TEsur, TEsur_GH05, TEsur_GH04])

    GHE_list = np.arange(0.1,0.55,0.05)
    TEsur_GHE = np.empty((GHE_list.size,1))
    for i in range(len(GHE_list)):
        GHE = GHE_list[i]
        PE = PEsur / (1 - GHE)
        TEsur_GHE[i] = ( PE / sigma )**(1/4)
    plt.plot(GHE_list, TEsur_GHE, label=planet)


# Plot 1

plt.xlabel('GreenHouse Effect', fontsize=12)
plt.ylabel('Temperature [K]', fontsize=12)
plt.grid()
plt.title('Varying GreenHouse gas effects and corresponding surface T', fontsize=14)
plt.legend(title="Planet")
plt.savefig(f"plot.png")


# Plot 2
fig, ax = plt.subplots(figsize=(7, 2))
ax.axis('off')
col_labels = ["Planet", "T_eff [K]", "T(GHE=0.5) [K]", "T(actual GHE) [K]"]
table_data = [[r[0], f"{r[1]:.2f}", f"{r[2]:.2f}", f"{r[3]:.2f}"] for r in results]

print(table_data)

table = ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.5)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#3f51b5')
    else:
        cell.set_facecolor('#f0f0f0')
plt.title("Surface Temperature Estimates for Earth, Venus, and Mars", fontsize=13, pad=10)
plt.tight_layout()
plt.savefig("results_table.png", dpi=300, bbox_inches='tight')
