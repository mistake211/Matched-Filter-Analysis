#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 15:12:11 2026

An attempt at Matched Filter Analysis
@author: max
"""


# %% IMPORTS

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import correlate, correlation_lags
from pathlib import Path


# %% USER SETTINGS

# Folder containing oscilloscope CSV files
DATA_FOLDER = Path(r"/home/max/Desktop/Advanced Lab/lab data/4th Collection")

# Output folder
OUTPUT_FOLDER = DATA_FOLDER / "Matched_Filter_Results"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# File numbers
FILE_NUMBERS = range(11, 19)

# Modulation type for each recording
MODULATION = {
    11: "27kHz",
    12: "Random",
    13: "Random",
    14: "27kHz",
    15: "27kHz",
    16: "Random",
    17: "Random",
    18: "27kHz"
}

# High-power random-waveform measurement
REFERENCE_FILE = 12

# CSV column positions (zero-indexed)
# Change these if your CSV format is different
TIME_COLUMN = 0
VOLTAGE_COLUMN = 1

# Set to None to search all delays.
# After inspecting the high-power measurement, you can
# specify a smaller window around the expected delay.
MAX_DELAY_SECONDS = None


# %% LOAD OSCILLOSCOPE DATA

def load_scope_csv('/home/max/Desktop/Advanced Lab/lab data/4th Collection'):
    """
    Load a CSV containing time and voltage.

    """

    df = pd.read_csv(filename, header=None, comment="#")

    time = pd.to_numeric(
        df.iloc[:, TIME_COLUMN], errors="coerce"
    )

    voltage = pd.to_numeric(
        df.iloc[:, VOLTAGE_COLUMN], errors="coerce"
    )

    valid = time.notna() & voltage.notna()

    time = time[valid].to_numpy(dtype=float)
    voltage = voltage[valid].to_numpy(dtype=float)

    if len(time) < 2:
        raise ValueError(f"Not enough samples in {filename}")

    if not np.all(np.diff(time) > 0):
        raise ValueError(
            f"Time values are not increasing in {filename}"
        )

    return time, voltage


# %% LOAD ALL MEASUREMENTS

data = {}

for number in FILE_NUMBERS:

    suffix = f"{number:05d}"

    pmt_file = DATA_FOLDER / (
        f"C1--LIAAdvancedLab--00011.csv"
    )

    lia_file = DATA_FOLDER / (
        f"C2--LIAAdvancedLab--{suffix}.csv"
    )

    t_pmt, pmt = load_scope_csv(pmt_file)
    t_lia, lia = load_scope_csv(lia_file)

    data[number] = {
        "time": t_pmt,
        "pmt": pmt,
        "lia_time": t_lia,
        "lia": lia,
        "modulation": MODULATION[number]
    }

    print(
        f"Loaded {suffix}: "
        f"{MODULATION[number]}, "
        f"{len(pmt)} PMT samples"
    )


# %% CONSTRUCT MATCHED FILTER REFERENCE

# High-power random waveform PMT measurement
ref_time = data[REFERENCE_FILE]["time"]
ref_signal = data[REFERENCE_FILE]["pmt"]

# Remove DC offset
ref_signal = ref_signal - np.mean(ref_signal)

# Normalize reference amplitude
ref_scale = np.max(np.abs(ref_signal))

if ref_scale == 0:
    raise ValueError("Reference signal has zero amplitude")

ref_signal = ref_signal / ref_scale

plt.figure(figsize=(12, 4))
plt.plot(ref_time, ref_signal)
plt.title(
    f"Reference PMT Signal - File {REFERENCE_FILE:05d}"
)
plt.xlabel("Time (s)")
plt.ylabel("Normalized Voltage")
plt.grid()
plt.tight_layout()
plt.show()


# %% MATCHED FILTER FUNCTION

def matched_filter(time, signal, ref_time, reference,
                   max_delay=None):
    """
    Perform matched filtering using cross-correlation.

    Returns:
        tau: delay axis in seconds
        S: matched filter output
        peak: maximum positive correlation
        delay: delay at peak
        amplitude: estimated scale relative to reference
    """

    time = np.asarray(time, dtype=float)
    signal = np.asarray(signal, dtype=float)

    # Remove DC offset
    M = signal - np.mean(signal)

    # Interpolate reference onto the measurement's
    # sampling interval, retaining its relative time axis
    dt = np.median(np.diff(time))

    ref_dt = np.median(np.diff(ref_time))

    ref_duration = ref_time[-1] - ref_time[0]

    ref_grid = np.arange(
        0, ref_duration + 0.5 * dt, dt
    )

    R = np.interp(
        ref_grid,
        ref_time - ref_time[0],
        reference
    )

    R = R - np.mean(R)

    # Equation (2): cross-correlation
    S = correlate(
        M, R, mode="full", method="fft"
    )

    lags = correlation_lags(
        len(M), len(R), mode="full"
    )

    tau = lags * dt

    # Restrict delay search if requested
    if max_delay is None:
        valid = np.ones(len(tau), dtype=bool)
    else:
        valid = np.abs(tau) <= max_delay

    if not np.any(valid):
        raise ValueError("No delays in search window")

    valid_indices = np.flatnonzero(valid)

    peak_index = valid_indices[
        np.argmax(S[valid])
    ]

    peak = S[peak_index]
    delay = tau[peak_index]

    # Calculate amplitude from overlapping samples
    lag = lags[peak_index]

    if lag >= 0:
        overlap = min(len(R), len(M) - lag)
        m_overlap = M[lag:lag + overlap]
        r_overlap = R[:overlap]
    else:
        overlap = min(len(M), len(R) + lag)
        m_overlap = M[:overlap]
        r_overlap = R[-lag:-lag + overlap]

    if overlap <= 0:
        amplitude = np.nan
    else:
        denominator = np.dot(r_overlap, r_overlap)
        amplitude = (
            np.dot(m_overlap, r_overlap) / denominator
            if denominator > 0 else np.nan
        )

    return tau, S, peak, delay, amplitude


# %% PROCESS ALL PMT MEASUREMENTS

results = []
filter_outputs = {}

for number in FILE_NUMBERS:

    measurement = data[number]

    tau, S, peak, delay, amplitude = matched_filter(
        measurement["time"],
        measurement["pmt"],
        ref_time,
        ref_signal,
        MAX_DELAY_SECONDS
    )

    filter_outputs[number] = {
        "tau": tau,
        "S": S
    }

    results.append({
        "File": number,
        "Modulation": MODULATION[number],
        "MF_Peak": peak,
        "MF_Delay_s": delay,
        "MF_Amplitude": amplitude,
        "LIA_Mean_V": np.mean(measurement["lia"]),
        "LIA_Std_V": np.std(measurement["lia"])
    })

results_df = pd.DataFrame(results)

print("\nMATCHED FILTER RESULTS")
print(results_df.to_string(index=False))


# %% PLOT MATCHED FILTER OUTPUTS

fig, axes = plt.subplots(
    4, 2, figsize=(14, 12), constrained_layout=True
)

for ax, number in zip(axes.flat, FILE_NUMBERS):

    output = filter_outputs[number]

    ax.plot(
        output["tau"],
        output["S"],
        linewidth=1
    )

    ax.set_title(
        f"File {number:05d} - {MODULATION[number]}"
    )

    ax.set_xlabel("Time Delay (s)")
    ax.set_ylabel("Correlation")
    ax.grid(True)

plt.show()


# %% COMPARE MATCHED FILTER AMPLITUDES

fig, ax = plt.subplots(figsize=(10, 5))

for modulation, marker in [
    ("27kHz", "o"),
    ("Random", "s")
]:

    subset = results_df[
        results_df["Modulation"] == modulation
    ]

    ax.plot(
        subset["File"],
        subset["MF_Amplitude"],
        marker=marker,
        linestyle="none",
        markersize=8,
        label=modulation
    )

ax.set_xlabel("Measurement File Number")
ax.set_ylabel("Matched Filter Amplitude")
ax.set_title("Matched Filter Response by Measurement")
ax.legend()
ax.grid()

plt.tight_layout()
plt.show()


# %% PLOT LIA OUTPUTS

fig, ax = plt.subplots(figsize=(10, 5))

for modulation, marker in [
    ("27kHz", "o"),
    ("Random", "s")
]:

    subset = results_df[
        results_df["Modulation"] == modulation
    ]

    ax.errorbar(
        subset["File"],
        subset["LIA_Mean_V"],
        yerr=subset["LIA_Std_V"],
        marker=marker,
        linestyle="none",
        capsize=4,
        label=modulation
    )

ax.set_xlabel("Measurement File Number")
ax.set_ylabel("LIA Output (V)")
ax.set_title("Traditional LIA Output")
ax.legend()
ax.grid()

plt.tight_layout()
plt.show()


# %% EXPORT RESULTS

output_file = OUTPUT_FOLDER / "matched_filter_results.csv"

results_df.to_csv(output_file, index=False)

print(f"\nResults saved to: {output_file}")
