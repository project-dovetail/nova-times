from typing import Optional

from astropy.table import Table
from matplotlib.axes import Axes

from matplotlib.lines import Line2D


def viz_dataset(ax: Axes, data_table: Table, band: Optional[str] = None) -> None:

    marker_keys = list(Line2D.markers.keys())
    for marker_indx, group in enumerate(data_table.groups):
        band_label = group[0]["Band"]
        if band is None or band_label == band:
            ax.scatter(
                group["JD"],
                group["Magnitude"],
                marker=str(marker_keys[marker_indx]),
                label=band_label,
            )
    ax.invert_yaxis()
    ax.set_xlabel("Julian Date (JD)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Light Curve of the Novae")
    ax.legend()

    return
