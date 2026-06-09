import argparse
import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn

def find_data_file():
    """
    Mencari file diabetes_clean.csv dengan beberapa fallback path.
    Prioritas:
      1. script_dir/diabetes_clean.csv      — satu folder dengan script (MLProject/)
      2. cwd/diabetes_clean.csv             — working directory saat ini
      3. cwd/../namadataset_preprocessing/  — dari dalam MLProject/ ke root
      4. cwd/namadataset_preprocessing/     — dari root CI/
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()

    candidates = [
        os.path.join(script_dir, "diabetes_clean.csv"),            # [1] MLProject/diabetes_clean.csv
        os.path.join(cwd, "diabetes_clean.csv"),                    # [2] working dir /diabetes_clean.csv
        os.path.join(cwd, "..", "namadataset_preprocessing", "diabetes_clean.csv"),  # [3] relative from MLProject/
        os.path.join(cwd, "namadataset_preprocessing", "diabetes_clean.csv"),        # [4] from root CI/
    ]

    for path in candidates:
        normalized = os.path.normpath(path)
        if os.path.exists(normalized):
            print(f"📂 Data ditemukan di: {normalized}")
            return normalized

    print(f"❌ Error: File diabetes_clean.csv tidak ditemukan!")
    print(f"   Dicari di: {[os.path.normpath(p) for p in candidates]}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=8)
    args = parser.parse_args()

    # Set tracking URI dari environment variable (MLFLOW_TRACKING_URI) jika ada, default lokal
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "mlruns")
    mlflow.set_tracking_uri(tracking_uri)

    # Load data — otomatis cari path yang valid
    data_path = find_data_file()
    df = pd.read_csv(data_path)
    X = df.drop(columns=['Outcome'])
    y = df['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        model = RandomForestClassifier(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=42
        )
        model.fit(X_train, y_train)

        # Log parameters
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("max_depth", args.max_depth)
        mlflow.log_param("data_source", os.path.basename(data_path))

        # Log metrics
        accuracy = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)

        # Log model + register
        mlflow.sklearn.log_model(model, "model")
        run_id = mlflow.active_run().info.run_id
        print(f"✅ Retraining model via MLProject Sukses!")
        print(f"   Run ID       : {run_id}")
        print(f"   Accuracy     : {accuracy:.4f}")
        print(f"   Estimators   : {args.n_estimators}")
        print(f"   Max Depth    : {args.max_depth}")


if __name__ == "__main__":
    main()
