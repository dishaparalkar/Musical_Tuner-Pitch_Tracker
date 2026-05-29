# 🎵 Musical Tuner & Pitch Tracker
Real-time Musical Tuner and Pitch Tracker using Digital Signal Processing (DSP), FFT, Python, and Streamlit.

## Overview

Musical Tuner & Pitch Tracker is a real-time audio signal processing application developed using Python and Digital Signal Processing (DSP) techniques. The system captures live microphone input, estimates the dominant pitch frequency using Fast Fourier Transform (FFT), and maps the detected frequency to the nearest musical note.

The application provides real-time visualizations including waveform display, FFT spectrum, peak detection, tuning meter, note mapping, cents error analysis, and pitch trend monitoring through an interactive Streamlit dashboard.

---

## Features

* Real-time microphone audio acquisition
* Time-domain waveform visualization
* FFT-based frequency spectrum analysis
* Dominant frequency detection
* Musical note mapping
* Cents error calculation
* Sharp / Flat / In Tune indication
* Pitch trend visualization
* Interactive Streamlit dashboard

---

## DSP Techniques Used

* Audio Sampling (16 kHz)
* Hamming Windowing
* Fast Fourier Transform (FFT)
* Frequency Spectrum Analysis
* Peak Detection
* Frequency Smoothing
* Musical Note Mapping
* Cents Error Calculation

---

## Technologies Used

* Python
* NumPy
* SoundDevice
* Streamlit
* Matplotlib

---

## Project Structure

```text
Musical_Tuner-Pitch_Tracker/
│
├── Backend/
│   └── realtime_tuner_phs4.py
│
├── Frontend/
│   └── tuner_ui.py
│
├── Screenshots/
│   └── Project screenshots
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dishaparalkar/Musical_Tuner-Pitch_Tracker.git
cd Musical_Tuner-Pitch_Tracker
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Start the Backend

Open a terminal and run:

```bash
python Backend/realtime_tuner_phs4.py
```

### Launch the Streamlit Dashboard

Open another terminal and run:

```bash
streamlit run Frontend/tuner_ui.py
```

The dashboard will open automatically in your browser.

---

## Screenshots

The `Screenshots` folder contains sample outputs including:

* Dashboard
* Time Domain Signal
* FFT Spectrum
* Peak Detection
* Note Mapping
* Tuning Meter
* Cents Error Analysis
* Frequency Trend Analysis
* Stability Analysis

---

## Applications

* Musical Instrument Tuning
* Audio Signal Analysis
* DSP Education and Demonstration
* Real-Time Pitch Tracking

---

## Author

**Disha Paralkar**

BS in Electronic Systems

Indian Institute of Technology Madras (IIT Madras)

