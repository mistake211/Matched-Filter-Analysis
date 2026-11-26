# ProcessCWFM.m
"""
Created on Mon Nov 9, 2026 @ 18:04:43 - Dustin

@author: Dustin Percifield
"""

# Requires matchedf() from the previous cell.

# ---------------- helpers ----------------
def load_csv(folder, prefix, filenum):
    """Reads '<prefix>--LIAAdvancedLab--<nnnnn>.csv' and returns the first two columns
    (time, amplitude). Skips any non-numeric header lines at the top of the file."""
    path = Path(folder) / f"{prefix}--LIAAdvancedLab--{filenum:05d}.csv"
    with open(path) as fh:
        for skip, line in enumerate(fh):
            fields = line.strip().split(",")[:2]
            try:
                [float(x) for x in fields]
                if len(fields) == 2:
                    break
            except ValueError:
                pass
    return np.loadtxt(path, delimiter=",", skiprows=skip, usecols=(0, 1), ndmin=2)

def gauss(x, G, a, b, f):
    # MATLAB orders fittype coefficients alphabetically (uppercase first): G, a, b, f.
    # That's the order the Lower/StartPoint/Upper vectors refer to.
    return a + b * np.exp(-(x - f)**2 / (2 * G**2))

def fit_with_ci(x, y, p0, lower, upper, level=0.95):
    """Nonlinear least-squares fit plus confint()-style confidence intervals.
    Returns popt [G, a, b, f] and ci (row 0 = lower bounds, row 1 = upper bounds)."""
    popt, pcov = curve_fit(gauss, x, y, p0=p0, bounds=(lower, upper))
    dof = max(len(x) - len(popt), 1)
    half = t_dist.ppf((1 + level) / 2, dof) * np.sqrt(np.diag(pcov))
    ci = np.vstack([popt - half, popt + half])
    return popt, ci

# ---------------- constants ----------------
c = 299792458
ABSORB_WL = 587.7249            # nm
M_HeII = 6.645572669e-27        # kg   (M_ArII = 6.6335e-26)
E = 1.602e-19
LAMBDA_M = ABSORB_WL * 1e-9
COLOR = np.array([9, 12, 100]) / 255
xplot = np.linspace(-10, 10, 2001)   # -10:0.01:10

WAVELENGTHS = np.array([587.7190, 587.7200, 587.7210, 587.7220, 587.7230, 587.7240, 587.7250,
                        587.7260, 587.7270, 587.7280, 587.7290, 587.7300, 587.7310, 587.7320])

# =============== Matched filter ===============
MF_FOLDER = r'/content/drive/Shareddrives/Advanced_Lab/Advanced Lab/lab data/3rd Data Collection/'
FILENUMBERS_MF = np.arange(10001, 10004)
WAVELENGTHS_MF = WAVELENGTHS.copy()
FREQS_MF = c / WAVELENGTHS_MF - c / ABSORB_WL      # GHz (wavelengths in nm)
Y_MF = np.zeros(len(WAVELENGTHS_MF))
ERRORS_MF = np.zeros(len(WAVELENGTHS_MF))

NUMSTACKS = 50
NREF = 10000 * NUMSTACKS

# Find the signal peak positions from file 11, then reuse them for every file
PEAK_FILE = 11
DATA = load_csv(MF_FOLDER, "C1", PEAK_FILE)
TIME_MF = DATA[:, 0]
PMT = DATA[:, 1] - DATA[:, 1].mean()
REF_MF = load_csv(MF_FOLDER, "C2", PEAK_FILE)[:, 1]

R = matchedf(PMT, REF_MF[:NREF])
P = np.argmax(R[:15000 + NREF])                               # 0-based index
SIGLOC = np.arange(P, P + 10000 * (97 - NUMSTACKS) + 1, 10000)

for i, n in enumerate(FILENUMBERS_MF):
    DATA = load_csv(MF_FOLDER, "C1", n)
    TIME_MF = DATA[:, 0]
    PMT = DATA[:, 1] - DATA[:, 1].mean()
    REF_MF = load_csv(MF_FOLDER, "C2", n)[:, 1]

    R = matchedf(PMT, REF_MF[:NREF])
    # P = np.argmax(R[:15000 + NREF])
    # SIGLOC = np.arange(P, P + 10000 * (97 - NUMSTACKS) + 1, 10000)

    ERRORS_MF[i] = np.std(R[SIGLOC], ddof=1)   # MATLAB std() uses N-1
    Y_MF[i] = np.mean(R[SIGLOC])

popt_MF, ci_MF = fit_with_ci(FREQS_MF, Y_MF,
                             p0=[2, 0, 500, 0],
                             lower=[0, -50, 0, -10],
                             upper=[10, 50, 1300, 10])

T_i_MF = (popt_MF[0] * 1e9)**2 * LAMBDA_M**2 * M_HeII / E
T_i_conf_MF = T_i_MF - (ci_MF[0, 0] * 1e9)**2 * LAMBDA_M**2 * M_HeII / E
print("T_i_MF =", T_i_MF)
print("T_i_conf_MF =", T_i_conf_MF)

# =============== Lock-in amplifier ===============
LIA_FOLDER = r'/content/drive/Shareddrives/Advanced_Lab/Advanced Lab/lab data/3rd Data Collection/'
FILENUMBERS_LIA = np.arange(10009, 10012)   # to 23 for full dataset
WAVELENGTHS_LIA = WAVELENGTHS.copy() # (587.7265, 587.7255 for full dataset)
FREQS_LIA = c / WAVELENGTHS_LIA - c / ABSORB_WL
Y_LIA = np.zeros(len(WAVELENGTHS_LIA))
ERRORS_LIA = np.zeros(len(WAVELENGTHS_LIA))

for i, n in enumerate(FILENUMBERS_LIA):
    DATA = load_csv(LIA_FOLDER, "C2", n)
    TIME_MF = DATA[:, 0]
    PMT = DATA[:, 1]

    ERRORS_LIA[i] = np.sqrt(PMT.max() - PMT.min()) / 2
    Y_LIA[i] = np.mean(PMT)

popt_LIA, ci_LIA = fit_with_ci(FREQS_LIA, Y_LIA,
                               p0=[2, 0, 20, 0],
                               lower=[0, -5, 0, -10],
                               upper=[10, 5, 100, 10])

T_i_LIA = (popt_LIA[0] * 1e9)**2 * LAMBDA_M**2 * M_HeII / E
T_i_conf_LIA = T_i_LIA - (ci_LIA[0, 0] * 1e9)**2 * LAMBDA_M**2 * M_HeII / E
print("T_i_LIA =", T_i_LIA)
print("T_i_conf_LIA =", T_i_conf_LIA)

# =============== Plot (LIA left, MF right) ===============
fig, (ax_lia, ax_mf) = plt.subplots(1, 2, figsize=(7, 5), facecolor="white")
for ax, x, y, err, popt in [(ax_lia, FREQS_LIA, Y_LIA, ERRORS_LIA, popt_LIA),
                            (ax_mf,  FREQS_MF,  Y_MF,  ERRORS_MF,  popt_MF)]:
    ax.errorbar(x, y, yerr=err, fmt="s", color=COLOR, elinewidth=2, markersize=10,
                markerfacecolor=COLOR, capsize=4)
    ax.plot(xplot, gauss(xplot, *popt), "--", color=COLOR, linewidth=2)
plt.tight_layout()
plt.show()