"""Redraw saved CRC P2 CellCharter domains without refitting the model."""

import argparse
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import zarr
from anndata.io import read_elem
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("spatialdata", type=Path)
parser.add_argument("spatial_dir", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()

tables = zarr.open_group(str(args.spatialdata / "tables"), mode="r")
table_keys = list(tables.group_keys())
assert len(table_keys) == 1, "This demo expects one expression table"
table = tables[table_keys[0]]
obs = read_elem(table["obs"])
positions = pd.read_parquet(args.spatial_dir / "tissue_positions.parquet")
positions = positions.set_index("barcode").loc[obs.index]
with (args.spatial_dir / "scalefactors_json.json").open() as handle:
    scale = json.load(handle)
xy = positions[["pxl_col_in_fullres", "pxl_row_in_fullres"]].to_numpy()
xy = xy * scale["microns_per_pixel"]
assert np.isfinite(xy).all() and obs["spatial_cluster"].notna().all()

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "pdf.fonttype": 42, "svg.fonttype": "none"})
fig, ax = plt.subplots(figsize=(7, 6), layout="constrained")
colors = ["#0072B2", "#D55E00", "#009E73"]
labels = obs["spatial_cluster"].astype(str)
for i, label in enumerate(sorted(labels.unique())):
    color = colors[i] if i < len(colors) else plt.get_cmap("tab20")(i % 20)
    selected = labels.eq(label).to_numpy()
    ax.scatter(xy[selected, 0], xy[selected, 1], c=color, s=0.3,
               marker="s", linewidths=0, rasterized=True, label=label)
ax.set_aspect("equal")
ax.invert_yaxis()
ax.set(xlabel="x (µm)", ylabel="y (µm)", title="CRC P2 · CellCharter domains")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(title="Domain", loc="center left", bbox_to_anchor=(1.02, 0.5),
          frameon=False, markerscale=12, handletextpad=0.5)
fig.savefig(args.output, dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Plotted {len(obs):,} bins; domains: {labels.value_counts().to_dict()}")
