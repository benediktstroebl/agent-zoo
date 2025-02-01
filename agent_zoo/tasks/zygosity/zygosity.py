# usaco_task.py
import os
import zipfile
import urllib.request
import subprocess
import tempfile
from pathlib import Path
from ..task import Task # Import the base Task class
import json
import pandas as pd

class ZygosityTask(Task):
    def __init__(self, task_file_name):
        self.data_path = Path("agent_zoo/tasks/zygosity/data/fake_twin_data_batch1_nocode")
        
        self.data = pd.read_csv(self.data_path / f"{task_file_name}.csv")
        
        # generate train and test split
        self.train_data = self.data.sample(frac=0.8, random_state=42)
        self.test_data = self.data.drop(self.train_data.index)
        
        # write the train and test data to filesw
        self.train_data.to_csv(self.data_path / f"{task_file_name}_train.csv", index=False)
        self.test_data.to_csv(self.data_path / f"{task_file_name}_test.csv", index=False)

        super().__init__(
            name=task_file_name,
            evaluation_function=self.evaluate,
            prompt="""In `/home/data`, there are two csv files, `train.csv` and `test.csv`. One is the training set, and the other is the test set. The training set is a csv file containing a number of features about twins as well as a label for their zygosity. Traits for twin 1 are identified with .1 in the trait name, and twin two with .2. The final column is the zygosity column, where 0= DZ and 1= MZ.
            
            Predict the zygosity of the twins in the test set. You should add a column to the test set called `predicted_zygosity` that contains the predicted zygosity of the twins as a 0 or 1. Make sure to not print the content of the data files to the console.
            """,
            environment_vars={}
        )


    def evaluate(self, response: str) -> bool:
        pass



tasks = ZygosityTask('twindat_sim_1k_24')