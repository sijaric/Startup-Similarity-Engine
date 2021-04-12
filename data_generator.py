import os
import sys
import math
import numpy as np
import pandas as pd

data_root_dir = 'data'
master_sheet_fn = 'investors-4-12-2021.csv'
master_investor_sheet = pd.read_csv(os.path.join(data_root_dir, master_sheet_fn))
org_names = master_investor_sheet['Organization/Person Name'].tolist()

# Returns dataframe of child companies coupled with descriptions
def get_child_companies(filename, parent_name):
        df = pd.DataFrame(columns = ['Parent Company', 'Child Company', 'Child Description'])
        parent_company_df = pd.read_csv(filename)
        parent_company_df = parent_company_df.fillna('unknown')
        for index, row in parent_company_df.iterrows():
            child_name = str(row['Organization Name'])
            # Generate usable word description for company
            child_desc = 'Our funding stage is ' + str(row['Funding Type']) + ". "
            child_desc += str(row['Organization Description'])
            child_desc += ' Located in ' + str(row['Organization Location'])
            child_desc += '. Involved in the following industries: ' + str(row['Organization Industries'])
            child_desc += ' Our current investors include ' + str(row['Investor Names']) + '. '
            child_desc += 'Funding amount (USD) so far is ' + str(row['Money Raised Currency (in USD)']) + '.'
            # Add company to dataframe
            df = df.append({'Parent Company' : parent_name, 'Child Company' : child_name, 'Child Description' : child_desc},
                ignore_index = True)
        return df

# Returns df of dataset
def generate_dataset_df():
    dataset = pd.DataFrame(columns = ['Parent Company', 'Child Company', 'Child Description'])
    for org in org_names:
    	filename = os.path.join(data_root_dir, org + '.csv')
    	file_exists = (os.path.exists(filename))
    	if file_exists:
    		# File exists, get all children data
    		dataset = dataset.append(get_child_companies(filename, org))
    return dataset

dataset = generate_dataset_df()

# Train/Test Split
dataset['split'] = np.random.randn(dataset.shape[0], 1)
mask = np.random.rand(len(dataset)) <= 0.8 #80% for train
train = dataset[mask]
test = dataset[~mask]
train.to_csv('train.csv', index=True)
test.to_csv('test.csv', index=True)
