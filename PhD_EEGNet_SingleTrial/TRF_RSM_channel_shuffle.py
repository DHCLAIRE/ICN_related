#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
First-order (spatial) inter-subject RSM on TRF topographies, Natives vs ESLs.

Two things happen per time window:

 (A) CONSISTENCY NULL, set by SHUFFLE_MODE -- "is the shared topography above chance?"
       'channel' -> scramble the 64 sensor values within each subject (row-wise)
       'subject' -> scramble the 59 subject values within each sensor (column-wise)
     Both live INSIDE group_data; both are topography-consistency tests.

 (B) IS-RSA (VST Mantel), ESL group only -- "does that consistency track proficiency?"
     Steps 3-5 of IS-RSA: build a VST similarity matrix (Nearest-Neighbor and
     Anna Karenina), Spearman-correlate it with the ESL block of the neural RSM,
     and test with a subject-label (Mantel) permutation.
     NOTE: (B) is independent of SHUFFLE_MODE -- it gives the same result in both
     scripts, because it does not use the (A) shuffle at all.
"""

from pathlib import Path
import re
import matplotlib.pyplot as plt
import eelbrain
import mne
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import zscore, spearmanr

# --------------------------------------------------------------------------- #
#  RUN CONFIG -- the ONLY line that differs between the two shuffle scripts.
# --------------------------------------------------------------------------- #
SHUFFLE_MODE = 'channel'   # 'channel' or 'subject'
SEED = 42                  # reproducibility


# ========================================================================== #
#  HELPER 1: build the null RSMs for the chosen shuffle mode  (part A)
# ========================================================================== #
def build_null_rsms(group_data, mode, n_permutations, rng):
    """group_data: (n_subjects, n_sensors). Returns (n_perm, n_subj, n_subj)."""
    n_subj, n_sens = group_data.shape
    null_rsms = np.zeros((n_permutations, n_subj, n_subj))
    for i in range(n_permutations):
        shuffled = np.zeros_like(group_data)
        if mode == 'channel':
            for s in range(n_subj):
                shuffled[s, :] = rng.permutation(group_data[s, :])   # sensors within subject
        elif mode == 'subject':
            for j in range(n_sens):
                shuffled[:, j] = rng.permutation(group_data[:, j])   # subjects within sensor
        else:
            raise ValueError(f"Unknown SHUFFLE_MODE: {mode!r}")
        null_rsms[i, :, :] = np.corrcoef(shuffled)
    return null_rsms


# ========================================================================== #
#  HELPER 2: p-values + threshold + thresholded heatmap  (part A)
# ========================================================================== #
def summarize_and_plot(spatial_rsm_real, null_rsms, mode,
                       predictorSTR, tmin, tmax, num_natives,
                       combined_labels, alpha_threshold, n_permutations, dst):
    n_subj = spatial_rsm_real.shape[0]
    exceedances = np.sum(np.abs(null_rsms) >= np.abs(spatial_rsm_real), axis=0)
    p_values = exceedances / n_permutations

    idx_all = np.triu_indices(n_subj, k=1)
    fake_off_diag = null_rsms[:, idx_all[0], idx_all[1]]
    pct = 100 * (1 - alpha_threshold)                      # 0.01->99, 0.05->95 (FIXED)
    threshold = np.nanpercentile(np.abs(fake_off_diag), pct)

    mask = (p_values > alpha_threshold) | (np.eye(n_subj, dtype=bool))
    pretty = {'channel': 'Channel-shuffle', 'subject': 'Subject-shuffle'}[mode]

    plt.figure(figsize=(14, 12))
    sns.heatmap(spatial_rsm_real, cmap='RdBu_r', center=0, vmin=-1, vmax=1, square=True,
                mask=mask, xticklabels=combined_labels, yticklabels=combined_labels,
                cbar_kws={'label': f"Pearson's r (p < {alpha_threshold})"})
    plt.axhline(num_natives, color='black', linewidth=2)
    plt.axvline(num_natives, color='black', linewidth=2)
    plt.title(f"Thresholded Spatial RSM [{pretty}]: {predictorSTR}-Zed "
              f"({tmin*1000:.0f}-{tmax*1000:.0f} ms)\n"
              f"Permutations: {n_permutations}, alpha = {alpha_threshold}")
    plt.xlabel("Subject ID"); plt.ylabel("Subject ID")
    fn = (f'Thresholded_FirstOrder_Spatial_{predictorSTR}_{pretty}_'
          f'a={alpha_threshold}Zed_{tmin*1000:.0f}-{tmax*1000:.0f}ms.png')
    plt.tight_layout(); plt.savefig(dst / fn); plt.close()
    return p_values, threshold


# ========================================================================== #
#  HELPER 3: IS-RSA via Mantel permutation  (part B, steps 3-5)
# ========================================================================== #
def isrsa_mantel(neural_rsm, vst_scores, model, n_perm, rng):
    """
    neural_rsm : (n, n) subject x subject similarity (ESL block of spatial_rsm_real)
    vst_scores : (n,)   VST, SAME row order as neural_rsm
    model      : 'nn' (Nearest-Neighbor) or 'annak' (Anna Karenina)
    Returns (observed Spearman r, two-tailed Mantel p-value).
    """
    vst = np.asarray(vst_scores, dtype=float)
    n = len(vst)

    # ---- Step 3: build the model similarity matrix (higher = predicted more alike)
    if model == 'nn':
        model_rsm = -np.abs(vst[:, None] - vst[None, :])       # close scores -> similar
    elif model == 'annak':
        model_rsm = (vst[:, None] + vst[None, :]) / 2.0        # both high -> similar
    else:
        raise ValueError(f"Unknown model: {model!r}")

    tri = np.tril_indices(n, k=-1)          # each pair once, diagonal excluded
    b = neural_rsm[tri]
    ok = ~np.isnan(b)                        # a flat subject can make its r NaN; drop those pairs
    b_ok = b[ok]

    # ---- Step 4: observed Spearman between the two matrices' lower triangles
    obs = spearmanr(b_ok, model_rsm[tri][ok]).statistic

    # ---- Step 5: Mantel -- shuffle SUBJECT LABELS (rows+cols together), rebuild
    null = np.empty(n_perm)
    for i in range(n_perm):
        p = rng.permutation(n)
        m_perm = model_rsm[np.ix_(p, p)][tri]
        null[i] = spearmanr(b_ok, m_perm[ok]).statistic

    pval = (np.sum(np.abs(null) >= np.abs(obs)) + 1) / (n_perm + 1)
    return obs, pval


# ========================================================================== #
#  MAIN
# ========================================================================== #
if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    pretty = {'channel': 'Channel-shuffle', 'subject': 'Subject-shuffle'}[SHUFFLE_MODE]
    print(f"=== RUNNING: {pretty} + IS-RSA(VST) ===")

    STIMULI = [str(i) for i in range(1, 13)]
    DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")
    EEG_DIR_NATs = DATA_ROOT / 'EEG_Natives' / 'Alice_natives_ICAed_fif'
    EEG_DIR_ESLs = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESL_ICAed_fif'

    Native_SUBJECTS = [p.name for p in EEG_DIR_NATs.iterdir() if re.match(r'S\d*', p.name)]
    ESL_SUBJECTS = [p.name for p in EEG_DIR_ESLs.iterdir() if re.match(r'n_2_S\d*', p.name)]

    TRF_DIR_NATs = DATA_ROOT / 'TRFs_Natives'; TRF_DIR_NATs.mkdir(exist_ok=True)
    DST_NATs = TRF_DIR_NATs / 'Natives_figures'; DST_NATs.mkdir(exist_ok=True)
    TRF_DIR_ESLs = DATA_ROOT / 'TRFs_ESLs'; TRF_DIR_ESLs.mkdir(exist_ok=True)
    DST_ESLs = TRF_DIR_ESLs / 'ESLs_figures'; DST_ESLs.mkdir(exist_ok=True)

    print(f"Natives: {len(Native_SUBJECTS)} | ESLs: {len(ESL_SUBJECTS)}")

    predictorLIST = ['ngram', 'cfg', 'word', 'lexical', 'non_lexical']
    predictorSTR = predictorLIST[1]  # -> 'cfg'

    # VST proficiency (sorted high -> low)
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

    # Super-cap interpolation setup
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

    step = 0.200
    start_times = np.arange(0, 1.000, step)
    n_permutations = 1000        # for the (A) consistency null
    n_mantel = 10000             # for the (B) IS-RSA Mantel
    alpha_threshold = 0.05

    plot_times = []
    median_r_natives, median_r_esls, thresh_perm = [], [], []
    # (B) IS-RSA accumulators
    isrsa_r_nn, isrsa_p_nn, isrsa_r_ak, isrsa_p_ak = [], [], [], []

    all_time_raw_data, all_time_rsms = [], []

    # ====================================================================== #
    #  MAIN TEMPORAL LOOP
    # ====================================================================== #
    for tmin in start_times:
        tmax = tmin + step
        print(f"\n--- Window {tmin*1000:.0f}-{tmax*1000:.0f} ms ---")

        all_subjects_spatial_data = []
        combined_labels = []
        esl_vst_used = []        # VST aligned to the ESL rows we actually append

        # --- A. Natives (interpolate onto the ESL cap) ------------------- #
        for subj in Native_SUBJECTS:
            n_subj = int(subj[1:3])
            combined_labels.append(f"Nat_{n_subj}")
            n_trf = eelbrain.load.unpickle(
                TRF_DIR_NATs / f'S{n_subj:02d}' / f'S{n_subj:02d} Ngram-CFG_all.pickle')
            n_trf.x = ['ngram', 'cfg', 'word', 'lexical', 'non_lexical']
            window = n_trf.h[n_trf.x.index(predictorSTR)].sub(time=(tmin, tmax))
            native_data = window.get_data(dims=('sensor', 'time'))
            n_times = native_data.shape[1]
            combined_data = np.vstack((native_data, np.zeros((len(esl_chs), n_times))))
            evoked = mne.EvokedArray(combined_data, info_combined)
            evoked.info['bads'] = esl_chs
            evoked.interpolate_bads(reset_bads=True, verbose=False)
            interpolated_data = evoked.copy().pick_channels(esl_chs).data
            mean_spatial_map = interpolated_data.mean(axis=1)
            zmap = np.zeros_like(mean_spatial_map) if np.std(mean_spatial_map) == 0 else zscore(mean_spatial_map)
            all_subjects_spatial_data.append(zmap)

        num_natives = len(Native_SUBJECTS)

        # --- B. ESLs (sorted by VST) ------------------------------------- #
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
                esl_data_final = evoked.copy().pick_channels(esl_chs).data
            else:
                ch_indices = [esl_actual_chs.index(ch) for ch in esl_chs]
                raw_data = window.get_data(dims=('sensor', 'time'))
                esl_data_final = raw_data[ch_indices, :]

            mean_spatial_map = esl_data_final.mean(axis=1)
            zmap = np.zeros_like(mean_spatial_map) if np.std(mean_spatial_map) == 0 else zscore(mean_spatial_map)
            all_subjects_spatial_data.append(zmap)
            esl_vst_used.append(vst)          # keep VST aligned to this ESL row

        # --- C. Real RSM -------------------------------------------------- #
        group_data = np.array(all_subjects_spatial_data)
        num_total_subj = group_data.shape[0]
        spatial_rsm_real = np.corrcoef(group_data)
        all_time_raw_data.append(group_data)
        all_time_rsms.append(spatial_rsm_real)

        idx_nat = np.triu_indices(num_natives, k=1)
        median_r_natives.append(np.nanmedian(spatial_rsm_real[:num_natives, :num_natives][idx_nat]))
        idx_esl = np.triu_indices(num_total_subj - num_natives, k=1)
        median_r_esls.append(np.nanmedian(spatial_rsm_real[num_natives:, num_natives:][idx_esl]))
        plot_times.append(tmin * 1000)

        # --- D. Part A: consistency null (this run's shuffle) ------------- #
        print(f"   {n_permutations} permutations [{SHUFFLE_MODE} shuffle]...")
        null_rsms = build_null_rsms(group_data, SHUFFLE_MODE, n_permutations, rng)
        _, threshold = summarize_and_plot(
            spatial_rsm_real, null_rsms, SHUFFLE_MODE,
            predictorSTR, tmin, tmax, num_natives,
            combined_labels, alpha_threshold, n_permutations, DST_ESLs)
        thresh_perm.append(threshold)

        # --- E. Part B: IS-RSA (VST Mantel), ESL block only -------------- #
        esl_block = spatial_rsm_real[num_natives:, num_natives:]     # (n_esl, n_esl)
        r_nn, p_nn = isrsa_mantel(esl_block, esl_vst_used, 'nn', n_mantel, rng)
        r_ak, p_ak = isrsa_mantel(esl_block, esl_vst_used, 'annak', n_mantel, rng)
        isrsa_r_nn.append(r_nn); isrsa_p_nn.append(p_nn)
        isrsa_r_ak.append(r_ak); isrsa_p_ak.append(p_ak)
        print(f"   IS-RSA  NN: r={r_nn:+.3f} p={p_nn:.4f}   |   AnnaK: r={r_ak:+.3f} p={p_ak:.4f}")

    # ====================================================================== #
    #  PLOT 1: consistency time-series (part A)
    # ====================================================================== #
    plt.figure(figsize=(12, 6))
    plt.plot(plot_times, median_r_natives, label='Native (median r)', color='#1f77b4', lw=2.5, marker='o')
    plt.plot(plot_times, median_r_esls, label='ESL (median r)', color='#d62728', lw=2.5, marker='o')
    plt.plot(plot_times, thresh_perm, label=f'Threshold ({SHUFFLE_MODE} shuffle)',
             color='black', linestyle='--', lw=2)
    plt.title(f"Spatial Similarity Dynamics [{pretty}]: Natives vs ESLs "
              f"({predictorSTR}-Zed, alpha={alpha_threshold})")
    plt.xlabel("Time Window Start (ms)"); plt.ylabel("Median Pearson's r")
    plt.xticks(plot_times, rotation=45); plt.grid(axis='y', linestyle='--', alpha=0.7); plt.legend()
    plt.tight_layout()
    plt.savefig(DST_ESLs / f'ISRSA_Median_RSM_TimeSeries_{predictorSTR}_{pretty}_a={alpha_threshold}Zed.png')
    plt.close()

    # ====================================================================== #
    #  PLOT 2: IS-RSA time-series (part B) -- shuffle-independent
    #  Filled markers = significant window (p < 0.05).
    # ====================================================================== #
    plt.figure(figsize=(12, 6))
    for r_list, p_list, name, color in [
            (isrsa_r_nn, isrsa_p_nn, 'Nearest-Neighbor', '#2ca02c'),
            (isrsa_r_ak, isrsa_p_ak, 'Anna Karenina', '#9467bd')]:
        plt.plot(plot_times, r_list, label=f'{name} (IS-RSA r)', color=color, lw=2.5)
        sig = [t for t, p in zip(plot_times, p_list) if p < 0.05]
        sig_r = [r for r, p in zip(r_list, p_list) if p < 0.05]
        plt.scatter(plot_times, r_list, facecolors='none', edgecolors=color, s=60)
        plt.scatter(sig, sig_r, color=color, s=90, zorder=5, label=f'{name} p<0.05')
    plt.axhline(0, color='gray', lw=1)
    plt.title(f"IS-RSA: does the ESL {predictorSTR} topography track VST? "
              f"(Mantel, {n_mantel} perms)")
    plt.xlabel("Time Window Start (ms)"); plt.ylabel("Spearman r (neural RSM vs VST model)")
    plt.xticks(plot_times, rotation=45); plt.grid(axis='y', linestyle='--', alpha=0.7); plt.legend()
    plt.tight_layout()
    plt.savefig(DST_ESLs / f'ISRSA_VST_TimeSeries_{predictorSTR}.png')
    plt.close()

    print(f"\n--- {pretty} + IS-RSA pipeline complete ---")

# ========================================================================== #
#  NOTE: neither (A) shuffle tests L1-vs-ESL difference. For that, permute
#  GROUP LABELS across the pooled sample (outside group_data):
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
