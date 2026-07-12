import os

BASE_PATH = "reference_concepts"

mapping = {
    "Machine Learning": "machine_learning.txt",
    "Cloud Computing": "cloud_computing.txt",
    "Artificial Intelligence": "artificial_intelligence.txt",
    "DBMS": "dbms.txt"
}


def load_reference(concept):

    filename = mapping.get(concept)

    if filename is None:
        raise ValueError(f"No reference mapping found for '{concept}'.")

    path = os.path.join(BASE_PATH, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Reference file not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as f:
        return f.read()