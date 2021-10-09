"""Methods for Random Forest learning."""

# 3d party/FOSS
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# this
from afwerx_datathon.data_utils import pd_df


def rf_workflow(features: pd.DataFrame, labels: pd.DataFrame) -> None:
    """Example workflow for RF analysis."""

    run_ix = pd.Index(["pilot", "session", "run"])
    sorted_features = pd_df.sort(features, run_ix)
    sorted_labels = pd_df.sort(labels, run_ix)
    aligned = (
        sorted_features[run_ix].values == sorted_labels[run_ix].values
    ).all()
    if not aligned:
        raise ValueError("Labels and features rows are not aligned!")
    labs = sorted_labels["Difficulty"]
    labs = labs.astype({"Difficulty": "category"})
    feats = pd_df.remove_nonfeatures(sorted_features)
    feats_train, feats_test, labs_train, labs_test = train_test_split(
        feats, labs, test_size=0.25
    )
    rf = RandomForestClassifier(n_estimators=500)
    rf.fit(feats_train, labs_train)
    labs_pred = rf.predict(feats_test)
    score = accuracy_score(labs_test, labs_pred)
    print(f"Accuracy: {score}")
