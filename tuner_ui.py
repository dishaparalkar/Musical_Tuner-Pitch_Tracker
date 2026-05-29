import time
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go


from Backend.realtime_tuner_phs4 import latest_data
# Backend imports
from Backend.realtime_tuner_phs4 import (
    get_tuner_data,
    start_tuner,
    stop_tuner,
    DURATION,
)
if "pitch_history" not in st.session_state:
    st.session_state.pitch_history = []
if "page" not in st.session_state:
    st.session_state.page = "welcome"
# =====================================================
# Page Configuration
# =====================================================
st.set_page_config(
    page_title="Musical Tuner & Pitch Tracker",
    page_icon="🎵",
    layout="wide",
)

# =====================================================
# Session State
# =====================================================
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if "tuner_running" not in st.session_state:
    st.session_state.tuner_running = False

if "input_mode" not in st.session_state:
    st.session_state.input_mode = "Chromatic"

# =====================================================
# Auto Refresh While Running
# =====================================================
if st.session_state.tuner_running:
    st_autorefresh(interval=500, key="tuner_refresh")

# CSS Styling
# =====================================================
st.markdown(
    """
    <style>

    .stApp {
        background: radial-gradient(
            circle at top,
            rgba(25, 10, 50, 0.25),
            #020617 70%
        );
        color: white;
    }

    /* Remove unwanted empty blocks */
    div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }

    /* Remove background from all Streamlit containers */
    div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Hide the first empty block that creates the top rectangle */
    .main-card::before {
        display: none !important;
        content: none !important;
    }

    /* Main Card */
    .main-card {
        position: relative;
        max-width: 1100px;
        margin: 20px auto;
        padding: 40px 32px;
        border-radius: 28px;
        background: radial-gradient(
            circle at top,
            rgba(80, 30, 150, 0.10),
            rgba(0, 0, 0, 0.85)
        );
        border: 1px solid rgba(139, 92, 246, 0.20);
        box-shadow: 0 0 40px rgba(139, 92, 246, 0.08);
        overflow: hidden;
    }

    /* Title */
    .title {
        text-align: center;
        font-size: 4.4rem;
        line-height: 1.05;
        font-weight: 800;
        margin-bottom: 18px;
        background: linear-gradient(90deg, #8b5cf6, #a855f7, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #d1d5db;
        font-size: 1.55rem;
        line-height: 1.6;
        max-width: 820px;
        margin: 0 auto 28px auto;
    }

    /* Dividers */
    .divider,
    .footer-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin: 28px 0;
    }

    /* Input Heading */
    .input-heading {
        color: white;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 16px;
    }

    /* Input Description */
    .input-description {
        color: #9ca3af;
        text-align: center;
        font-size: 1rem;
        margin-top: 12px;
        margin-bottom: 8px;
    }

/* =========================================
   PERFECTLY CENTERED INPUT OPTIONS
========================================= */

/* Full width radio widget */
div[data-testid="stRadio"] {
    width: 100% !important;
}

/* Internal wrapper */
div[data-testid="stRadio"] > div {
    width: 100% !important;
}

/* Actual horizontal options container */
div[data-testid="stRadio"] > div > div {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 180px !important;   /* Space between options */
    width: 100% !important;
    margin: 0 auto !important;
}

/* Each option container */
div[data-testid="stRadio"] > div > div > label {
    display: flex !important;
    align-items: center !important;
    gap: 50px !important;    /* Space between radio circle and text */
    margin: 0 !important;
    white-space: nowrap !important;
}

/* Text only */
div[data-testid="stRadio"] label p {
    margin: 0 !important;
    color: white !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
}

/* Radio circle only */
div[data-testid="stRadio"] input[type="radio"] {
    transform: scale(1.3);
}

/* Description below */
.input-description {
    color: #9ca3af;
    text-align: center;
    font-size: 1.1rem;
    margin-top: 24px;
    margin-bottom: 8px;
}

    /* Author */
    .author {
        text-align: center;
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 8px;
    }

    .author-sub {
        text-align: center;
        color: #9ca3af;
        font-size: 1.15rem;
        margin-bottom: 20px;
    }

    /* Launch Button */
    div.stButton > button {
        background: rgba(10, 8, 25, 0.95);
        color: #a855f7;
        font-size: 1.35rem;
        font-weight: 700;
        height: 4.4rem;
        border-radius: 18px;
        border: 2px solid #7c3aed;
        box-shadow:
            0 0 18px rgba(124, 58, 237, 0.25),
            inset 0 0 12px rgba(124, 58, 237, 0.05);
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background: rgba(18, 12, 40, 1);
        color: #c084fc;
        border-color: #a855f7;
        box-shadow:
            0 0 28px rgba(168, 85, 247, 0.45),
            0 0 60px rgba(124, 58, 237, 0.18);
        transform: translateY(-2px);
    }

    /* Feature Cards */
    .feature-card {
        background: rgba(17, 24, 39, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 26px 22px;
        min-height: 170px;
    }

    .feature-icon {
        font-size: 2.4rem;
        margin-bottom: 12px;
    }

    .feature-title {
        color: white;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .feature-desc {
        color: #cbd5e1;
        font-size: 0.98rem;
        line-height: 1.6;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)
# =====================================================
# =====================================================
# PAGE ROUTING
# =====================================================
if st.session_state.page == "history":

    import pandas as pd

    # -----------------------------------------------
    # Header: Title + Small Back Icon
    # -----------------------------------------------
    header_left, header_right = st.columns([8, 1])

    with header_left:
        st.title("📜 History & Export")

    with header_right:
        st.write("")  # vertical alignment
        if st.button("⬅", use_container_width=True, help="Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    # -----------------------------------------------
    # Load History Data
    # -----------------------------------------------
    history = st.session_state.pitch_history

    if not history:
        st.info("No pitch history available yet.")
        st.stop()

    # Convert to DataFrame
    df = pd.DataFrame(history)
    df["Timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    export_df = df[
        ["Timestamp", "frequency", "note", "cents", "status"]
    ].rename(
        columns={
            "frequency": "Frequency (Hz)",
            "note": "Note",
            "cents": "Cents Error",
            "status": "Status",
        }
    )

    # -----------------------------------------------
    # Summary Metrics
    # -----------------------------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Samples", len(export_df))
    c2.metric(
        "Average Frequency",
        f"{export_df['Frequency (Hz)'].mean():.2f} Hz"
    )
    c3.metric(
        "Average Cents",
        f"{export_df['Cents Error'].mean():+.2f}"
    )

    in_tune_pct = (
        (export_df["Status"] == "In Tune").sum()
        / len(export_df)
        * 100
    )
    c4.metric("In Tune %", f"{in_tune_pct:.1f}%")

    st.divider()

    # -----------------------------------------------
    # Frequency History Plot
    # -----------------------------------------------
    st.subheader("📈 Frequency History")
    st.line_chart(
        export_df.set_index("Timestamp")["Frequency (Hz)"],
        height=300,
    )

    # -----------------------------------------------
    # Cents Error Plot
    # -----------------------------------------------
    st.subheader("🎯 Cents Error History")
    st.line_chart(
        export_df.set_index("Timestamp")["Cents Error"],
        height=300,
    )

    st.divider()

    # -----------------------------------------------
    # Measurement Table
    # -----------------------------------------------
    st.subheader("📋 Measurement Table")
    st.dataframe(
        export_df.tail(100),
        use_container_width=True,
        height=400,
    )

    st.divider()

    # -----------------------------------------------
    # Export + Clear Buttons
    # -----------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        csv_data = export_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download CSV Report",
            csv_data,
            "pitch_history_report.csv",
            "text/csv",
            use_container_width=True,
        )

    with col2:
        if st.button("🗑 Clear History", use_container_width=True):
            st.session_state.pitch_history = []
            st.rerun()

    # Stop here so dashboard does not render
    st.stop()
# =====================================================
# Plot Helpers
# =====================================================
def create_waveform_plot(waveform):
    fig, ax = plt.subplots(figsize=(14, 4))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    if waveform is not None and len(waveform) > 0:
        time_axis = np.linspace(0, DURATION, len(waveform))
        ax.plot(time_axis, waveform, linewidth=2)
        ax.set_title("Time Domain Signal", color="white")
        ax.set_xlabel("Time(s)", color="white")
        ax.set_ylabel("Amplitude", color="white")
        ax.grid(True, alpha=0.2)
    else:
        ax.text(
            0.5,
            0.5,
            "No Data",
            ha="center",
            va="center",
            color="white"
        )

    ax.tick_params(colors="white")

    for spine in ax.spines.values():
        spine.set_color("#334155")

    fig.tight_layout()
    return fig

def create_fft_plot(freqs, mags):
    fig, ax = plt.subplots(figsize=(14, 4))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    if (
    freqs is not None and len(freqs) > 0 and
    mags is not None and len(mags) > 0
):
        ax.plot(freqs, mags, linewidth=2)
        ax.set_title("FFT Frequency Spectrum", color="white")
        ax.set_xlabel("Frequency (Hz)", color="white")
        ax.set_ylabel("Magnitude", color="white")
        ax.set_xlim(0, 1000)
    else:
        ax.text(0.5, 0.5, "No Data", ha="center", va="center", color="white")

    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#334155")

    return fig

# =====================================================
# Welcome Page
# =====================================================
if not st.session_state.app_started:

    # Single centered container (no empty side columns)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    # Title
    st.markdown(
        '<div class="title">Musical Tuner & Pitch Tracker</div>',
        unsafe_allow_html=True,
    )

    # Subtitle
    st.markdown(
        """
        <div class="subtitle">
            Real-Time Pitch Detection and Musical Note Estimation<br>
            Using FFT and Digital Signal Processing
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Input Type Section
    # Input Type Section
    st.markdown(
        '<div class="input-heading">🎙️ Select Input Type</div>',
        unsafe_allow_html=True,
    )

    # Centered radio options using columns
    left_space, center_col, right_space = st.columns([1, 3, 1])

    with center_col:
        input_type = st.radio(
            "",
            ["🎤 Vocals", "🎸 Instrument", "🎼 Chromatic"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )

# Description based on selected mode
        descriptions = {
           "🎤 Vocals": "Optimized for human voice and singing.",
           "🎸 Instrument": "Designed for guitar, violin, flute, and other instruments.",
           "🎼 Chromatic": "General-purpose mode for any monophonic sound.",
        }

        st.markdown(
           f'<div class="input-description">{descriptions[input_type]}</div>',
            unsafe_allow_html=True,
        )

    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Author
    st.markdown(
        '<div class="author">👤 Disha Paralkar</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="author-sub">IIT Madras – BS in Electronic Systems</div>',
        unsafe_allow_html=True,
    )

    # Launch Button (centered)
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        if st.button(
            "🚀 Launch Application",
            use_container_width=True,
        ):
            st.session_state.app_started = True
            st.session_state.input_mode = input_type
            st.rerun()

    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Feature Cards
    feature_cols = st.columns(3)

    features = [
        (
            "🎤",
            "Live Audio Input",
            "Capture sound in real-time through your microphone.",
        ),
        (
            "📊",
            "FFT Analysis",
            "Detect the dominant frequency using Fast Fourier Transform.",
        ),
        (
            "🎼",
            "Note Detection",
            "Map frequency to the nearest musical note with accuracy.",
        ),
    ]

    for col, (icon, title, desc) in zip(feature_cols, features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Footer Divider
    st.markdown('<div class="footer-divider"></div>', unsafe_allow_html=True)

    # Footer
    st.markdown(
        """
        <div class="footer">
            💜 Built with Streamlit • Python • DSP • Real-Time Audio
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Close main card
    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()
# =====================================================
# DSP Dashboard
# =====================================================



# Controls
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("▶ Start Tuner", use_container_width=True):
        start_tuner()   # Start backend microphone processing
        st.session_state.tuner_running = True
        st.rerun()

with c2:
    if st.button("■ Stop Tuner", use_container_width=True):
        stop_tuner()    # Stop backend processing
        st.session_state.tuner_running = False
        st.rerun()

with c3:
    if st.button("⬅ Back", use_container_width=True):
        if st.session_state.tuner_running:
            stop_tuner()
            st.session_state.tuner_running = False

        st.session_state.app_started = False
        st.rerun()


# Dashboard Header
header_left, header_right = st.columns([8, 1])

with header_left:
    st.title("🎵 Musical Tuner Dashboard")

with header_right:
    st.write("")  # Align vertically
    if st.button("📜", use_container_width=True, help="History & Export"):
        st.session_state.page = "history"
        st.rerun()
# -----------------------------------------------------
# Current Data from Backend
# -----------------------------------------------------
data = get_tuner_data()

# Read all live values from backend
frequency = float(data.get("frequency", 0.0))
note = data.get("note", "--")
status = data.get("status", "--")
cents = int(data.get("cents", 0))

# Get standard/reference frequency directly from backend
standard_freq = float(
    data.get("standard", data.get("standard_frequency", 0.0))
)

# Arrays used for plots
waveform = data.get("waveform", [])
fft_freqs = data.get("fft_freqs", [])
fft_magnitude = data.get("fft_magnitude", [])

from datetime import datetime

# Store only valid readings
if frequency > 0 and note != "--":
    st.session_state.pitch_history.append({
        "timestamp": datetime.now(),
        "frequency": frequency,
        "note": note,
        "cents": cents,
        "status": status,
    })

# Keep last 200 samples
if len(st.session_state.pitch_history) > 200:
    st.session_state.pitch_history = (
        st.session_state.pitch_history[-200:]
    )

# Arrays for plots
waveform = data.get("waveform", [])
fft_freqs = data.get("fft_freqs", [])
fft_magnitude = data.get("fft_magnitude", [])

# -----------------------------------------------------
# Standard Frequency Lookup
# -----------------------------------------------------
NOTE_FREQUENCIES = {
    "C0": 16.35, "C#0": 17.32, "D0": 18.35, "D#0": 19.45,
    "E0": 20.60, "F0": 21.83, "F#0": 23.12, "G0": 24.50,
    "G#0": 25.96, "A0": 27.50, "A#0": 29.14, "B0": 30.87,
    "C1": 32.70, "C#1": 34.65, "D1": 36.71, "D#1": 38.89,
    "E1": 41.20, "F1": 43.65, "F#1": 46.25, "G1": 49.00,
    "G#1": 51.91, "A1": 55.00, "A#1": 58.27, "B1": 61.74,
    "C2": 65.41, "C#2": 69.30, "D2": 73.42, "D#2": 77.78,
    "E2": 82.41, "F2": 87.31, "F#2": 92.50, "G2": 98.00,
    "G#2": 103.83, "A2": 110.00, "A#2": 116.54, "B2": 123.47,
    "C3": 130.81, "C#3": 138.59, "D3": 146.83, "D#3": 155.56,
    "E3": 164.81, "F3": 174.61, "F#3": 185.00, "G3": 196.00,
    "G#3": 207.65, "A3": 220.00, "A#3": 233.08, "B3": 246.94,
    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13,
    "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00,
    "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88,
    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25,
    "E5": 659.25, "F5": 698.46, "F#5": 739.99, "G5": 783.99,
    "G#5": 830.61, "A5": 880.00, "A#5": 932.33, "B5": 987.77
}


# -----------------------------------------------------
# Live Metrics
# -----------------------------------------------------
m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Frequency", f"{frequency:.2f} Hz")
m2.metric("Note", note)
m3.metric("Standard", f"{standard_freq:.2f} Hz" if standard_freq else "--")
m4.metric("Cents Error", f"{cents:+d}")
m5.metric("Status", status)

st.divider()

# -----------------------------------------------------
# Tabs
# -----------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Waveform",
    "📊 FFT Spectrum",
    "🎯 Peak Detection",
    "🎼 Note Mapping",
    "🧮 Cents Error",
    "🎛️ Tuning Meter",
    "📈 Pitch Trend"
])
# -----------------------------------------------------
# 1. Waveform Tab
# -----------------------------------------------------
with tab1:
    st.subheader("Time-Domain Signal")
    st.write("Raw microphone samples captured in real time.")

    if waveform is not None and len(waveform) > 0:
        waveform_fig = create_waveform_plot(waveform)
        st.pyplot(waveform_fig, width="stretch")
    else:
        st.info("No waveform data available yet.")

# -----------------------------------------------------
# 2. FFT Spectrum Tab
# -----------------------------------------------------
with tab2:
    st.subheader("Frequency Spectrum")
    st.write("Frequency-domain representation of the audio signal using Fast Fourier Transform (FFT).")

    if (
    fft_freqs is not None and len(fft_freqs) > 0 and
    fft_magnitude is not None and len(fft_magnitude) > 0
):
        fft_fig = create_fft_plot(fft_freqs, fft_magnitude)
        st.pyplot(fft_fig, width="stretch")
    else:
        st.info("No FFT data available yet.")

# =====================================================
# 3. Peak Detection
# =====================================================
with tab3:
    st.subheader("🎯 Peak Detection")
    st.write(
        "The dominant frequency is identified by finding the highest magnitude "
        "peak in the FFT spectrum within the valid pitch range."
    )

    # Extract FFT data
    fft_freqs = data.get("fft_freqs", [])
    fft_magnitude = data.get("fft_magnitude", [])
    frequency = float(data.get("frequency", 0.0))

    # Display summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Dominant Frequency", f"{frequency:.2f} Hz")

    with col2:
        if len(fft_magnitude) > 0:
            peak_mag = max(fft_magnitude)
            st.metric("Peak Magnitude", f"{peak_mag:.4f}")
        else:
            st.metric("Peak Magnitude", "N/A")

    with col3:
        st.metric("Search Range", "50–2000 Hz")

    st.markdown("---")

    # Plot FFT with highlighted peak
    if len(fft_freqs) > 0 and len(fft_magnitude) > 0:
        fig = go.Figure()

        # FFT spectrum line
        fig.add_trace(
            go.Scatter(
                x=fft_freqs,
                y=fft_magnitude,
                mode="lines",
                name="FFT Spectrum",
                line=dict(color="#00d4ff", width=2),
            )
        )

        # Highlight dominant peak
        if len(fft_magnitude) > 0 :
            
            peak_idx = np.argmax(fft_magnitude)
            peak_x = fft_freqs[peak_idx]
            peak_y = fft_magnitude[peak_idx]

            fig.add_trace(
                go.Scatter(
                    x=[peak_x],
                    y=[peak_y],
                    mode="markers+text",
                    marker=dict(
                        size=15,
                        color="red",
                        line=dict(color="white", width=3),
                    ),
                    text=[f"{peak_x:.2f} Hz"],
                    textposition="top center",
                    name="Detected Peak",
                )
            )

        fig.update_layout(
            template="plotly_dark",
            height=500,
            title="FFT Spectrum with Detected Peak",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,10,20,0.95)",
            margin=dict(l=40, r=40, t=60, b=40),
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No FFT data available yet. Start the tuner to analyze audio.")

    st.markdown("---")

    # Explanation section
    st.markdown(
        """
### 📘 How Peak Detection Works

1. Microphone audio is converted into digital samples.
2. Fast Fourier Transform (FFT) converts the signal into the frequency domain.
3. The spectrum contains peaks at frequencies present in the sound.
4. The largest peak is selected as the fundamental frequency.
5. This frequency is used to determine the nearest musical note.

### Example
If the strongest peak occurs at **440 Hz**, the detected note is **A4**.
"""
    )
# -----------------------------------------------------
# =====================================================
# 4. Note Mapping
# =====================================================
with tab4:
    st.subheader("🎼 Note Mapping")
    st.write(
        "The detected frequency is mapped to the nearest musical note "
        "using the equal-tempered tuning system with A4 = 440 Hz."
    )

    # Extract data
    frequency = float(data.get("frequency", 0.0))
    note = data.get("note", "--")
    standard_freq = float(data.get("standard_frequency", 440.0))

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Detected Frequency", f"{frequency:.2f} Hz")

    with col2:
        st.metric("Nearest Note", note)

    with col3:
        st.metric("Standard Frequency", f"{standard_freq:.2f} Hz")

    st.markdown("---")

    # Piano-style visualization
    notes = [
        "C", "C#", "D", "D#", "E", "F",
        "F#", "G", "G#", "A", "A#", "B"
    ]

    # Extract note name without octave
    if note and note != "--":
        if len(note) >= 2 and note[1] == "#":
            note_name = note[:2]
        else:
            note_name = note[:1]
    else:
        note_name = None

    cols = st.columns(len(notes))

    for col, n in zip(cols, notes):
        with col:
            if n == note_name:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, #7c3aed, #a855f7);
                        color: white;
                        text-align: center;
                        padding: 18px 6px;
                        border-radius: 12px;
                        font-weight: 700;
                        box-shadow: 0 0 20px rgba(168, 85, 247, 0.45);
                    ">
                        {n}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        background: rgba(17, 24, 39, 0.75);
                        color: #cbd5e1;
                        text-align: center;
                        padding: 18px 6px;
                        border-radius: 12px;
                        border: 1px solid rgba(255,255,255,0.06);
                    ">
                        {n}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("---")



    # Current result
    st.success(
        f"Detected frequency {frequency:.2f} Hz maps to note {note} "
        f"(reference {standard_freq:.2f} Hz)."
    )
# -----------------------------------------------------
# 5. Cents Error Tab
# =====================================================
# 5. Cents Error
# =====================================================
with tab5:
    st.subheader("🧮 Cents Error")
    st.write(
        "Cents measure how far the detected frequency deviates from "
        "the ideal tuning frequency."
    )

    # Extract data
    frequency = float(data.get("frequency", 0.0))
    note = data.get("note", "--")
    cents = int(data.get("cents", 0))
    standard_freq = float(data.get("standard_frequency", 440.0))

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Detected Frequency", f"{frequency:.2f} Hz")

    with col2:
        st.metric("Reference Frequency", f"{standard_freq:.2f} Hz")

    with col3:
        st.metric("Cents Error", f"{cents:+d} cents")

    st.markdown("---")

    # Visual meter
    meter_col1, meter_col2, meter_col3 = st.columns([1, 6, 1])

    with meter_col2:
        # Normalize to percentage across -50 to +50 cents
        clamped = max(-50, min(50, cents))
        percent = ((clamped + 50) / 100) * 100

        # Status text
        if abs(cents) <= 5:
            label = "🎯 In Tune"
            color = "#22c55e"
        elif cents < 0:
            label = "⬇ Flat"
            color = "#3b82f6"
        else:
            label = "⬆ Sharp"
            color = "#ef4444"

        # Meter
        st.markdown(
            f'''
            <div style="text-align:center; margin-bottom:10px;
                        color:{color}; font-weight:700; font-size:1.3rem;">
                {label}
            </div>

            <div style="
                position: relative;
                width: 100%;
                height: 22px;
                border-radius: 12px;
                background: linear-gradient(
                    90deg,
                    #3b82f6 0%,
                    #22c55e 50%,
                    #ef4444 100%
                );
                overflow: hidden;
            ">
                <div style="
                    position: absolute;
                    left: {percent}%;
                    top: -6px;
                    width: 4px;
                    height: 34px;
                    background: white;
                    box-shadow: 0 0 10px rgba(255,255,255,0.8);
                    transform: translateX(-50%);
                "></div>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                color:#94a3b8;
                font-size:0.9rem;
                margin-top:6px;
            ">
                <span>-50¢</span>
                <span>0¢</span>
                <span>+50¢</span>
            </div>
            ''',
            unsafe_allow_html=True,
        )

    st.markdown("---")



    # Final explanation
    st.info(
        f"The note {note} is {cents:+d} cents away from its ideal "
        f"frequency of {standard_freq:.2f} Hz."
    )
# =====================================================
# 6. Tuning Meter
# =====================================================
with tab6:
    st.subheader("🎛️ Tuning Meter")
    st.write(
        "Final tuning decision based on the cents error relative to "
        "the standard frequency."
    )

    # Extract data
    note = data.get("note", "--")
    frequency = float(data.get("frequency", 0.0))
    cents = int(data.get("cents", 0))
    status = data.get("status", "Waiting")
    standard_freq = float(data.get("standard_frequency", 440.0))

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Note", note)

    with col2:
        st.metric("Detected", f"{frequency:.2f} Hz")

    with col3:
        st.metric("Reference", f"{standard_freq:.2f} Hz")

    with col4:
        st.metric("Cents", f"{cents:+d}")
    

    # Determine status color
    if abs(cents) <= 5:
        decision = "🎯 IN TUNE"
        color = "#22c55e"
        glow = "0 0 25px rgba(34,197,94,0.55)"
    elif cents < 0:
        decision = "⬇ TOO FLAT"
        color = "#3b82f6"
        glow = "0 0 25px rgba(59,130,246,0.55)"
    else:
        decision = "⬆ TOO SHARP"
        color = "#ef4444"
        glow = "0 0 25px rgba(239,68,68,0.55)"

    # Needle position for -50 to +50 cents
    clamped = max(-50, min(50, cents))
    percent = ((clamped + 50) / 100) * 100

    

    st.markdown("---")



    # Final summary
    st.success(
        f"{note} detected at {frequency:.2f} Hz "
        f"with a tuning error of {cents:+d} cents."
    )
# =====================================================
# 7. Pitch Trend
# =====================================================
with tab7:
    st.subheader("📈 Pitch Trend")
    st.write(
        "This section shows how the detected pitch and tuning error "
        "change over time during real-time monitoring."
    )

    history = st.session_state.pitch_history

    if not history:
        st.info("No pitch data available yet. Start the tuner.")
    else:
        import pandas as pd

        df = pd.DataFrame(history)

        # Convert timestamp to readable format
        df["Time"] = df["timestamp"].dt.strftime("%H:%M:%S")

        # -------------------------------------------------
        # Summary Metrics
        # -------------------------------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Samples Stored", len(df))

        with col2:
            avg_freq = df["frequency"].mean()
            st.metric("Average Frequency", f"{avg_freq:.2f} Hz")

        with col3:
            avg_cents = df["cents"].mean()
            st.metric("Average Cents Error", f"{avg_cents:+.2f}")

        st.markdown("---")

        # -------------------------------------------------
        # Frequency Trend
        # -------------------------------------------------
        st.markdown("### 🎵 Frequency vs Time")
        st.write(
            "Tracks the detected pitch over time."
        )

        st.line_chart(
            df.set_index("Time")["frequency"],
            height=320,
        )

        st.markdown("---")

        # -------------------------------------------------
        # Cents Error Trend
        # -------------------------------------------------
        st.markdown("### 🎯 Cents Error vs Time")
        st.write(
            "Shows how tuning deviation changes over time."
        )

        st.line_chart(
            df.set_index("Time")["cents"],
            height=320,
        )

        st.markdown("---")

        # -------------------------------------------------
        # Stability Analysis
        # -------------------------------------------------
        st.markdown("### 📘 Stability Analysis")

        freq_std = df["frequency"].std()
        cents_std = df["cents"].std()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Frequency Std Dev", f"{freq_std:.4f} Hz")

        with col2:
            st.metric("Cents Std Dev", f"{cents_std:.4f}")

        if cents_std < 2:
            st.success("Excellent pitch stability.")
        elif cents_std < 5:
            st.info("Good pitch stability.")
        else:
            st.warning("Pitch is fluctuating significantly.")

        
    



