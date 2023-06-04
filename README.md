# ICN_related

## Thesis_Ailce TRFs Progress and scripts

#### `(DONE)` Predictors
```
# Scripts
All(gammatone, onset, CFG-Lexical): Thesis/Alice_gammatone_word-predictors.py
```  
#### `(DONE)` Acoustic (envelope, word onset)
```
# TRF Scripts
  Natives: /Thesis/TRFs_produce-estimate_Natives.py
  ESLs: /Thesis/TRFs_produce-estimate_ESLs.py
```  
#### `(DONE)` Word-Models (NGram, CFG, Fractality)
```
# CFG & N-gram TRFs (Produced and analyzed)
  Natives: /Thesis/TRFs_produce-estimate_Natives.py
  ESLs: /Thesis/TRFs_produce-estimate_ESLs.py

# Fractality Model script (unfinished)
  /Thesis/Importance_Fractality.py

# box count result (preview ver.)
  /Thesis/boxed_count_results_2.csv
```  
#### `(DONE)` Lexical (Content v.s. Function words)
```
# Lexical & non-lexical TRFs (Produced and analyzed)
  Natives: /Thesis/TRFs_produce-estimate_Natives.py
  ESLs: /Thesis/TRFs_produce-estimate_ESLs.py
```  
#### Instant Frequency (From envelope by HHT_EMD)  `(Almost, not yet divided into 12 parts)`
```
Produced by EMD, working on how to trun into the 12 part of the data.
# Predictor: IF
  Alice_IF_EMD.ipynb
# IF TRFs
  Natives: /Thesis/??
  ESLs: /Thesis/??
```  
#### Foundamental Frequency (F0)  `(Working on it, Matlab)`

#### figures (Statistics/Analyses)
```
# envelope & onset
  Natives:/Thesis/Alice_Natives_analysis.ipynb
  ESLs:/Thesis/Alice_ESLs_analysis.ipynb
```  

#### `(DONE)` Experiment (for ESLs)
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
***

## Thesis_LTTC TRFs Progress (0% Starting with Predictor tables_)

#### Predictor tables `(Partial, but not orgaanized and saved into csv)`
`(DONE)` word (split)  

`(DONE)` Segment (per tape)  

`Ongoing` Onset & Offset   

`(DONE)` Order (accumalate sequence)  

LogFreq & LogFreq_Prev & LogFreq_Next  `NOPE`

SndPower  `NOPE`

Length (Offset - Onset)  `NOPE`  

`(DONE)` Position (by sentence)  

`(DONE)` Sentence (by tape)  

`Ongoing` IsLexical (1 & 0 == Booleen)  

`Almost` NGram  

CFG `NOPE`  

Fractality `NOPE`  

#### Acoustic (envelope, word onset)  (NOPE)

#### Word-Models (NGram, CFG, Fractality)  (NOPE)

#### Lexical (Content v.s. Function words)  (NOPE)

#### Instant Frequency (From envelope by HHT_EMD)  (NOPE)

#### Foundamental Frequency (F0)  (NOPE)

#### figures (Statistics/Analyses)  (NOPE)


# THE PROGRESS OF THE THESIS

Table of Contents(ALL Content needs to be rewrite!!!)  

- [ ] Chinese Abstract---  
- [ ] English Abstract---  
- [ ] Aknoledgements--  
- [ ] Content Table---  
- [ ] List of Tables---  
- [ ] List of Figures---  

### 1 Introduction

- [ ] 1.1 Text/speech comprehension  
- [ ] 1.2 Bilingualism and second language learning  
  - [ ] 1.2.1
- [ ] 1.3 Auditory features(phonetics, envelope, word onset, sentence boundary, F0,instantaneous frequency)
  - [ ] 1.3.1 Envelope
- [ ] 1.4 Linguistic features(phonetics, semantics, syntactics, context, Verb types)
- [ ] 1.5 Language model(Ngram, CFG, Fractality: Syntactic surprisal & Semantic Surprisal)
  - [ ] 1.5.1 N-gram model
  - [ ] 1.5.2 Context Free G model	
- [ ] 1.6 Temporal Response Function (TRF) Analysis
- [ ] 1.7 Aims of this study

### 2 Experiment 1

- [ ] 2.1 Hypothesis (Fractality model => A useful indicator on neural activity prediction?)
- [ ] 2.2 Methods and Materials
  - [x] 2.2.1 `(1st Draft_need to check on Natives)`Participants
  - [x] 2.2.2 `(1st Draft_need revised on REFs)` Stimuli
  - [x] 2.2.3 `(1st Draft)` Procedure (Same as Brennan & Hal, 2019 + Vocabulary Size Test)
  - [x] 2.2.4 `(1st Draft_need revised on ESL-EEG)` EEG recording
  - [x] 2.2.5 `(1st Draft_need to chech references descriptions)` EEG pre-processing
- [ ] 2.3 Statistical analyses (TRF)
- [ ] 2.4 Results (TRF)
- [ ] 2.5 Discussion

### 3 Experiment 2_LTTC

- [ ] 3.1 Hypothesis (How ESL learners’ proficiency level affect their VP detection abilities? (Arai & Keller, 2013))
- [ ] 3.2 Methods and Materials
  - [x] 3.2.1 `(1st Draft)` Participants
  - [ ] 3.2.2 Stimuli
  - [x] 3.2.3 `(1st Draft)` Procedure (Same as LTTC)
  - [ ] 3.2.4 MEG recording
  - [ ] 3.2.5 MEG pre-processing
- [ ] 3.3 Statistical analyses (ERPs_?? & TRF)
- [ ] 3.4 Results (TRFs)
- [ ] 3.5 Discussion

### 4 General Discussion and Conclusion

- [ ] 4.1 Summary
- [ ] 4.2 Applications
- [ ] 4.3 Limitations of this study and future directions

- [ ] ### References
- [ ] ### Appendixes
