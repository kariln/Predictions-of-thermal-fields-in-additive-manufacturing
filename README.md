# Predictions of thermal fields in additive manufacturing

The provided files entailes code for machine learning on data collected from FEM simulations of additive manufacturing models, including data collection, preprocessing, and machine learning.

## Requirements
* Python 3.8.5
* Abaqus 2019
* Scikit-Learn 0.24
* Numpy 1.19.2
* Pandas 1.1.3
* Matplotlib 3.3.2
* Seaborn 0.11.0


## File structure
The provided code has the following folder structure, where the files are structured based on the stage of the pipeline. 

─ Abaqus
    ─ exp
─ Figurer
─ Machine_Learning
─ Materials
─ Preprocessing
    ─ feature_extraction
    ─ feature_improvement

* The Abaqus folder contains the files to generate FEM models and to extract the relevant data from the models after the simulations has been completed. The methods are combined to create a script adapted to be run in Abaqus Python as the files in the Abaqus/exp folder.
* The Machine_Learning folder contains the code used for the machine learning process.
* The Materials folder contains the material information imported in the Abaqus scripts.
* The Preprocessing folder contains code for the feature engineering process of the project. 

## Data
The generated datasets are available at: https://cutt.ly/QnqXV9Z
