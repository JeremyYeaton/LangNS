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
After running the query below and downloading the files as a text file (or using the existing pmc_result file in the [OSF repository](https://osf.io/2f9yc/)), you can download the corpus using LangNS_Build_Corpus.py. It depends on LangNStools being in a directory called "scripts".

Once the files have been downloaded, extracted, and processed, the vocabulary will be vectorized, and [NeuroSynth](https://neurosynth.org/) maps will be produced for the terms in the vocabulary. You can customize the vocabulary by updating the mapping dictionary in LangNS_Build_Corpus, as well as the "excludeterms.txt" (removes terms from the vocabulary--can be overridden using the "exceptions" list in LangNS_Build_Corpus) and "interest_terms_tmp.txt" which pares down the vocabulary by only keeps term which contain one or more terms in the file.

If you want to run the basic NeuroSynth query tool in your browser, you can navigate to the folder containing your NeuroSynth maps in the command line and execute "flask run" which will allow you to interactively query the maps through a browser interface. You can also use query_LangNS.py to plot NeuroSynth maps onto the glass brain template from NiLearn.

If you use this code, please cite [Yeaton (2025)](https://doi.org/10.31234/osf.io/xku24) and/or the [corresponding OSF repository](doi.org/10.17605/OSF.IO/2F9YC), as well as the [NeuroSynth reference paper](https://doi.org/10.1038/nmeth.1635).

If you have any questions or run into any issues, feel free to contact me: jyeaton@uci.edu

### Query text (run 20 Nov. 2024)
(language processing OR language development OR language acquisition OR autism OR ASD OR psycholinguistic OR neurolinguistic OR morphosyntax OR morphosyntactic OR syntax OR syntactic OR phonological OR phonology OR composition OR semantic OR morphological OR phonetic OR sentence OR phrase OR phonemic OR phrase structure OR aphasia OR dementia OR apraxia of speech OR speech OR dld OR sli OR alzheimer OR PPA) AND (language OR linguistic) AND (imaging OR MRI OR fnirs OR MEG OR voxel OR sEEG OR intracranial)

#### Query URL
https://www.ncbi.nlm.nih.gov/pmc/?term=(language+processing+OR+language+development+OR+language+acquisition+OR+autism+OR+ASD+OR+psycholinguistic+OR+neurolinguistic+OR+morphosyntax+OR+morphosyntactic+OR+syntax+OR+syntactic+OR+phonological+OR+phonology+OR+composition+OR+semantic+OR+morphological+OR+phonetic+OR+sentence+OR+phrase+OR+phonemic+OR+phrase+structure+OR+aphasia+OR+dementia+OR+apraxia+of+speech+OR+speech+OR+dld+OR+sli+OR+alzheimer+OR+PPA)+AND+(language+OR+linguistic)+AND+(imaging+OR+MRI+OR+fnirs+OR+MEG+OR+voxel+OR+sEEG+OR+intracranial)

Send to > file > Format[PMCID List]
