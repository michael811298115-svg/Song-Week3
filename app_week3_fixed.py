# app_week3_fixed.py
# Week 3 — Generative Poster (Streamlit, corrected syntax)

import io
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import streamlit as st

# ---------------- Core logic ----------------
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.12):
    """Generate a wobbly closed shape around a center with base radius r."""
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def make_palette(k=8, mode="pastel", base_h=0.60):
    """Return k colors (RGB) using simple HSV sampling."""
    cols = []
    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.12, 0.28); v = random.uniform(0.92, 1.00)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.85, 1.00); v = random.uniform(0.85, 1.00)
        elif mode == "mono":
            h = base_h; s = random.uniform(0.25, 0.65); v = random.uniform(0.55, 1.00)
        else:
            h = random.random(); s = random.uniform(0.30, 1.00); v = random.uniform(0.55, 1.00)
        cols.append(tuple(hsv_to_rgb([h, s, v])))
    return cols

def draw_week3_poster(n_layers=12, wobble=0.12, palette_mode="pastel", seed=None,
                      points=200, r_min=0.18, r_max=0.48, a_min=0.30, a_max=0.65,
                      figsize=(7, 10), dpi=300, bg_gray=0.98,
                      title="Generative Poster", subtitle="Week 3 • Made by Boyang Wang"):
    if seed is not None:
        random.seed(int(seed)); np.random.seed(int(seed))
    else:
        random.seed(); np.random.seed(None)

    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = plt.gca()
    ax.set_axis_off()
    ax.set_facecolor((bg_gray, bg_gray, bg_gray))

    palette = make_palette(8, mode=palette_mode)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(r_min, r_max)
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble, points=points)
        color = random.choice(palette)
        alpha = random.uniform(a_min, a_max)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    ax.text(0.05, 0.95, f"{title} • {palette_mode}", fontsize=14, weight="bold", transform=ax.transAxes)
    ax.text(0.05, 0.91, subtitle, fontsize=10, transform=ax.transAxes)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    return fig

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Week 3 • Generative Poster", layout="centered")
st.title("Generative Poster (Week 3)")
st.caption("Random palette • Blob layering • Seed reproducibility • Simple export")

with st.sidebar:
    st.header("Parameters")
    n_layers = st.slider("Layers", 4, 36, 12, 1)
    wobble = st.slider("Wobble", 0.02, 0.30, 0.12, 0.005)
    palette_mode = st.selectbox("Palette", ["pastel", "vivid", "mono", "random"], index=0)
    seed_mode = st.radio("Random seed", ["Random each run", "Fixed value"], index=0)
    seed_value = st.number_input("Seed value", value=7, step=1)

    st.subheader("Geometry / Alpha")
    points = st.slider("Outline points", 50, 800, 200, 10)
    r_min = st.slider("Radius min", 0.05, 0.80, 0.18)
    r_max = st.slider("Radius max", 0.06, 0.90, 0.48)
    a_min = st.slider("Alpha min", 0.05, 1.00, 0.30, 0.01)
    a_max = st.slider("Alpha max", 0.05, 1.00, 0.65, 0.01)

    st.subheader("Canvas")
    fig_w = st.slider("Width (in)", 4.0, 16.0, 7.0)
    fig_h = st.slider("Height (in)", 4.0, 20.0, 10.0)
    dpi = st.slider("DPI", 72, 600, 300)
    bg_gray = st.slider("Background gray", 0.90, 1.00, 0.98)

    st.subheader("Labels")
    title = st.text_input("Title", "Generative Poster")
    subtitle = st.text_input("Subtitle", "Week 3 • Made by Boyang Wang")

seed_to_use = int(seed_value) if seed_mode == "Fixed value" else None

fig = draw_week3_poster(
    n_layers=n_layers, wobble=wobble, palette_mode=palette_mode, seed=seed_to_use,
    points=points, r_min=r_min, r_max=r_max, a_min=a_min, a_max=a_max,
    figsize=(fig_w, fig_h), dpi=dpi, bg_gray=bg_gray, title=title, subtitle=subtitle
)

st.pyplot(fig, use_container_width=True)

png_buf = io.BytesIO()
fig.savefig(png_buf, format="png", dpi=dpi, bbox_inches="tight", pad_inches=0.1)
st.download_button("Download PNG", data=png_buf.getvalue(), file_name="week3_poster.png", mime="image/png")

pdf_buf = io.BytesIO()
fig.savefig(pdf_buf, format="pdf", bbox_inches="tight", pad_inches=0.1)
st.download_button("Download PDF", data=pdf_buf.getvalue(), file_name="week3_poster.pdf", mime="application/pdf")

svg_buf = io.BytesIO()
fig.savefig(svg_buf, format="svg", bbox_inches="tight", pad_inches=0.1)
st.download_button("Download SVG", data=svg_buf.getvalue(), file_name="week3_poster.svg", mime="image/svg+xml")
