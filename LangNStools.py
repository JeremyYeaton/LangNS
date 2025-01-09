#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build and process corpus of Language Neuroscience literature, prepare & query NeuroSynth maps

Created 20 Nov. 2024

@author: Jeremy Yeaton

Requires pubget: https://pypi.org/project/pubget/
"""

import os
from pathlib import Path

import numpy as np
from scipy import sparse
import pandas as pd
from nilearn import image
from matplotlib import pyplot as plt

try:
    from nilearn import maskers, plotting
except ImportError:
    from nilearn import input_data as maskers
from nilearn.plotting import view_img
from nilearn.glm import fdr_threshold

class LangNS:
    def __init__(self,query=False,data_dir=''):
        self.pubget_dir = 'raw_data/'
        self.pmcids = None
        if not os.path.isdir(self.pubget_dir):
            os.mkdir(self.pubget_dir)
        if query:
            self.pmc_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{}"
            if data_dir == '':
                self.data_dir = Path(__file__).resolve().parent
            else:
                self.data_dir = data_dir
            self.maps_dir = self.data_dir.joinpath("neurosynth_maps")
            self.terms_info = pd.read_csv(str(self.data_dir.joinpath("terms.csv")), index_col=0)
            self.terms_info["pos"] = np.arange(self.terms_info.shape[0])
            self.metadata = pd.read_csv(str(self.data_dir.joinpath("metadata.csv")))
            self.tfidf = sparse.load_npz(str(self.data_dir.joinpath("tfidf.npz")))
            self.masker = maskers.NiftiMasker(str(self.data_dir.joinpath("brain_mask.nii.gz"))).fit()
    
    def get_pmcids(self,fileName):
        '''
        Download PMCIDs from file
        '''
        f = open(self.pubget_dir + fileName,'r')
        pmcids = []
        for line in f:
            pmcids.append(line[3:-1])
        f.close()
        return pmcids
    
    def makemap(self, term, replacement):
        # term: replacement
        return '"' + term + '":"' + replacement +'",'

    def title_as_link(self,df):
        urls = []
        for _, row in df.iterrows():
            paper_url = self.pmc_url.format(row["pmcid"])
            link = f"""<a href="{paper_url}" target="_blank">{row["title"]}</a>"""
            urls.append(link)
        return urls

    def get_docs_list(self,term):
        loadings = self.tfidf[:, self.terms_info.loc[term, "pos"]].A.ravel()
        # get number of studies
        nstudies = (loadings > 0).astype('int32').sum()
        order = np.argpartition(-loadings, np.arange(nstudies))[:nstudies]
        similar_docs = self.metadata.iloc[order].copy()
        similar_docs["similarity"] = loadings[order]
        similar_docs["title_link"] = self.title_as_link(similar_docs)
        return similar_docs

    def get_image(self,term,threshold_val=0.01):
        term_file_name = self.terms_info.loc[term, "file_name"]
        img_path = self.maps_dir.joinpath(f"{term_file_name}.nii.gz")
        img = image.load_img(str(img_path))
        threshold = fdr_threshold(self.masker.transform(img).ravel(), threshold_val)
        return [img,threshold]

    def query_a_term(self,term,threshold=0.01,display_mode='ortho',colormap=''):
        similar_docs = self.get_docs_list(term)
        self.figure = self.NSfig()
        self.figure.img, self.figure.threshold = self.get_image(term,threshold)
        print(term+': An automated meta-analysis of ' + str(len(similar_docs))+' studies')
        return(similar_docs)
    
    def makefig(self,term,args,save=True):
        cmap = 'viridis'
        if not args == []:
            cmap = args[0]
        studies = self.query_a_term(term,display_mode='ylz',threshold=0.01)
        nstudies = len(studies)
        title = '``'+term+'" ('+str(nstudies)+' studies)'
        fig = plotting.plot_glass_brain(self.figure.img,
                                        threshold=self.figure.threshold,
                                        display_mode='ylz',
                                        colorbar=True,
                                        cmap=cmap
                                        )
        fig.title(title,bgcolor='w',color='k',size=20,alpha=0)
        if len(args) > 1:
            fig._cbar.set_ticks(ticks=args[1],labels=args[1],fontsize=16)
        # fig._cbar.set_ticks([3,6,9,12])
        plotting.show()
        if save:
            fig.savefig('figures/NS_'+term+'.png',dpi=300)
        return fig, studies
    
    class NSfig:
        def __init__(self):
            self.threshold = None
            self.img = None
    
#%%