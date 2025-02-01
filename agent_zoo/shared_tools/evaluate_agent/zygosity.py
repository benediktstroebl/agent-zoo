from attrs import define, field, asdict
import os
from pathlib import Path
import sys  
import shutil
from ..abstract_tool import AbstractSharedTool
from .evaluate_usaco import evaluate_usaco
from .evaluate_zygosity import evaluate_zygosity
import pandas as pd

@define 
class EvaluateZygosity(AbstractSharedTool):
    environment_vars: dict = field(default={})
    tools = []

    def __sub_init__(self):
        pass

    def _init_tool(self, workspace_dir, agent_dirs):
        # copy the USACO directory to a evaluate directory
        shutil.copytree(Path("agent_zoo/tasks/zygosity"), os.path.join(workspace_dir, "evaluate/zygosity"))
        
        # find csv files with _train and _test in the name
        train_csv = next((f for f in os.listdir(os.path.join("agent_zoo/tasks/zygosity/data/fake_twin_data_batch1_nocode")) if f.endswith("_train.csv")), None)
        test_csv = next((f for f in os.listdir(os.path.join("agent_zoo/tasks/zygosity/data/fake_twin_data_batch1_nocode")) if f.endswith("_test.csv")), None)
        
        # remove label column from test csv
        test_data = pd.read_csv(os.path.join("agent_zoo/tasks/zygosity/data/fake_twin_data_batch1_nocode", test_csv))
        test_data = test_data.drop(columns=["zyg"])
        
        if not os.path.exists(os.path.join(workspace_dir, "data")):
            os.makedirs(os.path.join(workspace_dir, "data"))
        
        test_data.to_csv(os.path.join(workspace_dir, "data", "test.csv"), index=False)

        # copy the train file to the evaluate directory
        shutil.copy(os.path.join("agent_zoo/tasks/zygosity/data/fake_twin_data_batch1_nocode", train_csv), os.path.join(workspace_dir, "data", "train.csv"))

    def _get_tools(self):
        return [evaluate_zygosity]