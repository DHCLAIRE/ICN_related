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

- [ ] `(Zero) 2 parts_` Chinese Abstract---  
- [ ] `(Zero) 2 parts_` English Abstract---  
- [ ] `(Zero) 2 parts_` Aknoledgements--  
- [ ] `(Done)` Content Table---  
- [ ] `(Last to do)` List of Tables---  
- [ ] `(Last to do)` List of Figures---  

### 1 Introduction

- [ ] 1.1 `(Need to revise + add content) 3 parts_1&3 modified by the PI` Bilingualism and second language learning  
- [ ] 1.2 `(Need to revise + add content) 3 parts_1/2/3 modified by the PI` Speech comprehension  
- [ ] 1.3 `(Zero) 4 parts_` Auditory features (envelope, word onset, F0, instantaneous frequency_IF)  
- [ ] 1.4 `(Zero) 3 parts_` Linguistic features (Lexicality, semantic surprisal, syntactic surprisal_POS tags)
- [ ] 1.5 `(Zero) 2 parts_` Language model (Ngram, CFG)
  - [ ] 1.5.1 `(Zero) 3 parts_` N-gram model
  - [ ] 1.5.2 `(Zero) 3 parts_` Context Free G model	
- [ ] 1.6 `(Need to add content) 3 parts_` Temporal Response Function (TRF) Analysis
- [ ] 1.7 `(Need to add content) 3 parts_`Aims of this study

### 2 Experiment 1

- [ ] 2.1 `(Zero) 2 parts_` Intro  
- [ ] 2.2 Methods and Materials
  - [x] 2.2.1 `(1st Draft_need to check on Natives)`Participants
  - [x] 2.2.2 `(1st Draft_need revised on REFs)` Stimuli
  - [x] 2.2.3 `(1st Draft)` Procedure (Same as Brennan & Hal, 2019 + Vocabulary Size Test)
  - [x] 2.2.4 `(1st Draft_need revised on ESL-EEG)` EEG recording
  - [x] 2.2.5 `(1st Draft)_need to check refernces descriptions` EEG pre-processing
- [ ] 2.3 Results (TRF)
  - [x] 2.3.1 `1st_Env & onsetEnv//F0 & IF not included in here currently` Auditory response functions (Env / onsetEnv)  
  - [ ] 2.3.2 `(Zero) need description` Word class Categories: Function word and content word  
  - [ ] 2.3.2 `(Zero) need description` Language model: Ngram & CFG
- [ ] 2.4 `(Zero) 2 parts_` Summary

### 3 Experiment 2_LTTC

- [ ] 3.1 `(Zero) 2 parts_summarize it from LTTC`Intro  
- [ ] 3.2 Methods and Materials  
  - [x] 3.2.1 `(1st Draft)` Participants
  - [x] 3.2.2 `(1st Draft)` Stimuli
  - [x] 3.2.3 `(1st Draft)` Procedure (Same as LTTC)
  - [x] 3.2.4 `(1st Draft)` MEG recording
  - [ ] 3.2.5 `(Need to revise)` MEG pre-processing
- [ ] 3.3 Results (TRFs)  
  - [ ] 3.3.1 `(Need to revise + add content&graph+Stats)` Behavioral results (LDT)  
  - [ ] 3.3.2 `(Need to revise + add content&graph+Stats)` Sensor level of CD (ERP)  
- [ ] 3.4 `(Zero) 2 parts_` Summary

### 4 General Discussion and Conclusion

- [ ] 4.1 `(Zero)` Summary
- [ ] 4.2 `(Zero)` Differences in Natives & ESLs
- [ ] 4.3 `(Zero)` Surprisal representations not that useful?
- [ ] 4.4 `(Zero)` CFG not sig. in both groups (would materials influence the CFG? story主題性較發散, cfg對於主題性預測有關？)
- [ ] 4.5 `(Zero)` (Universal Grammar?)
- [ ] 4.6 `(Zero)` Application TRF analysis
- [ ] 4.7 `(Zero)` Limitation and the future direction

- [ ] ### References
- [ ] ### Appendixes
