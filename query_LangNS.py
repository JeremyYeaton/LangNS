#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Query NeuroSynth maps and documents from constructed corpus

Created 20 Nov. 2024

@author: Jeremy Yeaton
"""

from pathlib import Path
import numpy as np
from scripts import LangNStools as lnst

from scipy.ndimage import binary_dilation
from matplotlib.colors import ListedColormap, to_rgb
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

from nilearn import plotting


data_dir = Path('raw_data/pmcidList_132ba1648e0222ccee1e8ace8cf5b3c4/subset_articlesWithCoords-voc_2f6db5be2cc57c713b5ea554efcd038a_neurosynthResults/')
# data_dir = Path('/Users/jyeaton/Library/CloudStorage/OneDrive-UCIrvine/expressive_syntax/NeuroSynth_Lang/raw_data/pmcidList_132ba1648e0222ccee1e8ace8cf5b3c4/subset_articlesWithCoords-voc_09de558b0c314c28e6fb9bc14a74844c_neurosynthResults/')
# /Users/jyeaton/Library/CloudStorage/OneDrive-UCIrvine/expressive_syntax/NeuroSynth_Lang/

lns = lnst.LangNS(query=True,data_dir = data_dir)

#%% Dict of figures
figs2plot = {'sentence production':['inferno',[0,4,6]],
             'sentence repetition':['cividis_r',[0,4,6]],
             'syntactic processing':['plasma_r',[0,4,8,11]],
             'morphosyntactic':['viridis',[0,4,6]],
             # 'pronoun':['viridis_r',[0,2,4,6]],
             'clause':['plasma',[0,4,6,8]],
              # 'embedded clause':['Oranges',[0,2,4,6,8]],
              'relative clause':['Reds',[0,4,6,8]],
             # 'phrase':['Purples',[0,2,4,6,8]],
             'verb phrase':['Blues',[0,4,6]],
              'noun phrase':['Reds',[0,4,6,8]],
             # 'transitive sentences':['Greens',[0,2,4,6,8]],
             'word order':['RdPu',[0,4,6,8]],
             # 'syntactic dependencies':['GnBu',[0,2,4,6]],
             'lexical syntactic':['magma',[0,4,6,8]],
             'lexical selection':['Purples',[0,4,6]],
             'semantic processing':['viridis_r',[0,4,8,12]],
             # 'argument structure':['YlOrBr',[0,2,4,6]],
             'thematic role':['PuOr_r',[0,4,6,8]],
             'syntactic':['jet',[0,4,8,12]],
             'grammatical':['jet_r',[0,4,6,8]]
    }
#%%
shortlist = ['sentence production','sentence repetition','syntactic processing',
             'morphosyntactic','clause','relative clause','verb phrase','noun phrase','word order',
             'lexical selection','lexical syntactic','semantic processing','thematic role',
             'syntactic','grammatical'
             ] # 'pronoun','embedded clause','phrase','noun phrase','argument structure','syntactic dependencies','transitive sentences',

for term in shortlist:
    fig,studies = lns.makefig(term,figs2plot[term],save=False)
    studies.to_csv('study lists/studyList_'+term+'.csv')
#%%
# TODO: make tables with lists of studies for each term?    

#%%
term = 'sentence production'
fig,studies = lns.makefig(term,['jet_r'],save=False)

#%%


tex = studies.drop(labels=['license','title_link'],axis=1).to_latex(index=False)

tex2 = ''.join([char for char in tex if not char in ['\n']])


#%%
term = 'sentence'
studies = lns.query_a_term(term,display_mode='ylz',threshold=0.01)
nstudies = len(studies)
title = '``'+term+'" ('+str(nstudies)+' studies)'
fig = plotting.plot_glass_brain(lns.figure.img,
                                threshold=lns.figure.threshold,
                                # plot_abs=False,
                                # title=term,
                                vmin = lns.figure.threshold,
                                # symmetric_cbar=False,
                                display_mode='ylz',
                                colorbar=True,
                                cmap='jet'
                                )
fig.title(title,bgcolor='w',color='k',size=18,alpha=0)
# fig._cbar.set_ticks([0,4,7,10])
plotting.show()
# fig.savefig('figures/NS_'+term+'.png',dpi=300)



#%%
figs2plot = {'clause':['plasma_r',[0,2,4,6,8]],
              'sentence production':['plasma',[0,2,4,6]],
              'sentence comprehension':['Reds'],
              'syntactic':['jet'],
              'verb phrase':['Purples'],
               # 'verb naming':[],
              'phrase':['Blues'],
              'syntactic category':['Greens'],
              'sentence repetition':['magma'],
              'syntactic complexity':[],
              'morphosyntactic':['inferno_r'],
              'lexical syntactic':['viridis'],
              'lexical access':[],
              'lexical selection':['inferno'],
              'semantic':['cividis_r'],
    #          'semantic congruency':[],
    #          'processing semantic':[],
              'preposition':[],
              'ungrammatical':['blue_purple'],
              'grammatical':['purple_blue_r'],
    #          'default mode':[],
    #          'multiple demand':[],
    #          'ambiguity':[],
              'argument structure':[],
              'thematic role':[],
    #          'orthographic':[],
              'sentence structure':[],
              'transitive sentences':[],
              'narrative comprehension':[],
              'sentence length':[],
    #          'working memory':[],
              'noun verb':[],
              'subject verb':[],
             # 'ifg triangularis':[],
             # 'ifg opercularis':[],
             # 'pmtg':[],
              'action verb':[],
             # 'addition multiplication':[],
             # 'arithmetic processing':[],
             # 'primary auditory':[],
             # 'primary motor':[],
              'adjective':[],
              'adjective noun':[],
             # 'alzheimer':[],
             # 'syllabic structure':[],
              # 'animacy':[],
             # 'arcuate fasciculus':[],
             # 'auditory comprehension':[],
             # 'bdae':[],
             # 'bigram frequency':[],
             # 'bisyllabic':[],
             # 'broca':[],
             # 'broca aphasia':[],
             # 'broca wernicke':[],
              'canonical language':[],
             # 'categorical perception':[],
             # 'chinese character':[],
             # 'chord':[],
             # #'complete sentence':[],
              'concrete noun':[],
             # 'conduction aphasia':[],
             # 'confrontation naming':[],
             # 'consonant vowel':[],
             # 'covert speech':[],
             # # 'picture description':[],
             # 'spt':[],
             # 'dysfluencies':[],
             # 'dyslexia':[],
              'embedded clause':[],
              'embedded sentence':[],
             # 'episodic memory':[],
             # 'form meaning':[],
              'grammar':[],
              'grammatical errors':[],
              'grammatically correct':[],
             # 'grapheme phoneme':[],
             # 'harmonic structure':[],
             # 'harmonic':[],
             # 'hickok':[],
             # 'poeppel':[],
              'hierarchical structure':[],
             # 'homophone':[],
             # 'idiom':[],
             # 'ifof':[],
             # 'insula':[],
             # 'intonation':[],
              'language production':[],
             # 'language':[],
             # 'letter processing':[],
             # 'letter string':[],
             # 'letter word':[],
             # 'lexical competition':[],
             # 'lexical decision':[],
             # 'lexical processing':[],
              'lexical retrieval':['cividis'],
             # 'lexical semantic':[],
             # 'lexical tone':[],
             # 'linguistic':[],
             # 'literal':[],
             # 'logographic':[],
             # 'meaning':[],
              'syntactic movement':[],
             # 'mtg':[],
             # 'stg':[],
              'pmtg':[],
             # 'pstg':[],
             # 'sts':[],
             # 'psts':[],
             # 'music':[],
             # 'music listening':[],
             # 'music processing':[],
             # 'music perception':[],
             # 'naming':[],
             # 'naming repetition':[],
             # 'picture naming':[],
              'nominative':[],
             # 'nonverbal iq':[],
             # 'nonword repetition':[],
              'noun':[],
              'noun phrase':[],
             # 'numerical processing':[],
             # 'object naming':[],
              'object relative':[],
              'object sentence':[],
             # 'overt speech':[],
              'parse':[],
              'passive sentences':[],
             # 'phoneme':[],
             # 'phonetic features':[],
             # 'phonological':[],
              'phrase structure':[],
             # 'pitch discrimination':[],
             # 'planum temporale':[],
             # 'primary sensorimotor':[],
             # 'primary somatosensory':[],
              'pronoun':[],
             # 'prosody processing':[],
             # 'prosody':[],
             # 'putamen':[],
             # 'pwi':[],
             # 'reading aloud':[],
             # 'reading disability':[],
             # 'reading':[],
              'reinterpretation':[],
              'relative clause':[],
             # 'schizophrenia':[],
              'semantic processing':[],
             # 'sensorimotor':[],
              'sentence listening':[],
              'sentence picture':[],
              'sentence processing':[],
              'sentence reading':[],
              'sentence':[],
             # 'sign language':[],
             # 'silent reading':[],
              'simple sentence':[],
             # 'sma':[],
             # 'smg':[],
             # 'somatosensory':[],
             # 'speech articulation':[],
             # 'speech comprehension':[],
             # 'speech error':[],
             # 'speech fluency':[],
             # 'speech listening':[],
             # 'speech monitoring':[],
             # 'speech motor':[],
             # 'speech perception':[],
             # 'speech processing':[],
             # 'speech production':[],
             # 'speech prosody':[],
             # 'spelling':[],
             # 'spoken language':[],
              'spoken sentence':[],
             # 'spoken word':[],
              'subject object':[],
             # # 'predicate':[],
             'subject relative':[],
             # 'sublexical':[],
             'subordinate clause':[],
             # 'svppa':[],
             # 'syllabic':[],
             'syntactic dependencies':[],
             'syntactic processing':[],
             'syntactic rules':[],
             'syntactic semantic':[],
             'syntactic structure':[],
             # 'temporoparietal':[],
             # 'temporoparietal junction':[],
             # 'text comprehension':[],
             # 'thalamus':[],
             # 'hippocampus':[],
             # 'tip tongue':[],
             # 'tom':[],
             # 'mentalizing':[],
             # 'tone processing':[],
             # 'subvocal':[],
             # 'turkeltaub':[],
             # 'valenced words':[],
              'verb object':[],
             'verb processing':[],
             'verb':[],
             'verbal wm':[],
             # 'vocal production':[],
             # 'vocal':[],
             # 'vocoded speech':[],
             # 'voice processing':[],
             # 'voice':[],
             # 'voicing':[],
             # 'vowel':[],
             # 'consonant':[],
             # 'vwfa':[],
             'wab':[],
             'wernicke aphasia':[],
             'wernicke':[],
             # 'word form':[],
             # 'word frequency':[],
             # 'word length':[],
             # 'word meaning':[],
             'word order':[],
             # 'word processing':[],
              'word production':[],
             # 'word reading':[],
             'word repetition':[],
             }

#%%
def get_cmap(hexcode):
    N = 256
    frac = 8/16
    nbig = int(frac*N)
    nsmall = int((1-frac)*N)
    vals = np.ones((N, 4))
    rgbvals = to_rgb(hexcode)
    vals[nbig:, 0] = np.linspace(1,rgbvals[0], nsmall)
    vals[nbig:, 1] = np.linspace(1,rgbvals[1], nsmall)
    vals[nbig:, 2] = np.linspace(1,rgbvals[2], nsmall)
    newcmp = ListedColormap(vals)
    return newcmp

def solid_cmap(hex_code):
    N = 256
    vals = np.ones((N, 4))
    rgbvals = to_rgb(hex_code)
    vals[:, 0] = rgbvals[0]
    vals[:, 1] = rgbvals[1]
    vals[:, 2] = rgbvals[2]
    newcmp = ListedColormap(vals)
    return newcmp

def binarize_map(img,threshold):
    tmp = image.get_data(img)
    tmp = (tmp > threshold)
    tmp = binary_dilation(tmp)
    return image.new_img_like(img, tmp.astype('int32'))
