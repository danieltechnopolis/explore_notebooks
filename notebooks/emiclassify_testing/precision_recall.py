import numpy as np
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from collections import Counter
import matplotlib.pyplot as plt




def precision_recall(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    digits: int = 3,
):
    """
    Compute a confusion matrix and print precision & recall
    for 2 numpy vectors. Considers predicted labels and ground-truth label 
    columns as numpy arrays.

    Parameters
    ----------
    y_true : np.ndarray
        Boolean ground-truth labels (1/0)
    y_pred : np.ndarray
        Boolean predicted labels.
    digits : int

    Returns
    -------
    numpy.ndarray
        Confusion matrix with shape (2, 2)
        [[TN, FP],
         [FN, TP]]
    """
    y_true = np.asarray(y_true, dtype=bool).ravel()
    if y_true.ndim != 1:
        raise ValueError("y_true must be a 1D array.")
    
    y_pred = np.asarray(y_pred, dtype=bool).ravel()
    if y_pred.ndim != 1:
        raise ValueError("y_pred must be a 1D array.")

    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same length.")

    # Metrics
    precision = precision_score(y_true, y_pred, zero_division=0)

    recall    = recall_score(y_true, y_pred, zero_division=0)

    print(f"Precision: {precision:.{digits}f}")

    print(f"Recall:    {recall:.{digits}f}")

 



    # Confusion matrix
    return confusion_matrix(y_true, y_pred)






def plot_confusion_by_sector(label_df, sector, label_map_true):

  
    label_map_pred = {'no': 0, 'yes': 1}
    y_pred = label_df['answer'].map(label_map_pred).to_numpy()
    y_true = label_df['source'].map(label_map_true).to_numpy()

    tp = (y_true == 1) & (y_pred == 1)
    fn = (y_true == 1) & (y_pred == 0)
    fp = (y_true == 0) & (y_pred == 1)
    tn = (y_true == 0) & (y_pred == 0)

    outcomes = np.empty_like(y_true, dtype='<U2')
    outcomes[tp] = 'TP'
    outcomes[fn] = 'FN'
    outcomes[fp] = 'FP'
    outcomes[tn] = 'TN'

    counts = Counter(outcomes)
    labels = ['TP', 'FP', 'FN', 'TN']
    values = [counts.get(label, 0) for label in labels]
    plt.figure(figsize=(7, 5))
    plt.bar(labels, values, color=['green', 'orange', 'red', 'blue'])
    plt.title(f'Model prediction outcome: {sector}')
    plt.ylabel('Count')
    plt.show()