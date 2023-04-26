# ICN_related

## Thesis_Ailce TRFs Progress and scripts

#### Predictors (DONE)
```
# Scripts
All(gammatone, onset, CFG-Lexical): Thesis/Alice_gammatone_word-predictors.py
```
#### Acoustic (envelope, word onset)  (DONE)
```
# TRF Scripts
  Natives: /Thesis/TRFs_produce-estimate_Natives.py
  ESLs: /Thesis/TRFs_produce-estimate_ESLs.py
```

#### Word-Models (NGram, CFG, Fractality) (NOT YET)
```
# CFG & N-gram TRFs (Produced, yet not analyzed)
  Natives: /Thesis/TRFs_produce-estimate_Natives.py
  ESLs: /Thesis/TRFs_produce-estimate_ESLs.py

# Fractality Model script (unfinished)
  /Thesis/Importance_Fractality.py

# box count result (preview ver.)
  /Thesis/boxed_count_results_2.csv
```

#### Lexical (Content v.s. Function words)  (About to)

#### Instant Frequency (From envelope by HHT_EMD)  (NO testing YET)

#### Foundamental Frequency (F0)  (Working on it)

#### figures (Statistics/Analyses)
```
# envelope & onset
  Natives:/Thesis/Alice_Natives_analysis.ipynb
  ESLs:/Thesis/Alice_ESLs_analysis.ipynb
```
#### Experiment (for ESLs) (DONE)
Text Preprocessing
```
12 Qs: /Thesis/12Qs_preprocess.py
Corrected 12 Qs text: /Thesis/Alice_questionsLIST.json
```
Procedure
```
# MacbookPro & iMac 2017
  /Thesis/Alice_SoundPlay.py

# Win10 & NeuroScan (in NCU)
  /Thesis/Alice_SoundPlay_windows_EEGver.py

# Win8 & MEG 160 system(in Academia _Sinica)
  /Thesis/Alice_SoundPlay_windows_MEGver.py
```





## Thesis_LTTC TRFs Progress (0% Starting with Predictor tables_)

#### Predictor tables (NOPE)
word (split)

Segment (per tape)

Onset & Offset

Order (accumalate sequence)

LogFreq & LogFreq_Prev & LogFreq_Next

SndPower

Length (Offset - Onser)

Position (by sentence)

Sentence (by tape)

IsLexical (1 & 0 == Booleen)

NGram

CFG

Fractality

#### Acoustic (envelope, word onset)  (NOPE)

#### Word-Models (NGram, CFG, Fractality)  (NOPE)

#### Lexical (Content v.s. Function words)  (NOPE)

#### Instant Frequency (From envelope by HHT_EMD)  (NOPE)

#### Foundamental Frequency (F0)  (NOPE)

#### figures (Statistics/Analyses)  (NOPE)


# THE PROGRESS OF THE THESIS

Table of Contents(ALL Content needs to be rewrite!!!)

Chinese Abstract---
English Abstract---
Aknoledgements--
Content Table---
List of Tables---
List of Figures---

Introduction
1.1 Text/speech comprehension
1.2 Bilingualism and second language learning
1.2.1
1.3 Auditory features(phonetics, envelope, word onset, sentence boundary, F0,instantaneous frequency)
	1.3.1 Envelope
1.4 Linguistic features(phonetics, semantics, syntactics, context, Verb types)
1.5 Language model(Ngram, CFG, Fractality: Syntactic surprisal & Semantic Surprisal)
	1.5.1 N-gram model
	1.5.2 Context Free G model
	
1.6 Temporal Response Function (TRF) Analysis
1.7 Aims of this study
Experiment 1
2.1 Hypothesis (Fractality model => A useful indicator on neural activity prediction?)
2.2 Methods and Materials
  2.2.1 Participants
  2.2.2 Stimuli
  2.2.3 Procedure (Same as Brennan & Hal, 2019 + Vocabulary Size Test)
  2.2.4 EEG recording
  2.2.5 EEG pre-processing
2.3 Statistical analyses (TRF)
2.4 Results (TRF)
2.5 Discussion
Experiment 2_LTTC
3.1 Hypothesis (How ESL learners’ proficiency level affect their VP detection abilities? (Arai & Keller, 2013))
3.2 Methods and Materials
  3.2.1 Participants
  3.2.2 Stimuli
  3.2.3 Procedure (Same as LTTC)
  3.2.4 EEG recording
  3.2.5 EEG pre-processing
3.3 Statistical analyses (ERPs_?? & TRF)
3.4 Results (TRFs)
3.5 Discussion
General Discussion and Conclusion
4.1 Summary
4.2 Applications
4.3 Limitations of this study and future directions
References
Appendixes

