import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 22,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "lines.linewidth": 1.5,
    "savefig.dpi": 300,
    "figure.autolayout": True,
    "axes.grid": True
})


def get_output_dir(model_type):
    if model_type == 1:
        outdir = Path("img/PE")
    elif model_type == 2:
        outdir = Path("img/BE")
    elif model_type == 3:
        outdir = Path("img/QG")
    else:
        raise ValueError("model_type must be 1, 2, 3, or 4")
    
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir

def get_model_prefix(model_type):

    if model_type == 1:
        return "pe_"
    elif model_type == 2:
        return "be_"
    elif model_type == 3:
        return "qg_"
    else:
        raise ValueError("model_type must be 1, 2, 3, or 4")


def plot_y2y3(df, model_type):

    y2, y3 = df["y2"], df["y3"]
    prefix = get_model_prefix(model_type)
    filename = f"{prefix}y3y2.png"
    outdir = get_output_dir(model_type)

    plt.figure(figsize=(12, 5))
    plt.plot(y3, y2, color="#0910aa")
    plt.title("Two-dimensional projection $y_3$ x $y_2$")
    plt.ylim(-1.5, 1.5)
    plt.xlabel("$y_3$")
    plt.ylabel("$y_2$")
    plt.grid(True)
    plt.savefig(outdir / filename)
    plt.close()
    
    return filename

def plot_y1y3(df, model_type):
    
    y1,y3 = df["y1"], df["y3"]
    prefix = get_model_prefix(model_type)
    filename = f"{prefix}y1y3.png"
    outdir = get_output_dir(model_type)

    plt.figure(figsize=(12, 5))
    plt.plot(y1, y3, color="#0910aa")
    plt.title("Two-dimensional projection $y_1$ x $y_3$")
    if model_type == 1:
        plt.ylim(-0.6, 0.6) 
    else:
        plt.ylim(-0.3, 0.3) 
    plt.xlabel("$y_1$")
    plt.ylabel("$y_3$")
    plt.grid(True)
    plt.savefig(outdir / filename)
    plt.close()
    
    return filename

def plot_y1y2(df, model_type):

    y1, y2= df["y1"], df["y2"]
    prefix = get_model_prefix(model_type)
    filename = f"{prefix}y1y2.png"
    outdir = get_output_dir(model_type)

    plt.figure(figsize=(12, 5))
    plt.plot(y1, y2, color="#0910aa")
    plt.title("Two-dimensional projection $y_1$ x $y_2$")
    plt.ylim(-1.5, 1.5)
    plt.xlabel("$y_1$")
    plt.ylabel("$y_2$")
    plt.grid(True)
    plt.savefig(outdir / filename)
    plt.close()
    
    return filename

def plot_xyz_temporal(df, model_type):
    t, x1, y1, z1 = df["time"], df["x1"], df["y1"], df["z1"]

    prefix = get_model_prefix(model_type)
    filename = f"{prefix}time_x1y1z1.png"
    outdir = get_output_dir(model_type)

    plt.figure(figsize=(12, 8))
    plt.plot(t, x1, label="$x_1$", color="#0b8126", linestyle="-")
    plt.plot(t, y1, label="$y_1$", color="#0910aa", linestyle="--")
    plt.plot(t, z1, label="$z_1$", color="#dc3220", linestyle=":")

    plt.xlabel("Time")
    plt.ylabel("Values of $x_1$, $y_1$ and $z_1$")
    plt.title("Temporal evolution of $x_1$, $y_1$ and $z_1$")
    plt.legend()
    plt.grid(True)
    plt.savefig(outdir / filename)
    
    plt.close()
    return filename

def plot_temporal(df, model_type, yi):
    t = df["time"]
    prefix = get_model_prefix(model_type)
    outdir = get_output_dir(model_type)

    if yi == "y1":
        y = df["y1"]
        ylabel = "y1"
    elif yi == "y2":
        y = df["y2"]
        ylabel = "y2"
    elif yi == "y3":
        y = df["y3"]
        ylabel = "y3"
    else:
        raise ValueError("yi must be 1, 2, or 3")
    
    filename = f"{prefix}time{ylabel}.png"
    
    plt.figure(figsize=(12, 5))
    plt.plot(t, y, color="#0910aa")
    plt.title(f"Temporal evolution of ${ylabel}$")
    plt.xlabel("Time")
    plt.ylabel(f"${ylabel}$")
    plt.grid(True)
    plt.savefig(outdir / filename)
    
    plt.close()
    
    return filename

def temporal_evolution_y(df, model_type):
    VARS = ["y1", "y2", "y3"]
    prefix = get_model_prefix(model_type)
    filename = f"{prefix}temporal_evolution_y.png"
    outdir = get_output_dir(model_type)
    
    ylims = {}
    for v in VARS:
        vals = df[v].to_numpy(dtype=float)
        vmin, vmax = vals.min(), vals.max()
        rng = vmax - vmin
        pad = 0.05 * (rng if rng > 0 else 1.0)
        ylims[v] = (vmin - pad, vmax + pad)

    nrows = len(VARS)
    fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(12, 7), sharex=True)
    if nrows == 1:
        axes = [axes]

    for i, v in enumerate(VARS):
        ax = axes[i]
        ax.plot(df["time"].to_numpy(), df[v].to_numpy(), color="#0910aa")
        ax.axhline(0.0, lw=1.5, alpha=0.75)
        ax.grid(True, linewidth=0.4, alpha=0.35)
        ax.set_ylim(*ylims[v])
        ax.text(0.01, 0.88, v, transform=ax.transAxes, fontsize=10, weight="bold")
        if i < nrows - 1:
            ax.tick_params(axis="x", labelbottom=False)

    axes[0].set_title("Stacked time series of $y_1,y_2,y_3$", pad=8)
    axes[-1].set_xlabel("Time")
    plt.subplots_adjust(hspace=0.12, top=0.95, bottom=0.07, left=0.07, right=0.985)
    fig.savefig(outdir / filename)
    plt.close(fig)
    
    return filename

def generate_all_plots(df, model_type):
    generated_plots = []
    if model_type == 1:
        generated_plots.append(plot_xyz_temporal(df, model_type))
        
    generated_plots.append(plot_y1y2(df, model_type))
    generated_plots.append(plot_y1y3(df, model_type))
    generated_plots.append(plot_y2y3(df, model_type))
    generated_plots.append(plot_temporal(df, model_type, "y1"))
    generated_plots.append(plot_temporal(df, model_type, "y2"))
    generated_plots.append(plot_temporal(df, model_type, "y3"))
    generated_plots.append(temporal_evolution_y(df, model_type))
    
    for plot in generated_plots:
        print(f"  - {plot}")
    
    return generated_plots

