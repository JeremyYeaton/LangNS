# Language-weighted NeuroSynth (LangNS)
This repository contains the scripts used to collect and a language-specific corpus of human neuroimaging articles from PubMedCentral, as well as extract and vectorize the vocabulary and generate NeuroSynth maps.

## Dependencies
You will need the following packages included in the [Anaconda distribuation]():
- [SciPy](https://scipy.org/)
- [NumPy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)

You will also need these packages which are not included in Anaconda:
- [Nilearn](https://nilearn.github.io/stable/index.html)
- [pubget](https://neuroquery.github.io/pubget/pubget.html)

The code is written in blocks for the Spyder IDE.

## How-to
### Query text (run 20 Nov. 2024)
(language processing OR language development OR language acquisition OR autism OR ASD OR psycholinguistic OR neurolinguistic OR morphosyntax OR morphosyntactic OR syntax OR syntactic OR phonological OR phonology OR composition OR semantic OR morphological OR phonetic OR sentence OR phrase OR phonemic OR phrase structure OR aphasia OR dementia OR apraxia of speech OR speech OR dld OR sli OR alzheimer OR PPA) AND (language OR linguistic) AND (imaging OR MRI OR fnirs OR MEG OR voxel OR sEEG OR intracranial)

### Query URL
https://www.ncbi.nlm.nih.gov/pmc/?term=(language+processing+OR+language+development+OR+language+acquisition+OR+autism+OR+ASD+OR+psycholinguistic+OR+neurolinguistic+OR+morphosyntax+OR+morphosyntactic+OR+syntax+OR+syntactic+OR+phonological+OR+phonology+OR+composition+OR+semantic+OR+morphological+OR+phonetic+OR+sentence+OR+phrase+OR+phonemic+OR+phrase+structure+OR+aphasia+OR+dementia+OR+apraxia+of+speech+OR+speech+OR+dld+OR+sli+OR+alzheimer+OR+PPA)+AND+(language+OR+linguistic)+AND+(imaging+OR+MRI+OR+fnirs+OR+MEG+OR+voxel+OR+sEEG+OR+intracranial)

Send to > file > Format[PMCID List]
