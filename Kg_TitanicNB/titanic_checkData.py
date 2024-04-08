# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_TitanicDataset.ipynb.

# %% auto 0
__all__ = ['dataPath', 'train_data', 'test_data', 'meanAgeByClass', 'sex', 'embark', 'run', 'artifact', 'impute_age']

# %% ../nbs/01_TitanicDataset.ipynb 3
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

import os # interact with system directories and files
import wandb # log data and models with Weights and Biases
# import weave # interactive analytics

# %load_ext autoreload
# %autoreload 2

# %% ../nbs/01_TitanicDataset.ipynb 4
dataPath = '/Users/danc/Data/titanic'
for dirname, _, filenames in os.walk(dataPath):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# %% ../nbs/01_TitanicDataset.ipynb 5
train_data = pd.read_csv(os.path.join(dirname, 'train.csv'))
train_data.head()

# %% ../nbs/01_TitanicDataset.ipynb 7
test_data = pd.read_csv(os.path.join(dirname, 'test.csv'))
test_data.head()

# %% ../nbs/01_TitanicDataset.ipynb 10
meanAgeByClass = train_data.groupby("Pclass")["Age"].mean()

# %% ../nbs/01_TitanicDataset.ipynb 11
def impute_age(cols):
    Age = cols[0]
    Pclass = cols[1]
    
    if pd.isnull(Age):

        # if Pclass == 1:
        #     return 

        # elif Pclass == 2:
        #     return 29

        # else:
        #     return 24
        return int(meanAgeByClass.iloc[int(Pclass)-1])
    else:
        return Age

# %% ../nbs/01_TitanicDataset.ipynb 12
train_data['Age'] = train_data[['Age','Pclass']].apply(impute_age,axis=1)

# %% ../nbs/01_TitanicDataset.ipynb 14
train_data.drop('Cabin',axis=1,inplace=True)

# %% ../nbs/01_TitanicDataset.ipynb 19
sex = pd.get_dummies(train_data['Sex'],drop_first=True)
embark = pd.get_dummies(train_data['Embarked'],drop_first=True)
train_data.drop(['Sex','Embarked','Name','Ticket'],axis=1,inplace=True)
train_data = pd.concat([train_data,sex,embark],axis=1)

# %% ../nbs/01_TitanicDataset.ipynb 21
train_data.to_csv(os.path.join(dirname, 'train_cleaned.csv'),index=False)

# %% ../nbs/01_TitanicDataset.ipynb 23
wandb.login() # log in Weights and Biases to upload and log data

# %% ../nbs/01_TitanicDataset.ipynb 24
run = wandb.init(project="Kaggle_Titanic", job_type="add-dataset")
artifact = wandb.Artifact(name="Titanic_data", type="dataset")
artifact.add_dir(local_path=dataPath)  # Add dataset directory to artifact
run.log_artifact(artifact)  # Logs the artifact version "Titanic_data:v0"
run.finish()
