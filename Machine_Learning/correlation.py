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
    ax.set_title('Pearson correlation heatmap',fontsize = 25,pad = 20)
    sns.set(font_scale=2)
    sns.heatmap(correlations, vmax=1.0, center=0,  annot = False,square=True, linewidths=.5, cbar_kws={"shrink": 0.82,'label': 'Pearson correlation'})
    plt.savefig('pearson_correlation', bbox_inches = "tight")
    plt.show();
    
def highly_correlated_features(feature: str, limit: float, X, data):
    X = constant_removal(X)
    data = constant_removal(data)
    highly_correlated_features = data.columns[data.corr()[feature].abs() > limit]
    highly_correlated_features = highly_correlated_features.drop(feature)# drop the response variable
    X = X[highly_correlated_features]
    train = constant_removal(X)
    correlations = train.astype(float).corr()
    fig, ax = plt.subplots(figsize=(20,20))
    ax.set_title('Highly correlated features',fontsize = 25)
    sns.set(font_scale=2)
    heatmap = sns.heatmap(correlations, vmax=1.0, center=0,  square=True, annot = True,linewidths=.5,  cbar_kws={"shrink": 0.82,'label': 'Pearson correlation'},cmap = 'mako')
    heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation = 90) 
    heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation = 0) 
    heatmap.savefig('highly_correlated', bbox_inches = "tight")
    plt.show();

def shearman_correlation_heatmap(train):
    train = constant_removal(train)
    
    corr = spearmanr(train).correlation
    corr_linkage = ward(corr)
    # #Plot dendrogram
    # fig=  plt.figure(figsize=(20,20))
    # dendro = dendrogram(corr_linkage, labels=list(train.columns), leaf_rotation=90)
    # dendro_idx = np.arange(0, len(dendro['ivl']))
    # fig.tight_layout()
    # plt.savefig('dendrogram', bbox_inches = "tight")
    # plt.show();

    #Plot shearman correlation heatmap
    sns.set(font_scale=2)
    fig2, ax = plt.subplots(figsize=(20,20))
    ax.set_title('Spearman correlation heatmap',fontsize = 25,pad = 20)
    sns.heatmap(corr, vmax=1.0, center=0, fmt='.2f', square=True, linewidths=.5, cbar_kws={"shrink": 0.82,'label': 'Spearman correlation'},xticklabels=train.columns, yticklabels=train.columns)
    #ax.set_xticklabels(dendro['ivl'], rotation='vertical')
    #ax.set_yticklabels(dendro['ivl'], rotation='horizontal')
    plt.savefig('spearman_correlation', bbox_inches = "tight")
    fig2.tight_layout()
    plt.show();

    
def shearman_dendrogram(train):
    sns.set(font_scale=2)
    train = constant_removal(train)
    fig, ax1 = plt.subplots(1, 1, figsize=(20, 10))
    corr = spearmanr(train).correlation
    corr_linkage = ward(corr)
    dendro = dendrogram(corr_linkage, labels=list(train.columns), leaf_rotation=90, ax = ax1, leaf_font_size=20,color_threshold = 2)
    dendro_idx = np.arange(0, len(dendro['ivl']))
    ax1.set_title('Spearman correlation clustering',fontsize = 25,pad = 20)
    ax1.set_ylabel('Feature dissimilarity',fontsize = 20, labelpad = 20)
    ax1.set_xticks(dendro_idx, loc = 'center',fontsize = 20)
    ax1.set_yticks(dendro_idx, loc = 'center',fontsize = 20)
    ax1.xaxis.set_tick_params(fontsize = 20)
    ax1.yaxis.set_tick_params(fontsize = 20)
    ax1.tick_params(labelsize = 'large')
    ax1.tick_params(axis='x', which='major', labelsize=15)
    plt.savefig('dendrogram', bbox_inches = "tight")
    plt.show()
    
def shearman_dendrogram2(train):
    sns.color_palette("Paired")
    train = constant_removal(train)
    fig, ax1 = plt.subplots(1, 1, figsize=(5, 10))
    corr = spearmanr(train).correlation
    corr_linkage = ward(corr)
    dendro = dendrogram(corr_linkage,color_threshold = 1,get_leaves = False, no_labels=True)
    dendro_idx = np.arange(0, len(dendro['ivl']))
    ax1.axhline(y=1, c='grey', lw=1, linestyle='dashed')
    ax1.set_xticks(dendro_idx, loc = 'center',fontsize = 20)
    ax1.set_yticks(dendro_idx, loc = 'center',fontsize = 20)
    ax1.xaxis.set_tick_params(fontsize = 20)
    ax1.yaxis.set_tick_params(fontsize = 20)
    ax1.tick_params(labelsize = 'large')
    ax1.tick_params(axis='x', which='major', labelsize=15)
    ax1.axhline(y=3.5, c='grey', lw=1, linestyle='dashed')
    plt.savefig('dendrogram', bbox_inches = "tight")
    plt.show()