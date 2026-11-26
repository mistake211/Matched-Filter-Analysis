#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rigol DG1022 Random ON/OFF Waveform Generator

Generates a 4096-point arbitrary waveform for the DG1022.

The waveform consists of randomly chosen ON and OFF durations.

Author: 
Maxwell Flanagan
"""

import random
import struct

# Things to Change

# Number of waveform points.
# The DG1022 supports up to 4096 points.
NUM_POINTS = 4096

# Duration represented by each waveform point.
# 10 ms means 100 samples/second.
SAMPLE_TIME_MS = 10

# Minimum and maximum ON duration.
MIN_ON_MS = 10
MAX_ON_MS = 100

# Minimum and maximum OFF duration.
MIN_OFF_MS = 10
MAX_OFF_MS = 100

# 0x0000 = minimum output
# 0x3FFF = maximum output
OFF_VALUE = 0x0000
ON_VALUE = 0x3FFF

# Name of the output file.
OUTPUT_FILE = "random_laser.raf"

# Set to an integer if you want to reproduce exactly the same
# random sequence later.
#
# Example:
# RANDOM_SEED = 12345
#
# Set to None for a different sequence every time.
RANDOM_SEED = None


# PROGRAM

def duration_to_points(duration_ms):
    """
    Convert a duration in milliseconds into the nearest
    whole number of waveform points.
    """
    points = round(duration_ms / SAMPLE_TIME_MS)

    # Every ON/OFF period must contain at least one point.
    return max(1, points)


def generate_waveform():
    """
    Generate a random sequence of ON and OFF states containing
    exactly NUM_POINTS samples.
    """

    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    waveform = []

    # Start with the laser OFF.
    state = OFF_VALUE

    while len(waveform) < NUM_POINTS:

        if state == ON_VALUE:
            duration = random.randint(MIN_ON_MS, MAX_ON_MS)
        else:
            duration = random.randint(MIN_OFF_MS, MAX_OFF_MS)

        num_points = duration_to_points(duration)

        # Don't exceed the 4096-point limit.
        remaining = NUM_POINTS - len(waveform)
        num_points = min(num_points, remaining)

        waveform.extend([state] * num_points)

        # Switch ON <-> OFF.
        if state == ON_VALUE:
            state = OFF_VALUE
        else:
            state = ON_VALUE

    return waveform


def write_rdf_file(waveform, filename):
    """
    Write the waveform as 16-bit little-endian values.

    DG1022 values:
        0x0000 = minimum
        0x3FFF = maximum
    """

    with open(filename, "wb") as file:

        for value in waveform:

            # '<H' = unsigned 16-bit integer, little endian
            file.write(struct.pack("<H", value))


def analyze_waveform(waveform):
    """
    Print useful information about the generated waveform.
    """

    on_points = waveform.count(ON_VALUE)
    off_points = waveform.count(OFF_VALUE)

    total_time_s = len(waveform) * SAMPLE_TIME_MS / 1000

    on_time_s = on_points * SAMPLE_TIME_MS / 1000
    off_time_s = off_points * SAMPLE_TIME_MS / 1000

    print()
    print("==========================================")
    print(" DG1022 RANDOM WAVEFORM")
    print("==========================================")
    print(f"Number of points:       {len(waveform)}")
    print(f"Time per point:         {SAMPLE_TIME_MS} ms")
    print(f"Total waveform period:  {total_time_s:.3f} s")
    print()
    print(f"ON time:                {on_time_s:.3f} s")
    print(f"OFF time:               {off_time_s:.3f} s")
    print(f"ON percentage:          {100 * on_points / len(waveform):.1f}%")
    print(f"OFF percentage:         {100 * off_points / len(waveform):.1f}%")
    print()
    print(f"Output file:            {OUTPUT_FILE}")
    print(f"File size:              {len(waveform) * 2} bytes")
    print("==========================================")


def main():

    print("Generating random DG1022 waveform...")

    waveform = generate_waveform()

    write_rdf_file(waveform, OUTPUT_FILE)

    analyze_waveform(waveform)

    print()
    print("Done.")
    print()
    print("Copy the following file to a FAT32-formatted USB drive:")
    print(f"    {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

