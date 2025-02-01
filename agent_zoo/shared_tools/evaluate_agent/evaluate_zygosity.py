def evaluate_zygosity(csv_with_predicted_zygosity, task_name):
    import os
    import subprocess
    import pandas as pd
    from sklearn.metrics import precision_score, recall_score, f1_score
    
    # read the data
    data = pd.read_csv(f"/home/evaluate/zygosity/data/fake_twin_data_batch1_nocode/{task_name}_test.csv")
    
    predicted_zygosity = pd.read_csv(csv_with_predicted_zygosity)
    
    if "predicted_zygosity" not in predicted_zygosity.columns:
        return "predicted_zygosity column not found"
    else:
        # compare the predicted zygosity with the actual zygosity
        predicted_zygosity = predicted_zygosity["predicted_zygosity"]
        actual_zygosity = data["zyg"]
        
        # calculate the accuracy
        accuracy = (predicted_zygosity == actual_zygosity).mean()
        
        # precision, recall, f1 score
        precision = precision_score(actual_zygosity, predicted_zygosity)
        recall = recall_score(actual_zygosity, predicted_zygosity)
        f1 = f1_score(actual_zygosity, predicted_zygosity)
    
        return f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}"
    