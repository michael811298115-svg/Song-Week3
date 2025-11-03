# -*- coding: utf-8 -*-
# Streamlit app: Week3 Generative Poster (Streamlit Edition)
# Converts the original matplotlib notebook-style script into an interactive Streamlit app.
# Core logic and function names are preserved (random_palette, blob, generate_poster), with UI controls.
#
# How to run:
#   1) pip install streamlit numpy matplotlib
#   2) streamlit run week3_streamlit_app.py
#
# Notes:
#   - You can control seed for reproducibility.
#   - Supports multiple palettes (random / pastel / vivid / monochrome).
#   - Includes style presets (Minimal / Vivid / NoiseTouch).
#   - Allows saving PNG files directly from the app.

import math
import random
from typing import List, Tuple, Optional

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# -----------------------------
# Original-like helper functions
# -----------------------------
def random_palette(k: int = 5) -> List[Tuple[float, float, float]]:
    """Create and return k random RGB colors (0~1)."""
    return [(random.random(), random.random(), random.random()) for _ in range(k)]


def pastel_palette(k: int = 6) -> List[Tuple[float, float, float]]:
    """Soft, pastel-like palette."""
    colors = [
        (0.98, 0.74, 0.76),  # soft pink
        (0.69, 0.88, 0.90),  # pastel blue
        (0.77, 0.92, 0.80),  # mint green
        (0.98, 0.91, 0.71),  # light yellow
        (0.86, 0.77, 0.90),  # lavender
        (0.99, 0.82, 0.64),  # peach
    ]
    return colors[:k] if k <= len(colors) else colors + random_palette(k - len(colors))


def vivid_palette(k: int = 3) -> List[Tuple[float, float, float]]:
    """High-contrast vivid palette."""
    base = [
        (1.0, 0.0, 0.0),   # bright red
        (0.0, 0.7, 0.0),   # vivid green
        (0.0, 0.0, 1.0),   # strong blue
        (1.0, 0.5, 0.0),   # orange
        (0.8, 0.0, 0.8),   # purple
        (1.0, 1.0, 0.0),   # yellow
    ]
    return base[:k] if k <= len(base) else base + random_palette(k - len(base))


def monochrome_palette(k: int = 3) -> List[Tuple[float, float, float]]:
    """Monochrome blue shades."""
    return [(0.2, 0.2 + i * 0.12, 0.6 + i * 0.05) for i in range(k)]


def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """Generate a wobbly closed blob-like shape."""
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y


def generate_poster(
    palette_fn,
    palette_size: int = 6,
    n_layers: int = 8,
    seed: Optional[int] = None,
    wobble_min: float = 0.05,
    wobble_max: float = 0.25,
    radius_min: float = 0.02,
    radius_max: float = 0.10,
    bg_color=(0.98, 0.98, 0.97),
    figsize=(7, 10),
    title_text: str = "Generative Poster",
    subtitle_text: str = "Week 2 • Arts & Advanced Big Data",
):
    """Draw layered blobs using a chosen palette and parameters."""
    # Seed for reproducibility
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Prepare canvas
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    ax.set_facecolor(bg_color)

    # Palette
    palette = palette_fn(palette_size)

    # Draw blobs
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(radius_min, radius_max)
        x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(wobble_min, wobble_max))
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    # Text overlays
    ax.text(0.05, 0.95, title_text, fontsize=18, weight="bold", transform=ax.transAxes)
    ax.text(0.05, 0.91, subtitle_text, fontsize=11, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Week3 Generative Poster (Streamlit)", layout="wide")

st.title("Week3 Generative Poster · Streamlit Edition")  # keep Week3 naming for continuity
st.caption("Interactive remake of the original matplotlib script — core logic preserved, Streamlit UI added.")

# Sidebar: palette + presets
with st.sidebar:
    st.header("Controls")

    preset = st.selectbox(
        "Style Preset",
        ["Custom", "Minimal", "Vivid", "NoiseTouch"],
        index=0,
        help="Presets set sensible defaults; switch to Custom for full manual control.",
    )

    palette_choice = st.selectbox(
        "Palette Type",
        ["Random", "Pastel", "Vivid", "Monochrome"],
        index=1,
    )

    palette_size = st.slider("Palette Size", 2, 12, 6)

    n_layers = st.slider("Layers", 1, 50, 10)

    wobble_min, wobble_max = st.slider(
        "Wobble Range", 0.0, 2.0, (0.05, 0.25), step=0.01, help="Edge waviness of blobs"
    )
    radius_min, radius_max = st.slider(
        "Radius Range", 0.005, 0.5, (0.02, 0.10), step=0.005, help="Size range for blobs"
    )

    seed_opt = st.text_input("Seed (optional)", value="", help="Use the same seed to reproduce exactly.")
    seed_val = None
    if seed_opt.strip():
        try:
            seed_val = int(seed_opt)
        except ValueError:
            st.warning("Seed must be an integer. Ignoring input.")

    # Figure size
    col_w, col_h = st.columns(2)
    with col_w:
        width_in = st.number_input("Figure Width (inches)", 3.0, 20.0, 7.0, step=0.5)
    with col_h:
        height_in = st.number_input("Figure Height (inches)", 3.0, 20.0, 10.0, step=0.5)

    # Background color (simple presets)
    bg_choice = st.selectbox("Background", ["Off-white", "White", "Black"], index=0)
    if bg_choice == "Off-white":
        bg = (0.98, 0.98, 0.97)
    elif bg_choice == "White":
        bg = (1.0, 1.0, 1.0)
    else:
        bg = (0.05, 0.05, 0.05)

    # Titles
    title_text = st.text_input("Title", "Generative Poster")
    subtitle_text = st.text_input("Subtitle", "Week 2 • Arts & Advanced Big Data")


# Apply presets if selected
if preset == "Minimal":
    n_layers = 5
    wobble_min, wobble_max = 0.02, 0.10
    palette_choice = "Pastel"
elif preset == "Vivid":
    n_layers = 20
    wobble_min, wobble_max = 0.20, 0.80
    palette_choice = "Vivid"
elif preset == "NoiseTouch":
    n_layers = 12
    wobble_min, wobble_max = 0.60, 1.20
    palette_choice = "Random"

# Choose palette function
palette_map = {
    "Random": random_palette,
    "Pastel": pastel_palette,
    "Vivid": vivid_palette,
    "Monochrome": monochrome_palette,
}
palette_fn = palette_map.get(palette_choice, random_palette)

# Draw button
col_left, col_right = st.columns([2, 1])
with col_left:
    if st.button("Generate Poster", use_container_width=True):
        fig = generate_poster(
            palette_fn=palette_fn,
            palette_size=palette_size,
            n_layers=n_layers,
            seed=seed_val,
            wobble_min=wobble_min,
            wobble_max=wobble_max,
            radius_min=radius_min,
            radius_max=radius_max,
            bg_color=bg,
            figsize=(width_in, height_in),
            title_text=title_text,
            subtitle_text=subtitle_text,
        )
        st.pyplot(fig)  # render

        # Save PNG and offer download
        import datetime, io
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"poster_{ts}.png"
        buf = io.BytesIO()
        fig.savefig(buf, dpi=300, bbox_inches="tight", format="png")
        st.success(f"Saved: {fname}")
        st.download_button("Download PNG (300 dpi)", data=buf.getvalue(), file_name=fname, mime="image/png", use_container_width=True)
        plt.close(fig)
    else:
        st.info("Set your parameters on the left, then click **Generate Poster**.")

with col_right:
    st.subheader("Quick Tips")
    st.markdown(
        """
        - **Seed**: repeat a seed to reproduce identical results.
        - **Layers**: more layers → denser composition.
        - **Wobble**: higher = wavier edges; lower = smoother shapes.
        - **Radius**: controls average blob size.
        - Try presets **Minimal / Vivid / NoiseTouch** for quick styles.
        """
    )

st.divider()
st.caption("© Week3 Generative Poster · Streamlit Edition — built for interactive exploration.")
