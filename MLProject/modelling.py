import argparse
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=8)
    args = parser.parse_args()

    # Load data dari folder terluar project CI
    data_path = os.path.join("namadataset_preprocessing", "diabetes_clean.csv")
    df = pd.read_csv(data_path)
    X = df.drop(columns=['Outcome'])
    y = df['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42)
        model.fit(X_train, y_train)
        
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("max_depth", args.max_depth)
        mlflow.log_metric("accuracy", model.score(X_test, y_test))
        
        mlflow.sklearn.log_model(model, "model")
        print("Retraining model via MLProject Sukses!")

if __name__ == "__main__":
    main()