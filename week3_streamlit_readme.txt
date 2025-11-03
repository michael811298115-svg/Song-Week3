Week3 Generative Poster — Streamlit Edition
===========================================

This app converts the original matplotlib-based notebook script into an interactive Streamlit app,
keeping the original core logic (random_palette, blob, and layered draws) while adding UI controls
and style presets.

How to run
----------
1) Install dependencies:
   pip install streamlit numpy matplotlib

2) Launch the app:
   streamlit run week3_streamlit_app.py

Features
--------
- Palettes: Random / Pastel / Vivid / Monochrome
- Style presets: Minimal / Vivid / NoiseTouch
- Full control for layers, wobble range, radius range, seed, figure size, and background
- Reproducibility via a fixed seed
- Save & download 300-dpi PNG outputs directly from the app

Notes
-----
- Core math & draw logic mirrors the uploaded Week3 script; only the UI flow changed to Streamlit.
- For exactly reproducible images, ensure the same seed and parameters.
