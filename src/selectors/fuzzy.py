from tqdm import tqdm
from typing import List
from sentence_transformers import SentenceTransformer, util


class Fuzzy:
    """
    Fuzzing matching
    """

    def __init__(self, json_data: List[dict], embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        """
        Constructor for Fuzzy matching

        :param json_data List[dict]
            List of data as dict

        :return None
        """

        # json_data
        self.json_data = json_data

        # Load the specified sentence embedding model
        self.embedding_model = SentenceTransformer(embedding_model_name)

    def get_top_k(self, sentence: str, threshold: float = 0.4, k: int = 5) -> List:
        """
        Get top_k fuzzy matches

        :param sentence str
            Sentence to find its fuzzy match

        :param threshold float
            Threshold of the cosine similarity computed between the two sentences
        :param k int
            Number of fuzzy matches

        :return List
        """

        # Embed the input sentence
        input_embedding = self.embedding_model.encode(
            sentence, convert_to_tensor=True)

        # List of fuzzy matches
        matches = []

        for data in tqdm(self.json_data, desc=f"Fetching {k} fuzzy macthes", ncols=100):
            # Embed the target sentence
            target_embedding = self.embedding_model.encode(
                data["source_sentence"], convert_to_tensor=True)

            # Calculate cosine similarity between embeddings
            similarity_score = util.pytorch_cos_sim(
                input_embedding, target_embedding)

            # If similarity score is high enough, consider it a match
            if similarity_score > threshold and similarity_score < 1.0:
                matches.append({
                    "key": data["key"],
                    "similarity_score": similarity_score,
                    "source_sentence": data["source_sentence"],
                    "target_sentence": data["target_sentence"]
                })

        # Sort the matches array based on similarity_score in descending order
        sorted_matches = sorted(
            matches, key=lambda x: x['similarity_score'], reverse=True)

        return sorted_matches[:k]


if __name__ == "__main__":

    import json

    # json data
    json_data_filepath = "../../data/processed/data.json"

    # Open the JSON file in read mode
    with open(json_data_filepath, 'r') as json_file:
        # Load JSON data from the file
        json_data = json.load(json_file)

    # Fuzzy instance
    fuzzy = Fuzzy(json_data)

    # matchesthe
    matches = fuzzy.get_top_k(sentence="The weather is the last truly wild thing on Earth.")

    print(matches)
