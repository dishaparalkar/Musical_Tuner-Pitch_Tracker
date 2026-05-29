import sounddevice as sd
import numpy as np
import threading

# ==========================================================
# SETTINGS
# ==========================================================
FS = 16000               # Sampling frequency
DURATION = 0.2          # Audio chunk duration (seconds)
BLOCKSIZE = int(FS * DURATION)

NOTES = [
    'C', 'C#', 'D', 'D#', 'E', 'F',
    'F#', 'G', 'G#', 'A', 'A#', 'B'
]

# ==========================================================
# GLOBAL VARIABLES
# ==========================================================

# Latest tuner information will share to UI
latest_data = {
    "frequency": 440.0,
    "note": "A4",
    "standard": 440.0,
    "standard_frequency": 440.0,
    "status": "In Tune",
    "cents": 0,
    "waveform": [],
    "fft_freqs": [],
    "fft_magnitude": []
}

# Latest waveform data (for live plot)
latest_waveform = np.zeros(1024)
# Latest FFT data (for live plot)
latest_fft_freqs = np.linspace(0, 1000, 512)
latest_fft_magnitude = np.zeros(512)

# Frequency smoothing buffer
freq_buffer = []

# Stream control
stream = None
running = False
stream_thread = None

# Thread lock for safe access
data_lock = threading.Lock()


# ==========================================================
# AUDIO PROCESSING (Main Fuction)
# ==========================================================
def process_audio(indata): #microphone input comes here
    """
    Process microphone audio and update:
    - frequency
    - note
    - status
    - cents
    - waveform
    - FFT spectrum
    """
    global freq_buffer
    global latest_waveform
    global latest_fft_freqs
    global latest_fft_magnitude

    # Flatten to 1D array
    audio = indata.flatten()

    # Save waveform for plotting
    with data_lock:
        latest_waveform = audio.copy()

    # Ignore silence
    if np.max(np.abs(audio)) < 0.01:
        return

    # Apply Hamming window to smooth edges results clean FFT & better peak detection 
    window = np.hamming(len(audio))
    audio_windowed = audio * window

    # FFT (time domain signal to Frequency domain signal)
    fft = np.fft.fft(audio_windowed)
    frequencies = np.fft.fftfreq(len(audio_windowed), 1 / FS)
    magnitude = np.abs(fft)

    # Keep only positive frequencies because Neg Freq are mirror image 
    half = len(frequencies) // 2
    frequencies = frequencies[:half]
    magnitude = magnitude[:half]

    # Restrict useful range
    min_freq = 50
    max_freq = 1000

    valid = np.where(
        (frequencies >= min_freq) &
        (frequencies <= max_freq)
    )[0]

    if len(valid) == 0:
        return

    freqs = frequencies[valid]
    mags = magnitude[valid]

    if len(mags) == 0:
        return
    
    # Smooth FFT magnitude to reduce noisy peaks by Convolve( avg nearby points)
    mags = np.convolve( 
        mags,
        np.ones(5) / 5,
        mode='same'
    )

    # Save FFT data for plotting
    with data_lock:
        latest_fft_freqs = freqs.copy()
        latest_fft_magnitude = mags.copy()

    # Peak detection (strongest frequency)
    peak_index = np.argmax(mags)
    peak_freq = freqs[peak_index]

    if peak_freq <= 0:
        return

    # Smooth frequency
    freq_buffer.append(peak_freq) #store recent frequencies
    if len(freq_buffer) > 5:
        freq_buffer.pop(0)

    peak_freq = sum(freq_buffer) / len(freq_buffer) #avg them

    # Calculate note number relative to A4 = 440 Hz
    n = 12 * np.log2(peak_freq / 440.0)
    n_rounded = int(round(n))

    # Determine note and octave
    note_index = (n_rounded + 9) % 12
    note_name = NOTES[note_index]
    octave = 4 + (n_rounded + 9) // 12
    full_note = f"{note_name}{octave}"

    # Ideal frequency of nearest note
    ideal_freq = 440.0 * (2 ** (n_rounded / 12))

    # Cents error imp for tuner
    cents = int(round(
        1200 * np.log2(peak_freq / ideal_freq)
    ))

    # Tuning status
    if abs(cents) <= 5:
        status = "In Tune"
    elif cents > 0:
        status = "Sharp"
    else:
        status = "Flat"

    # Update shared data
    with data_lock:
       latest_data.update({
        "frequency": round(peak_freq, 2),
        "note": full_note,
        "standard": round(ideal_freq, 2),
        "standard_frequency": round(ideal_freq, 2),
        "status": status,
        "cents": cents,
        "waveform": latest_waveform.tolist(),
        "fft_freqs": latest_fft_freqs.tolist(),
        "fft_magnitude": latest_fft_magnitude.tolist(),
    })

    # Terminal output
    print(
        f"\r{peak_freq:.1f} Hz | {full_note} | "
        f"{status} ({cents:+d} cents)",
        end=""
    )





# ==========================================================
# CALLBACK
# ==========================================================
def callback(indata, frames, time, status):
    if status:
        print(status)
    process_audio(indata)


# ==========================================================
# STREAM LOOP
# ==========================================================
def _stream_loop():
    global running

    print("Real-time tuner started... Press Stop to end.")

    try:
        with sd.InputStream(
            callback=callback,
            channels=1,
            samplerate=FS,
            blocksize=BLOCKSIZE
        ):
            while running:
                sd.sleep(100)

    except Exception as e:
        print(f"\nAudio error: {e}")

    print("\nStopping...")


# ==========================================================
# PUBLIC FUNCTIONS
# ==========================================================
def start_tuner():
    """
    Start tuner in background thread.
    """
    global running, stream_thread

    if running:
        return

    running = True
    stream_thread = threading.Thread(
        target=_stream_loop,
        daemon=True
    )
    stream_thread.start()


def stop_tuner():
    """
    Stop tuner safely.
    """
    global running
    global freq_buffer

    running = False

    # Clear smoothing buffer
    freq_buffer.clear()

    # Update status only
    with data_lock:
        latest_data["status"] = "Stopped"

def get_tuner_data():
    """
    Return latest data for Streamlit dashboard.
    """
    with data_lock:
        return {
            "frequency": latest_data["frequency"],
            "note": latest_data["note"],
            "status": latest_data["status"],
            "cents": latest_data["cents"],
            "waveform": latest_waveform.copy(),
            "fft_freqs": latest_fft_freqs.copy(),
            "fft_magnitude": latest_fft_magnitude.copy()
        }
def get_waveform():
    return latest_data["waveform"]

def get_fft_data():
    return latest_data["fft_freqs"], latest_data["fft_magnitude"]

# ==========================================================
# TERMINAL TEST MODE
# ==========================================================
if __name__ == "__main__":
    try:
        start_tuner()
        while True:
            sd.sleep(100)
    except KeyboardInterrupt:
        stop_tuner()
        print("\nStopped tuner.")