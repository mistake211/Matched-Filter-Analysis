##Another Attempt at MFA

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ===== LOAD PMT DATA =====

# Your random-waveform PMT measurement
PMT_FILE = "C1--LIAAdvancedLab--00012.csv"

df = pd.read_csv(PMT_FILE, skiprows=4)

# Extract time and voltage arrays
time = df["Time"].to_numpy(dtype=float)
pmt = df["Ampl"].to_numpy(dtype=float)

# ===== LOAD RANDOM WAVEFORM =====

WAVEFORM_FILE = "random_laser.raf"

waveform = np.fromfile(
    WAVEFORM_FILE,
    dtype="<u2"
).astype(float)

# Normalize waveform
waveform = waveform - np.mean(waveform)
waveform = waveform / np.max(np.abs(waveform))

# ===== VERIFY DATA =====

print("PMT samples:", len(pmt))
print("Waveform samples:", len(waveform))
print("Sampling frequency:", 1 / np.median(np.diff(time)))

print("All arrays loaded successfully!")
# Test frequencies
test_frequencies = [26450, 27000]

# Divide recording into independent segments
segment_duration = 0.02  # 20 ms

dt = np.median(np.diff(time))
samples_per_segment = int(segment_duration / dt)

num_segments = len(pmt) // samples_per_segment

fig, ax = plt.subplots(figsize=(10, 5))

for f in test_frequencies:

    correlations = []

    for i in range(num_segments):

        start = i * samples_per_segment
        end = start + samples_per_segment

        t = time[start:end]
        M = pmt[start:end] - np.mean(pmt[start:end])

        phase = np.mod(t * f, 1.0)

        indices = np.floor(
            phase * len(waveform)
        ).astype(int)

        R = waveform[indices]
        R = R - np.mean(R)

        # Normalized correlation at the assumed phase
        denominator = np.linalg.norm(M) * np.linalg.norm(R)

        correlation = (
            np.dot(M, R) / denominator
            if denominator > 0 else 0
        )

        correlations.append(correlation)

    ax.plot(
        np.arange(num_segments),
        correlations,
        marker="o",
        label=f"{f} Hz"
    )

ax.axhline(0, color="black", linestyle="--")

ax.set_xlabel("20 ms Segment")
ax.set_ylabel("Normalized Correlation")
ax.set_title("Correlation Consistency Across Time")
ax.legend()
ax.grid()

plt.show()
