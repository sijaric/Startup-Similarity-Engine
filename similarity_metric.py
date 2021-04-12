import os
import sys
import math
import numpy as np
import pandas as pd
from difflib import SequenceMatcher
from progress_bar import progress_bar

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# Turn the training dataframe into a lightweight Dictionary ===================
# Get names of all parent companies in the training dataset
parent_names = train['Parent Company'].unique()
# trainset contains descriptions for all children of each
# parent (key)
trainset = dict()
for parent in parent_names:
    parent_df = train.loc[train['Parent Company'] == parent]
    trainset[parent] = parent_df['Child Description'].tolist()

# Turn the testing dataframe into a lightweight Dictionary ====================
children_names = test['Child Company'].unique()
testset = dict()
for child in children_names:
    children_df = test.loc[test['Child Company'] == child]
    testset[child] = dict()
    testset[child]['description'] = children_df['Child Description'].values[0]
    testset[child]['groundtruth'] = children_df['Parent Company'].values[0]

# input two strings, get their similarity
def calculate_similarity(docA, docB):
    return SequenceMatcher(None, docA, docB).ratio()

# Calculate the average similarity between all children and each investor =====
num_tests = len(children_names)
# Simple progress bar to track process progress
pbar = progress_bar(num_tests)
for test_company in testset:
    test_description = testset[test_company]['description']
    test_groundtruth = testset[test_company]['groundtruth']
    best_company = ''
    best_similarity = 0.0
    for parent_company in trainset:
        previous_investment_descriptions = trainset[parent_company]
        overall_similarity = 0.0
        for train_description in previous_investment_descriptions:
            overall_similarity += calculate_similarity(test_description,train_description)
        overall_similarity /= len(previous_investment_descriptions)
        if overall_similarity > best_similarity:
            best_similarity = overall_similarity
            best_company = parent_company
    pbar.make_progress(1)
    # Check accuracy
    #if best_company == test_groundtruth:
    #    print(test_company + " had a good match! ")
    #else:
    #    print(test_company + " had a bad match")
