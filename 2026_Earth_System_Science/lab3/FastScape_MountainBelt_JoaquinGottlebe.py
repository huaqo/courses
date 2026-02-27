# Requirements:
# conda
# conda install fastscape -c conda-forge
# conda install -c conda-forge "zarr<3"

import numpy as np
import xarray as xr
import xsimlab as xs
import matplotlib.pyplot as plt
from fastscape.models import basic_model

Lx = 100e3
Ly = 100e3
nx = 101
ny = 101

t_end = 5e6
dt = 2e4
time = np.arange(0.0, t_end + dt, dt)

save_every = 10
save_time = time[::save_every]

Kf = 1e-5
m_exp = 0.5
n_exp = 1.0
Kd = 0.3

U_default = 1e-3

BC = "fixed_value"

def experiment(uplift_rate=U_default, k_coef=Kf, area_exp=m_exp, slope_exp=n_exp, diffusivity=Kd, seed=42, label="exp"):

    in_vars = {
        "grid__shape": xr.DataArray([ny, nx], dims=("shape_yx",)),
        "grid__length": xr.DataArray([Ly, Lx], dims=("shape_yx",)),
        "boundary__status": BC,
        "uplift__rate": uplift_rate,
        "diffusion__diffusivity": diffusivity,
        "spl__k_coef": k_coef,
        "spl__area_exp": area_exp,
        "spl__slope_exp": slope_exp,
        "init_topography__seed": seed,
    }

    clocks = {
        "time": xr.IndexVariable("time", time),
        "save": xr.IndexVariable("save", save_time),
    }

    out_vars = {
        "topography__elevation": "save",
        "terrain__slope": "save",
        "drainage__area": "save",
        "erosion__cumulative_height": "save",
    }

    setup = xs.create_setup(
        model=basic_model,
        clocks=clocks,
        master_clock="time",
        input_vars=in_vars,
        output_vars=out_vars,
    )

    ds = setup.xsimlab.run(model=basic_model)

    ds = ds.assign_attrs(
        experiment_label=label,
        uplift_rate=uplift_rate,
        k_coef=k_coef,
        area_exp=area_exp,
        slope_exp=slope_exp,
        diffusivity=diffusivity,
        seed=seed,
        Lx=Lx,
        Ly=Ly,
        nx=nx,
        ny=ny,
        dt=dt,
        t_end=t_end,
        boundary_condition=BC,
    )

    return ds

def plot_maps(ds, title_prefix=""):
    elev = ds["topography__elevation"]
    slope = ds["terrain__slope"]

    elev_f = elev.isel(save=-1)
    slope_f = slope.isel(save=-1)

    _, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(elev_f, origin="lower")
    ax.set_title(f"{title_prefix} final elevation (m)")
    plt.colorbar(im, ax=ax, shrink=0.85)
    plt.show()

    _, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(slope_f, origin="lower")
    ax.set_title(f"{title_prefix} final slope (-)")
    plt.colorbar(im, ax=ax, shrink=0.85)
    plt.show()


def plot_max_elevation(ds, title_prefix=""):
    elev = ds["topography__elevation"]
    t_myr = ds["save"].values / 1e6
    zmax = elev.max(dim=("y", "x")).values

    _, ax = plt.subplots(figsize=(6, 4))
    ax.plot(t_myr, zmax)
    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel("Max elevation (m)")
    ax.set_title(f"{title_prefix} max elevation vs time")
    ax.grid(True, alpha=0.3)
    plt.show()

experiments = [
    dict(label="baseline", uplift_rate=1e-3, k_coef=1e-5, diffusivity=0.3, seed=42),
    dict(label="high_uplift", uplift_rate=2e-3, k_coef=1e-5, diffusivity=0.3, seed=42),
    dict(label="low_Kf", uplift_rate=1e-3, k_coef=3e-6, diffusivity=0.3, seed=42),
    dict(label="high_Kd", uplift_rate=1e-3, k_coef=1e-5, diffusivity=0.9, seed=42),
]

results = {}

for p in experiments:
    ds = experiment(
        uplift_rate=p["uplift_rate"],
        k_coef=p["k_coef"],
        diffusivity=p["diffusivity"],
        seed=p["seed"],
        label=p["label"],
    )
    results[p["label"]] = ds

print("Done. Experiments:", list(results.items()))

#for label, ds in results.items():
#    plot_maps(ds, title_prefix=f"[{label}]")
#    plot_max_elevation(ds, title_prefix=f"[{label}]")
