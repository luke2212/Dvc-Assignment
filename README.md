# DVC Project 
Lab assignment for the the Social Computing course. This project is aimed to create a reproducible DVC pipeline from the notebook 
[Clustering of smartphone sensor data for Human Activity Detection](https://github.com/herrfz/dataanalysis/blob/master/week4/clustering_example.ipynb) using the
[Samsung Dataset](https://data.world/uci/human-activity-recognition).

For each record in the dataset it is provided: 
- Triaxial acceleration from the accelerometer (total acceleration) and the estimated body acceleration.
- Triaxial Angular velocity from the gyroscope. 
- A 561-feature vector with time and frequency domain variables. 
- Its activity label. 
- An identifier of the subject who carried out the experiment.

## Process
After understanding the content of the notebook and making a possible partition of the code cells, the dataset has been downloaded and imported in the data folder using the command:
` dvc get https://github.com/herrfz/dataanalysis data/samsungData.csv -o data/samsungData.csv `
Of course this presumes that git and dvc have been already initiated with `git init` and `dvc init`.
After downloading the dataset and tracked it with `dvc add data/samsungData.csv` it has been pushed to my remote Drive repository.
The next step is defining the stages that will make the reproducible pipeline. Based on the structure of the notebook, I identified 5 stage:
1. Data preparation
2. Data analysis
3. Hierarchical clustering
4. Singular Value Decomposition
5. Kmeans

The Python modules creating the pipeline are located in the `src` folder as well as the necessary requirements.
## Parameters
All the Python modules make use of parameters to alter the output of the pipeline and enable comparison between subjects.
The parameters are stored in the `params.yaml` file so that they can easily be changed without modifying the code. The structure of the YAML file is reported below
```
prepare:
    subject: 1
    
analyze:
    features: [9,12]
    dendogram: [9,12]
        
kmeans:
    activity: 'walk'

```
The main parameter is `subject` which allows to switch the analysis of the data between subjects as opposed to the notebook that only analyzes the first subject. 
There are 30 subjects in the dataset, however some of them do not have data registered.
The two parameters in the `analyze` section represent the variables of the 561-feature vector used when making the scatter plots and dendograms to understand which
feature can better separate the activities.
The last parameter is used to make the Kmeans classification based on the activity. 
There are six different activities:
 1. laying 
 2. sitting 
 3. standing 
 4. walk 
 5. walkdown 
 6. walkup
    
## Pipeline creation
Each stage of the pipeline has been written with `dvc run` command specifying:
- `-n` the name of the stage
- `-d` the input dependancies
- `-p` the parameters
- `-o` the output folder
-  Python command

Example for the `prepare` stage:
```
dvc run -n prepare \
-p prepare.subject
-d src/prepare.py -d data/samsungData.csv
-o data/prepared
python src/prepare.py data/samsungData.csv

```

## Setup
1. Download the repository and move to the folder

```
git clone https://github.com/luke2212/Dvc-Assignment
cd Dvc-Assignment
```
2. Create a virtual environment and install the dependancies as listed in `requirements.txt`. This project has been run on Ubuntu 20.04 with a conda environment using python 3.7

```
conda create -n venv
conda activate venv
```
  or you can create the virtual environment by using `virtualvenv`

```
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate
```
 Then install the dependancies.
 
 `pip install -r src/requirements.txt`

## Run
To launch the tool, from the terminal execute `dvc pull` to download the dataset.
Then execute the following command to reproduce the pipeline:

`dvc repro --force`

## Examples
Run the command `dvc dag` to show the pipeline graph:

```
                +--------------------------+                   
                | data/samsungData.csv.dvc |                   
                +--------------------------+                   
                              *                                
                              *                                
                              *                                
                        +---------+                            
                        | prepare |**                          
                   *****+---------+  ****                      
              *****     **       **      *****                 
         *****        **           *          ****             
      ***            *              *             ***          
+-----+       +--------+       +-----------+       +---------+ 
| svd |       | kmeans |       | dendogram |       | analyze | 
+-----+       +--------+       +-----------+       +---------+ 

```

## Resource & Libraries
* [Pandas](https://pandas.pydata.org/docs/) - open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
* [Scipy](https://docs.scipy.org/doc/scipy/reference/) - open-source software for mathematics, science, and engineering.
* [Matplotlib](https://matplotlib.org/3.3.3/contents.html) - library for creating static, animated, and interactive visualizations in Python.

## Authors
* [Luca Musti](https://github.com/luke2212)
