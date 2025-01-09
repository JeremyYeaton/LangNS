#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build and process corpus of Language Neuroscience literature, prepare & query NeuroSynth maps

Created 20 Nov. 2024

@author: Jeremy Yeaton

Requires pubget: https://pypi.org/project/pubget/
"""

import pubget as pg
from scripts import LangNStools as lnst

#%% Step 1: Query PubMedCentral and get list of PMCIDs
''' Query run 20 Nov. 2024
(language processing OR language development OR language acquisition OR autism OR ASD OR psycholinguistic OR neurolinguistic OR morphosyntax OR morphosyntactic OR syntax OR syntactic OR phonological OR phonology OR composition OR semantic OR morphological OR phonetic OR sentence OR phrase OR phonemic OR phrase structure OR aphasia OR dementia OR apraxia of speech OR speech OR dld OR sli OR alzheimer OR PPA) AND (language OR linguistic) AND (imaging OR MRI OR fnirs OR MEG OR voxel OR sEEG OR intracranial)
https://www.ncbi.nlm.nih.gov/pmc/?term=(language+processing+OR+language+development+OR+language+acquisition+OR+autism+OR+ASD+OR+psycholinguistic+OR+neurolinguistic+OR+morphosyntax+OR+morphosyntactic+OR+syntax+OR+syntactic+OR+phonological+OR+phonology+OR+composition+OR+semantic+OR+morphological+OR+phonetic+OR+sentence+OR+phrase+OR+phonemic+OR+phrase+structure+OR+aphasia+OR+dementia+OR+apraxia+of+speech+OR+speech+OR+dld+OR+sli+OR+alzheimer+OR+PPA)+AND+(language+OR+linguistic)+AND+(imaging+OR+MRI+OR+fnirs+OR+MEG+OR+voxel+OR+sEEG+OR+intracranial)

Send to > file > Format[PMCID List]
'''

queryfile = 'pmc_result_11-20-24.txt'

lns = lnst.LangNS()

lns.pmcids = [i for i in lns.get_pmcids(queryfile)]

#%% Step 2: Download articles and extract data
# Download article sets
dlOut = pg.download_pmcids(lns.pmcids, data_dir = lns.pubget_dir)

# Extract articles from article sets
exOut = pg.extract_articles(articlesets_dir=dlOut[0])

# Extract data from articles with coordinates
dtOut = pg.extract_data_to_csv(articles_dir=exOut[0],articles_with_coords_only=True)

# Extract vocabulary
vbOut = pg.extract_vocabulary_to_csv(extracted_data_dir=dtOut[0])

#%% Step 3: Prepare terms list
# Read in vocabulary
query_dir = lns.pubget_dir + 'pmcidList_132ba1648e0222ccee1e8ace8cf5b3c4/'
vocab_dir = query_dir + 'subset_articlesWithCoords_extractedVocabulary/'

# Create a copy of the original vocab file
f = open(vocab_dir + 'vocabulary.csv','r')
g = open(vocab_dir + 'vocabulary_orig.csv','w')
for line in f:
    g.write(line)
g.close()
f.close()

# Extract terms and frequency
f = open(vocab_dir + 'vocabulary.csv','r')

vocab = [line[:-1].split(',') for line in f]
# Filter terms so the first & last chars are non-numeric, and len(term) > 1
vocab = [i for i in vocab if len(i[0]) > 2 and not i[0][0].isnumeric() and not i[0][-1].isnumeric()]
# get separate list of terms
words = [i[0] for i in vocab]
f.close()

# Remove irrelevant/unhelpful terms
f = open('scripts/excludeterms.txt','r')
badwords = [i[:-1] for i in f]
f.close()

g=open('tmp2.txt','w')
vocab2 = []
for V in vocab:
    v = '|'+V[0]
    allGood = True
    for b in badwords:
        if b in v:
            allGood = False
            break
    if v[:3] == 'al ' or v[:3] == 'et ' or v[-3:] == ' et':
        allGood = False
    if allGood:
        vocab2.append(V)
        g.write(v+'\n')

exceptions = ['iq','function word','function words','functional morphological',
              'non word','non canonical', 'non words','lower case','upper case',
              'n back','non fluent','n400','p600','n1','n100','p250','p2',
              'lan','elan','p300','f0','af','structural prime','structural priming',
              'ifs','addition subtraction','addition multiplication','multiple demand',
              'one letter','complete sentence','picture description','verbal description',
              'thalamus','subject extracted','subject object','subject predicate',
              'subject relative','angular gyrus','resting state','ilf','frontal aslant',
              'inferior longitudinal','filler gap','angular gyrus','gyrus ag',
              'predicate','past tense','part speech','semantically reversible','reversible sentences','center embedded']
for i in exceptions:
    vocab2.append(i)
g.close()

# Pick out terms of interest (comment out for longer list in vocab_new.csv)
f = open('scripts/interest_terms_tmp.txt','r')
terms = [i[:-1] for i in f]
f.close()
vocab3 = []
for v in vocab2:
    for i in terms:
        if i in v[0]:
            vocab3.append(v)
            break
f = open(vocab_dir + 'vocab_new.csv','w')
for i in vocab3:
    f.write(','.join(i) + '\n')
f.close()

#%% Combine related terms in vocab

words3 = [i[0] for i in vocab3]
mapping = ''
for Idx,i in enumerate(vocab3):
    v = i[0]
    if v[:-1] in words3:
        if v[-1] == 's' and not v not in ['passive sentences','passives','actives','active sentences']:
            mapping = mapping + lns.makemap(v,v[:-1])

manual_maps = {'adverb':['adv','adverbial'],
               'agrammatic':['agrammatic aphasia'],
               'alexia':['alexic'],
               'ambiguity':['processing ambiguous','ambiguities'],
               'amnesia':['amnesic'],
               'anomia':['anomic','anomic aphasia'],
               'argument structure':['argument verb','verb argument'],
               'arithmetic':['mathematical','mathematic','arithmetical','addition subtraction','subtraction addition','subtraction multiplication','subtraction problem','subtraction problems','simple multiplication','multiplication division'],
               'artificial grammar':['artificial language'],
               'asd':['autism','autistic'],
               'atl damage':['atl lesions'],
               'audiovisual speech':['av speech'],
               'backward digit':['backwards digit'],
               'bigram frequency':['bigram','trigram'],
               'bisyllabic':['disyllabic','trisyllabic'],
               'bnt':['boston naming'],
               'braille':['braille readers','braille reading'],
               'broca wernicke':['wernicke broca'],
               'bvftd':['bv ftd'],
               'case marking':['case marker'],
               # 'clause':['clausal'],
               'character reading':['character processing','character recognition'],
               'cloze probability':['cloze'],
               'cochlea':['cochlear'],
               'color naming':['colour naming'],
               'color word':['colour word'],
               'composition':['compositional'],
               'conflict error':['error conflict'],
               'conflict monitoring':['monitoring conflict'],
               'congenital deafness':['congenitally deaf','born deaf'],
               'congenital blindness':['congenitally blind'],
               'confrontation naming':['confrontational naming'],
               'consonant vowel':['consonants vowels','vowel consonant'],
               'consonant':['consonance'],
               'constituent words':['constituents words'],
               'covert speech':['silent speech'],
               'dance':['dancing'],
               'default mode':['dmn'],
               'dependency':['dependencies'],
               'dorsal attentional':['dorsal attention','dan'],
               'dysarthria':['dysarthric'],
               'dysfluencies':['disfluencies','dysfluent','dysfluency','disfluencies','disfluency'],
               'dyslexia':['dyslexic'],
               # 'embedded clause':['relative clause'],
               'error monitoring':['monitoring error'],
               'ftd':['ftld'],
               'generative process':['generative processes','generativity'],
               'go nogo':['nogo go'],
               'grammatical':['syntactical'],
               'grapheme phoneme':['graphemes phonemes','phoneme grapheme'],
               'harmonic':['harmonized','harmony'], 
               'hierarchical organization':['hierarchically organized'],
               'hierarchical structure':['tree structure'],
               'hippocampus':['hippocampal','hippocampi'],
               'homophone':['homophonic'],
               'humming':['hum','humming sounds'],
               'humor':['humour','humorous','joke'],
               'humor comprehension':['humor processing'],
               'idiom':['idiomatic'],
               'ifg triangularis':['ifg tri','ifg triangular','pars triangularis','ifgtri','ifgtriang'],
               'ifg opercularis':['ifg oper','ifg opercular','pars opercularis','ifgop','ifgoper','ifgoperc'],
               'ifg orbitalis':['ifg orb','ifg orbital','pars orbitalis','ifgorb'],
               'inflectional morphology':['inflected forms','inflected words','verb agreement','agreement number','verb inflection'], # ,'functional morphological'
               'insula':['insular'],
               'irregular word':['words irregular'],
               'l2 learning':['l2 learners','l2 processing','l2 proficiency'],
               'language processing':['language processes'],
               'language production':['production language'],
               'letter string':['consonant string','string letters'],
               'letter word':['letters word','word letter','words letter'],
               'lexical access':['access lexical','access word'],
               'lexical category':['lexical categories'],
               'lexical processing':['lexical processes'],
               'lexical retrieval':['word retrieval'],
               'lexical semantic':['lexicosemantic'],
               'lexical competition':['competing lexical','competing words'],
               'lexical tone':['tonal language'],
               'linguistic processing':['linguistic processes'],
               'lipreading':['lip reading'],
               'lips tongue':['lip tongue'],
               'literacy':['illiterate','illiteracy','literate'],
               'melody':['melodic','melodies'],
               'lvppa':['logopenic','logopenic variant'],
               'mindreading':['mind reading','mind abilities','mind ability','mind processes','mind processing','reading mind'],
               'metaphor':['nonliteral','figurative language','metaphoric','metaphorical'],
               'mnemonic processing':['mnemonic processes'],
               'monosyllabic':['monosyllabic word'],
               'morphosyntactic':['morphosyntax','morpho syntactic','morphologically','morphological processing','morphologically complex','derivational','morpheme','morphemic','morpho'],
               'multiplication':['multiplication problem'],
               'music processing':['processing musical','processing music','musical processing'],
               'narrative comprehension':['narrative processing'],
               'negative valence':['negatively valenced'],
               'nfvppa':['nonfluent variant','aphasia nfvppa','agrammatic variant','nonfluent agrammatic'],
               'nonfluent':['nonfluent aphasia','non fluent'],
               'nonword repetition':['pseudoword repetition'],
               'noun verb':['nouns verb','verb noun','verbs nouns'],
               'object naming':['object name'],
               'omission error':['errors omission'],
               'orthographic':['spelled','symbol string','orthography'], # to return
               'overt naming':['overt picture','name aloud','oral naming'],
               'palpa':['aphasia palpa'],
               'parahippocampus':['parahippocampal','para hippocampus'],
               'parse':['parsed','parsing'],
               'phonic':['letter sound'],
               'passive sentences':['passives','actives','active voice','passive voice'],
               'phonological access':['access phonological'],
               'phonological loop':['phonological working','phonological memory'],
               'phrase':['phrasal'],
               'picture naming':['name picture','named pictures','naming picture'],
               'pitch processing':['processing pitch'],
               'plausibility':['implausible'],
               'pmtg':['posterior mtg'],
               'posterior dmn':['pdmn'],
               'posterior insula':['posterior insular'],
               'posterior thalamus':['posterior thalamic'],
               'posterior hippocampus':['posterior hippocampi','posterior hippocampal'],
               'poststroke aphasia':['stroke aphasia'],
               'ppa':['primary progressive','progressive aphasia'],
               'preposition':['prepositional','prepositional phrase'],
               'primary auditory':['a1 primary'],
               'prime word':['word prime'],
               'prosody':['prosodic'],
               'prosody processing':['prosodic processing','prosody perception'],
               'pseudoword':['pseudo word','non word','nonword','nonsense word','word non','word nonword','words non','words nonwords','pseudoword word','words pseudowords','word pseudoword','pseudowords words','word pseudo'],
               'pseudoword reading':['nonword reading','reading pseudoword'],
               'pstg':['posterior stg'],
               'psts':['posterior sts'],
               'pwi':['picture word','word interference'],
               'reading':['read'],
               'reading acquisition':['learn read','learned read','acquisition reading','learning read'],
               'reading chinese':['scripts chinese','readers chinese','written chinese','character chinese','characters chinese','chinese logographic','chinese orthographic'],
               'reading difficulty':['reading difficulties','reading deficit','deficits reading','reading problems'],
               'reading disability':['reading disabilities','reading disorder'],
               'reading fluency':['fluent reading'],
               'reading processes':['reading processing','reading process'],
               'reading proficiency':['proficient reading','proficient readers','reading ability'],
               'reading written':['word written','words written'],
               'regular word':['words regular'],
               'reinterpretation':['reinterpret','reinterpreting'],
               'rhyme judgment':['rhyming judgment','homophone judgment','phonological judgment'],
               'rhyme':['rhyming','rhymed'],
               'rhythm':['rhythmic'],
               'sarcasm':['irony sarcasm','sarcastic'],
               'schizophrenia':['schizophrenic','schizophreniform'],
               'self referential':['self reference'],
               'semantic access':['access semantic'],
               'semantic congruency':['semantically congruent','semantically incongruent','semantic violation'],
               'semantic judgment':['semantic judgement','synonym judgment'],
               'sentence context':['sentential context'],
               'sentence length':['length sentence'],
               'sentence listening':['listened sentence','heard sentence'],
               'sentence picture':['picture sentence'],
               'sentence processing':['processing sentence'],
               'sentence production':['production sentence','produce sentence','produced sentence','generate sentence','sentence construction','structure building'], # 'sentence generation',,'generation sentence'
               'sentence reading':['reading sentence'],
               'sentence repetition':['repetition sentence','repeated sentences'],
               'sentence structure':['structure sentence'],
               'sign language':['american sign','british sign','bsl','deaf signers','spoken signed','signed language'],
               'silent reading':['silently read','passive reading'],
               'single letter':['one letter'],
               'sma':['supplementary motor'],
               'speech monitoring':['monitoring speech'],
               'speech production':['produce speech','produced speech','production speech','producing speech'],
               'spelling':['spell','spelled'],
               'spoken word':['word spoken','words spoken'],
               'spoken sentence':['sentences spoken'],
               'statistical dependencies':['statistical dependence'],
               'stuttering':['stutter','stuttered'],
               'subject object':['subjects objects'],
               'sublexical':['sub lexical'],
               'subthalamic':['subthalamic nucleus'],
               'subvocal':['sub vocal','subvocalization','subvocal rehearsal'],
               'svppa':['semantic variant','semantic dementia'],
               'syllabic structure':['syllabification'],
               'synonym judgment':['synonym judgement'],
               'syntactic':['syntax','syntactically','grammatically'],
               'syntactic category':['grammatical categories','grammatical category','grammatical class','part speech'],
               'syntactic complexity':['syntactically complex','complexity sentences','sentence complexity'],
               'syntactic dependencies':['local dependencies','distance dependencies','dependency structure'],
               'syntactic processing':['syntactic processes','grammatical processing','grammar processing','processing syntactic','processing syntactically','processing syntax'],
               'syntactic rules':['grammatical rules'],
               'syntactic structure':['grammatical structure'],
               'temporoparietal junction':['tpj'],
               'text comprehension':['text processing','reading comprehension'],
               'thalamus':['thalamic'],
               'thematic role':['agent patient','semantic role'],# ,'role assignment'
               'tom':['theory mind'],
               'tone':['tonal'],
               'tone processing':['processing tone','processing tonal','tone perception'],
               'transition probability':['transition probabilities'],
               'transitive sentences':['transitive verb','transitivity','transitive'], # 'intransitive verb','transitive intransitive',
               'unambiguous':['unambiguously'],
               'ungrammatical':['syntactic violation'],
               'valence':['valenced'],
               'valenced words':['valence word'],
               'verb naming':['action naming','processing verb'],
               'verbal iq':['iq verbal'],
               'verbal wm':['verbal working'],
               'verbal nonverbal':['verbal non'],
               'verbal episodic':['episodic verbal'],
               'voice processing':['processing voice'],
               'voice recognition':['recognition voice'],
               'vocoded speech':['noise vocoded'],
               'vocalization':['vocalisation','vocalize','vocalized','vocalizing'],
               'vocabulary learning':['vocabulary acquisition'],
               'vocal production':['vocal output','vocal expression'],
               'wab':['western aphasia','wab aq'],
               'wais':['wechsler','wais iv','wais wechsler'],
               'word order':['canonical word','noncanonical','canonical sentence','words order', 'order word','non canonical'],
               'word reading':['words reading','words read','reading word'],
               'word recall':['recalled words','recall word'],
               'word comprehension':['comprehension word'],
               'word category':['word categories','word class'],
               'word frequency':['word frequencies'],
               'word length':['words length','length word'],
               'word production':['production word'],
               'working memory':['wm working'],
                'past tense':['past future','past present','present past','present tense','present future','future present','tense form','tense verb'],
                'embedded sentence':['embedded clause','subordinate clause'],
                'relative clause':['subject relative','object extracted','subject extracted','extracted relative']
                # 'object relative':['subject relative','object extracted','subject extracted','extracted relative'], # 'relative clause'
               }


for key in manual_maps:
    for i in manual_maps[key]:
        mapping = mapping + lns.makemap(i,key)
        # mapping = mapping + makemap(pair[0],pair[1])

f = open(vocab_dir + 'vocab_new.csv_voc_mapping_identity.json','w')
f.write('{')
f.write(mapping[:-1])
f.write('}')
f.close()
#%% Vectorize vocabulary
# query_dir = '/Users/jyeaton/meta_analysis_raw2/pmcidList_5b8b0b5d716e703081119e1c9ddd6746/'
query_dir = 'raw_data/pmcidList_132ba1648e0222ccee1e8ace8cf5b3c4/'
vocab_dir = query_dir + 'subset_articlesWithCoords_extractedVocabulary/'
data_dir = query_dir + 'subset_articlesWithCoords_extractedData'

vcOut = pg.vectorize_corpus_to_npz(extracted_data_dir = data_dir,\
                                    vocabulary = vocab_dir + 'vocab_new.csv', n_jobs = 8)

#%% Fit Neurosynth model

neurosynthOut = pg.fit_neurosynth(tfidf_dir=vcOut[0],\
                                  extracted_data_dir=data_dir, n_jobs=8)

'''
navigate to folder in terminal, then execute:
flask run
'''