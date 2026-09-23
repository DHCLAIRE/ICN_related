#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
First-order (spatial) inter-subject RSM on TRF topographies, Natives vs ESLs.

THIS SCRIPT RUNS ONE NULL ONLY, set by SHUFFLE_MODE below:

  'channel'  -> for each subject, scramble the 64 sensor values
                (row-wise: shuffled[s, :] = permutation(group_data[s, :]))
                H0: "a subject's topography is random / no consistent scalp pattern."

  'subject'  -> for each sensor, scramble the 59 subject values
                (column-wise: shuffled[:, j] = permutation(group_data[:, j]))
                H0: "no coordinated across-sensor structure holds a subject together."
                (Axis-mirror of the channel shuffle; rebuilds 'Frankenstein' subjects.
                 It is NOT a test of whether the L1/ESL groups differ -- for that see
                 the group-LABEL permutation in the note at the bottom of this file.)

Output per window: a per-cell two-tailed p-value matrix, a permutation threshold
(99th percentile of |null off-diagonal r|), and a thresholded RSM heatmap. Plus a
time-series graph across windows. All filenames are tagged with SHUFFLE_MODE.
"""

from pathlib import Path
import re
import matplotlib.pyplot as plt
import eelbrain
import mne
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import zscore

# --------------------------------------------------------------------------- #
#  RUN CONFIG -- this is the ONLY line that differs between the two scripts.
# --------------------------------------------------------------------------- #
SHUFFLE_MODE = 'subject'   # 'channel' or 'subject'
SEED = 42                  # reproducibility


# ========================================================================== #
#  HELPER 1: build the null RSMs for the chosen shuffle mode
# ========================================================================== #
def build_null_rsms(group_data, mode, n_permutations, rng):
    """group_data: (n_subjects, n_sensors). Returns (n_perm, n_subj, n_subj)."""
    n_subj, n_sens = group_data.shape
    null_rsms = np.zeros((n_permutations, n_subj, n_subj))

    for i in range(n_permutations):
        shuffled = np.zeros_like(group_data)

        if mode == 'channel':
            # scramble sensors WITHIN each subject (row-wise)
            for s in range(n_subj):
                shuffled[s, :] = rng.permutation(group_data[s, :])

        elif mode == 'subject':
            # scramble subjects WITHIN each sensor (column-wise)
            for j in range(n_sens):
                shuffled[:, j] = rng.permutation(group_data[:, j])

        else:
            raise ValueError(f"Unknown SHUFFLE_MODE: {mode!r} (use 'channel' or 'subject')")

        null_rsms[i, :, :] = np.corrcoef(shuffled)

    return null_rsms


# ========================================================================== #
#  HELPER 2: p-values + threshold + thresholded heatmap
# ========================================================================== #
def summarize_and_plot(spatial_rsm_real, null_rsms, mode,
                       predictorSTR, tmin, tmax, num_natives,
                       combined_labels, alpha_threshold, n_permutations, dst):
    n_subj = spatial_rsm_real.shape[0]

    # Two-tailed per-cell p-value: how often |fake r| >= |real r|
    exceedances = np.sum(np.abs(null_rsms) >= np.abs(spatial_rsm_real), axis=0)
    p_values = exceedances / n_permutations

    # Single-scalar threshold: 99th percentile of |null off-diagonal r|
    idx_all = np.triu_indices(n_subj, k=1)
    fake_off_diag = null_rsms[:, idx_all[0], idx_all[1]]
    pct = 100 * (1 - alpha_threshold)          # 0.01 -> 99,  0.05 -> 95
    threshold = np.nanpercentile(np.abs(fake_off_diag), pct)
    #threshold = np.nanpercentile(np.abs(fake_off_diag), 99)

    # Mask hides (a) non-significant cells (p > alpha) and (b) the diagonal,
    # so only significant OFF-diagonal correlations stay coloured.
    mask = (p_values > alpha_threshold) | (np.eye(n_subj, dtype=bool))

    pretty = {'channel': 'Channel-shuffle', 'subject': 'Subject-shuffle'}[mode]

    plt.figure(figsize=(14, 12))
    sns.heatmap(spatial_rsm_real,
                cmap='RdBu_r', center=0, vmin=-1, vmax=1, square=True,
                mask=mask,
                xticklabels=combined_labels, yticklabels=combined_labels,
                cbar_kws={'label': f"Pearson's r (p < {alpha_threshold})"})
    plt.axhline(num_natives, color='black', linewidth=2)
    plt.axvline(num_natives, color='black', linewidth=2)
    plt.title(f"Thresholded Spatial RSM [{pretty}]: {predictorSTR}-Zed "
              f"({tmin*1000:.0f}-{tmax*1000:.0f} ms)\n"
              f"Permutations: {n_permutations}, alpha = {alpha_threshold}")
    plt.xlabel("Subject ID")
    plt.ylabel("Subject ID")

    filename = (f'Thresholded_FirstOrder_Spatial_{predictorSTR}_'
                f'{pretty}_a={alpha_threshold}Zed_'
                f'{tmin*1000:.0f}-{tmax*1000:.0f}ms.png')
    plt.tight_layout()
    plt.savefig(dst / filename)
    plt.close()

    return p_values, threshold


# ========================================================================== #
#  MAIN
# ========================================================================== #
if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    pretty = {'channel': 'Channel-shuffle', 'subject': 'Subject-shuffle'}[SHUFFLE_MODE]
    print(f"=== RUNNING: {pretty} only ===")

    STIMULI = [str(i) for i in range(1, 13)]

    DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")
    PREDICTOR_audio_DIR = DATA_ROOT / 'TRFs_pridictors/audio_predictors'
    PREDICTOR_word_DIR = DATA_ROOT / 'TRFs_pridictors/word_predictors'
    EEG_DIR_NATs = DATA_ROOT / 'EEG_Natives' / 'Alice_natives_ICAed_fif'
    EEG_DIR_ESLs = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESL_ICAed_fif'

    IMF_DIR = DATA_ROOT / "TRFs_pridictors/IF_predictors"
    F0_DIR = DATA_ROOT / "TRFs_pridictors/F0_predictors"

    Native_SUBJECTS = [p.name for p in EEG_DIR_NATs.iterdir() if re.match(r'S\d*', p.name)]
    ESL_SUBJECTS = [p.name for p in EEG_DIR_ESLs.iterdir() if re.match(r'n_2_S\d*', p.name)]

    TRF_DIR_NATs = DATA_ROOT / 'TRFs_Natives'
    TRF_DIR_NATs.mkdir(exist_ok=True)
    DST_NATs = TRF_DIR_NATs / 'Natives_figures'
    DST_NATs.mkdir(exist_ok=True)

    TRF_DIR_ESLs = DATA_ROOT / 'TRFs_ESLs'
    TRF_DIR_ESLs.mkdir(exist_ok=True)
    DST_ESLs = TRF_DIR_ESLs / 'ESLs_figures'
    DST_ESLs.mkdir(exist_ok=True)

    print(f"Natives: {len(Native_SUBJECTS)} | ESLs: {len(ESL_SUBJECTS)}")

    # ---------------------------------------------------------------------- #
    # Predictor selection. MUST match the order the TRF was fitted with,
    # because n_trf.x.index(predictorSTR) picks the kernel by position.
    # ---------------------------------------------------------------------- #
    predictorLIST = ['ngram', 'cfg', 'word', 'lexical', 'non_lexical']  # Ngram-CFG_all.pickle
    predictorSTR = predictorLIST[0]  # -> 'cfg'

    # ---------------------------------------------------------------------- #
    # VST proficiency, used to sort ESLs (high -> low).
    # ---------------------------------------------------------------------- #
    VST_Score_float_LIST = [6.7, 7.3, 7.8, 8.2, 8.4, 6.4, 7.5, 6.7,
                            5.2, 5.3, 6.5, 5.1, 6.1, 7.9, 8.7, 8.0,
                            8.8, 6.4, 7.0, 7.4, 6.6, 7.2, 7.0, 7.3, 7.3, 7.7]
    sub_idLIST = [10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                  28, 29, 30, 31, 32, 34, 35, 36, 38, 39]
    sub_SexLIST = ["F", "M", "M", "F", "F", "M", "F", "M", "M", "F", "M", "F", "F",
                   "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M"]

    VST_df = pd.DataFrame({'id': sub_idLIST, 'VST': VST_Score_float_LIST, 'gender': sub_SexLIST})
    VST_df_sorted = VST_df.sort_values(by='VST', ascending=False)
    sorted_esl_ids = VST_df_sorted['id'].tolist()
    sorted_esl_vsts = VST_df_sorted['VST'].tolist()
    esl_subj_dict = {int(subj[5:8]): subj for subj in ESL_SUBJECTS}

    # ---------------------------------------------------------------------- #
    # Super-cap: interpolate Natives (59 surviving ch) onto the 64-ch ESL cap.
    # ---------------------------------------------------------------------- #
    native_montage = mne.channels.read_custom_montage(
        str(DATA_ROOT / 'TRFs_pridictors/easycapM10-acti61_elec.sfp'))

    sample_subj = int(Native_SUBJECTS[0][1:3])
    sample_trf = eelbrain.load.unpickle(
        TRF_DIR_NATs / f'S{sample_subj:02d}' / f'S{sample_subj:02d} Ngram-CFG_all.pickle')
    sample_trf.x = ['ngram', 'cfg', 'word', 'lexical', 'non_lexical']
    actual_native_chs = sample_trf.h[sample_trf.x.index(predictorSTR)].sensor.names
    native_chs_safe = [f"NAT_{ch}" for ch in actual_native_chs]

    esl_montage = mne.channels.make_standard_montage('standard_1020')
    esl_chs = esl_montage.ch_names[:64]

    all_chs = native_chs_safe + esl_chs
    info_combined = mne.create_info(ch_names=all_chs, sfreq=500, ch_types=['eeg'] * len(all_chs))

    combined_positions = {}
    native_positions = native_montage.get_positions()['ch_pos']
    esl_positions = esl_montage.get_positions()['ch_pos']
    for i, ch in enumerate(actual_native_chs):
        combined_positions[native_chs_safe[i]] = native_positions[ch]
    for ch in esl_chs:
        combined_positions[ch] = esl_positions[ch]

    combined_montage = mne.channels.make_dig_montage(ch_pos=combined_positions)
    info_combined.set_montage(combined_montage)
    print(f"Super-montage created with {len(info_combined.ch_names)} channels.")

    # ---------------------------------------------------------------------- #
    # Time windows + analysis parameters
    # ---------------------------------------------------------------------- #
    step = 0.200 # 10 ms
    start_times = np.arange(0, 1.000, step)   # [0, .2, .4, .6, .8]
    n_permutations = 1000
    alpha_threshold = 0.05

    plot_times = []
    median_r_natives = []
    median_r_esls = []
    thresh_perm = []          # this run's single permutation threshold per window

    all_time_raw_data = []
    all_time_rsms = []

    # ====================================================================== #
    #  MAIN TEMPORAL LOOP
    # ====================================================================== #
    for tmin in start_times:
        tmax = tmin + step
        print(f"\n--- Window {tmin*1000:.0f}-{tmax*1000:.0f} ms ---")

        all_subjects_spatial_data = []
        combined_labels = []

        # --- A. Natives (need interpolation onto the ESL cap) ------------- #
        for subj in Native_SUBJECTS:
            n_subj = int(subj[1:3])
            combined_labels.append(f"Nat_{n_subj}")

            n_trf = eelbrain.load.unpickle(
                TRF_DIR_NATs / f'S{n_subj:02d}' / f'S{n_subj:02d} Ngram-CFG_all.pickle')
            n_trf.x = ['ngram', 'cfg', 'word', 'lexical', 'non_lexical']
            window = n_trf.h[n_trf.x.index(predictorSTR)].sub(time=(tmin, tmax))
            native_data = window.get_data(dims=('sensor', 'time'))   # (59, n_times)
            n_times = native_data.shape[1]

            combined_data = np.vstack((native_data, np.zeros((len(esl_chs), n_times))))
            evoked = mne.EvokedArray(combined_data, info_combined)
            evoked.info['bads'] = esl_chs
            evoked.interpolate_bads(reset_bads=True, verbose=False)
            interpolated_data = evoked.copy().pick_channels(esl_chs).data  # (64, n_times)

            mean_spatial_map = interpolated_data.mean(axis=1)            # (64,)
            if np.std(mean_spatial_map) == 0:
                zmap = np.zeros_like(mean_spatial_map)
            else:
                zmap = zscore(mean_spatial_map)
            all_subjects_spatial_data.append(zmap)

        num_natives = len(Native_SUBJECTS)

        # --- B. ESLs (sorted by VST; interpolate only if channels missing) - #
        for esl_id, vst in zip(sorted_esl_ids, sorted_esl_vsts):
            if esl_id not in esl_subj_dict:
                continue
            subject_str = esl_subj_dict[esl_id]
            combined_labels.append(f"ESL_{esl_id} ({vst})")

            n_trf = eelbrain.load.unpickle(
                TRF_DIR_ESLs / subject_str[4:8] / f'{subject_str[4:8]} Ngram-CFG_all.pickle')
            n_trf.x = ['ngram', 'cfg', 'word', 'lexical', 'non_lexical']
            window = n_trf.h[n_trf.x.index(predictorSTR)].sub(time=(tmin, tmax))

            raw_esl_chs = list(window.sensor.names)
            standard_case_map = {ch.upper(): ch for ch in esl_montage.ch_names}
            esl_actual_chs = [standard_case_map.get(ch.upper(), ch) for ch in raw_esl_chs]
            missing_chs = [ch for ch in esl_chs if ch not in esl_actual_chs]

            if len(missing_chs) > 0:
                actual_data = window.get_data(dims=('sensor', 'time'))
                n_times = actual_data.shape[1]
                combined_data = np.vstack((actual_data, np.zeros((len(missing_chs), n_times))))
                current_all_chs = esl_actual_chs + missing_chs
                info_esl = mne.create_info(ch_names=current_all_chs, sfreq=500,
                                           ch_types=['eeg'] * len(current_all_chs))
                info_esl.set_montage(esl_montage)
                evoked = mne.EvokedArray(combined_data, info_esl)
                evoked.info['bads'] = missing_chs
                evoked.interpolate_bads(reset_bads=True, verbose=False)
                esl_data_final = evoked.copy().pick_channels(esl_chs).data   # (64, n_times)
            else:
                ch_indices = [esl_actual_chs.index(ch) for ch in esl_chs]
                raw_data = window.get_data(dims=('sensor', 'time'))
                esl_data_final = raw_data[ch_indices, :]                     # (64, n_times)

            mean_spatial_map = esl_data_final.mean(axis=1)                   # (64,)
            if np.std(mean_spatial_map) == 0:
                zmap = np.zeros_like(mean_spatial_map)
            else:
                zmap = zscore(mean_spatial_map)
            all_subjects_spatial_data.append(zmap)

        # --- C. Real RSM -------------------------------------------------- #
        group_data = np.array(all_subjects_spatial_data)   # (59, 64)
        num_total_subj = group_data.shape[0]
        spatial_rsm_real = np.corrcoef(group_data)         # (59, 59)

        all_time_raw_data.append(group_data)
        all_time_rsms.append(spatial_rsm_real)

        idx_nat = np.triu_indices(num_natives, k=1)
        median_r_natives.append(np.nanmedian(spatial_rsm_real[:num_natives, :num_natives][idx_nat]))
        idx_esl = np.triu_indices(num_total_subj - num_natives, k=1)
        median_r_esls.append(np.nanmedian(spatial_rsm_real[num_natives:, num_natives:][idx_esl]))
        plot_times.append(tmin * 1000)

        # --- D. Run THIS run's single null -------------------------------- #
        print(f"   {n_permutations} permutations [{SHUFFLE_MODE} shuffle]...")
        null_rsms = build_null_rsms(group_data, SHUFFLE_MODE, n_permutations, rng)
        _, threshold = summarize_and_plot(
            spatial_rsm_real, null_rsms, SHUFFLE_MODE,
            predictorSTR, tmin, tmax, num_natives,
            combined_labels, alpha_threshold, n_permutations, DST_ESLs)
        thresh_perm.append(threshold)

    # ====================================================================== #
    #  TIME-SERIES GRAPH (single threshold for this run)
    # ====================================================================== #
    print("\n--- Generating time-series graph ---")
    plt.figure(figsize=(12, 6))
    plt.plot(plot_times, median_r_natives, label='Native (median r)',
             color='#1f77b4', linewidth=2.5, marker='o')
    plt.plot(plot_times, median_r_esls, label='ESL (median r)',
             color='#d62728', linewidth=2.5, marker='o')
    plt.plot(plot_times, thresh_perm, label=f'Threshold ({SHUFFLE_MODE} shuffle)',
             color='black', linestyle='--', linewidth=2)
    plt.title(f"Spatial Similarity Dynamics [{pretty}]: Natives vs ESLs "
              f"({predictorSTR}-Zed, alpha={alpha_threshold})", fontsize=14)
    plt.xlabel("Time Window Start (ms)", fontsize=12)
    plt.ylabel("Median Pearson's r", fontsize=12)
    plt.xticks(plot_times, rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(DST_ESLs / f'Median_RSM_TimeSeries_{predictorSTR}_{pretty}_a={alpha_threshold}Zed.png')
    plt.close()

    print(f"--- {pretty} pipeline complete ---")

    # ---------------------------------------------------------------------- #
    # OPTIONAL: save 3D arrays for later analysis (uncomment to use)
    # ---------------------------------------------------------------------- #
    # np.save(DST_ESLs / f'Raw_Spatial_Maps_{predictorSTR}_{pretty}_AllWindows.npy',
    #         np.array(all_time_raw_data))   # (n_windows, 59, 64)
    # np.save(DST_ESLs / f'FirstOrder_Spatial_{predictorSTR}_{pretty}_RSM_AllWindows.npy',
    #         np.array(all_time_rsms))       # (n_windows, 59, 59)

# ========================================================================== #
#  NOTE: neither shuffle tests L1-vs-ESL difference. For that, permute GROUP
#  LABELS (this lives outside group_data):
#
#      labels = np.array(['NAT']*num_natives + ['ESL']*(num_total_subj-num_natives))
#      nb = spatial_rsm_real[:num_natives, :num_natives]
#      eb = spatial_rsm_real[num_natives:, num_natives:]
#      real_gap = (np.nanmedian(nb[np.triu_indices_from(nb, 1)])
#                  - np.nanmedian(eb[np.triu_indices_from(eb, 1)]))
#      null_gap = []
#      for _ in range(n_permutations):
#          perm = rng.permutation(labels)
#          pnb = spatial_rsm_real[np.ix_(perm == 'NAT', perm == 'NAT')]
#          peb = spatial_rsm_real[np.ix_(perm == 'ESL', perm == 'ESL')]
#          null_gap.append(np.nanmedian(pnb[np.triu_indices_from(pnb, 1)])
#                          - np.nanmedian(peb[np.triu_indices_from(peb, 1)]))
#      p_group = (np.sum(np.abs(null_gap) >= abs(real_gap)) + 1) / (n_permutations + 1)
# ========================================================================== #
