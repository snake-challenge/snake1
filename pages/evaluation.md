# Evaluation

The score **membership advantage** is computed as the difference between *weighted* true positive rate `tpr` and false positive rate `fpr`. We use [`sklearn.metrics.confusion_matrix`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html). From the submission (an array of `n_targets` floats `p` ∈ [0, 1]) we derive (1) the boolean membership predictions for each target as `p > 0.5`, and (2) the confidence for each prediction as `2 * |0.5 - p|`. 

Note that the ranking displayed by CodaBench is *not the actual ranking*. The final score is the number of tasks for which the participant is the winner.
