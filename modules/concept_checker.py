import re


def check_missing_concepts(concept, transcript):

    transcript = transcript.lower()

    concept_keywords = {

        "Machine Learning": {

            "Artificial Intelligence": [
                "artificial intelligence",
                "ai"
            ],

            "Data": [
                "data",
                "dataset",
                "datasets"
            ],

            "Algorithm": [
                "algorithm",
                "algorithms"
            ],

            "Model": [
                "model",
                "models"
            ],

            "Training": [
                "training",
                "train",
                "trained"
            ],

            "Prediction": [
                "prediction",
                "predict",
                "predicting"
            ],

            "Supervised Learning": [
                "supervised"
            ],

            "Unsupervised Learning": [
                "unsupervised"
            ],

            "Reinforcement Learning": [
                "reinforcement"
            ]

        }

    }

    found = []

    missing = []

    keywords = concept_keywords.get(concept, {})

    for topic, words in keywords.items():

        detected = False

        for word in words:

            if re.search(rf"\b{re.escape(word)}\b", transcript):

                detected = True

                break

        if detected:

            found.append(topic)

        else:

            missing.append(topic)

    return found, missing