# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:45:43 2021

@author: kariln
"""

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
from scipy.cluster.hierarchy import ward, dendrogram
import numpy as np
from dataset import constant_removal


def correlation_heatmap(train):
    train = constant_removal(train)
    correlations = train.astype(float).corr()
    fig, ax = plt.subplots(figsize=(20,20))
    sns.heatmap(correlations, vmax=1.0, center=0, fmt='.2f', square=True, linewidths=.5, annot=True, cbar_kws={"shrink": .70})
    plt.savefig('pearson_correlation', bbox_inches = "tight")
    plt.show();
    
def highly_correlated_features(feature: str, limit: float, X, data):
    X = constant_removal(X)
    data = constant_removal(data)
    highly_correlated_features = data.columns[data.corr()[feature].abs() > limit]
    highly_correlated_features = highly_correlated_features.drop(feature)# drop the response variable
    X = X[highly_correlated_features]
    correlation_heatmap(X)  

def shearman_correlation_heatmap(train, data):
    train = constant_removal(train)
    data = constant_removal(data)
    
    corr = spearmanr(train).correlation
    corr_linkage = ward(corr)
    #Plot dendrogram
    fig=  plt.figure(figsize=(20,20))
    dendro = dendrogram(corr_linkage, labels=data.columns, leaf_rotation=90)
    dendro_idx = np.arange(0, len(dendro['ivl']))
    fig.tight_layout()
    plt.savefig('dendrogram', bbox_inches = "tight")
    plt.show();

    #Plot shearman correlation heatmap
    fig2, ax = plt.subplots(figsize=(20,20))
    sns.heatmap(corr[dendro['leaves'], :][:, dendro['leaves']], vmax=1.0, center=0, fmt='.2f', square=True, linewidths=.5, annot=True, cbar_kws={"shrink": 0.7},xticklabels=dendro['ivl'], yticklabels=dendro['ivl'])
    ax.set_xticks(dendro_idx, loc = 'center')
    ax.set_yticks(dendro_idx, loc = 'center')
    #ax.set_xticklabels(dendro['ivl'], rotation='vertical')
    #ax.set_yticklabels(dendro['ivl'], rotation='horizontal')
    plt.savefig('spearman_correlation', bbox_inches = "tight")
    fig2.tight_layout()
    plt.show();
