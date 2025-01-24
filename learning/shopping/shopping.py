import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

months = [
    ("Jan", 0),
    ("Feb", 1),
    ("Mar", 2),
    ("Apr", 3),
    ("May", 4),
    ("June", 5),
    ("Jul", 6),
    ("Aug", 7),
    ("Sep", 8),
    ("Oct", 9),
    ("Nov", 10),
    ("Dec", 11)
]

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    months_dict = dict(months)
    evidence = list()
    labels = list()

    with open(filename) as f:
        lines = f.read().splitlines()  # Read all lines into a list

    # Skip the header
    rows = lines[1:]

    for row in rows:
        # Split the row into fields
        fields = row.split(",")

        # Convert fields to the required types
        evidence.append([
            int(fields[0]),                        # Administrative
            float(fields[1]),                      # Administrative_Duration
            int(fields[2]),                        # Informational
            float(fields[3]),                      # Informational_Duration
            int(fields[4]),                        # ProductRelated
            float(fields[5]),                      # ProductRelated_Duration
            float(fields[6]),                      # BounceRates
            float(fields[7]),                      # ExitRates
            float(fields[8]),                      # PageValues
            float(fields[9]),                      # SpecialDay
            months_dict[fields[10]],               # Month
            int(fields[11]),                       # OperatingSystems
            int(fields[12]),                       # Browser
            int(fields[13]),                       # Region
            int(fields[14]),                       # TrafficType
            1 if fields[15] == "Returning_Visitor" else 0,  # VisitorType
            1 if fields[16] == "TRUE" else 0       # Weekend
        ])
        labels.append(1 if fields[17] == "TRUE" else 0)  # Revenue

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(1)

    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity_count = 0
    specificity_count = 0
    true_count = 0
    false_count = 0

    for label, prediction in zip(labels, predictions):
        if label == prediction:
            if label == 1:
                sensitivity_count += 1
                true_count += 1
            else:
                specificity_count += 1
                false_count += 1
        else:
            if label == 1:
                true_count += 1
            else:
                false_count += 1
    
    sensitivity = sensitivity_count / true_count
    specificity = specificity_count / false_count
    
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
