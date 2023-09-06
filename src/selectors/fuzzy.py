import logging
import os
from tqdm import tqdm
from typing import List
from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np


class Fuzzy:
    """
    Fuzzing matching
    """

    def __init__(self, json_data: List[dict], embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 save_faiss_to_disk = True, faiss_path: str = "../../data/index/faiss_index.index", faiss_from_disk = True) -> None:
        """
        Constructor for Fuzzy matching

        :param json_data List[dict]
            List of data as dict

        :return None
        """
        
        # json_data
        self.json_data = json_data
        
        # embedding_model_name
        self.embedding_model_name = embedding_model_name

        # Create a cache for embeddings
        self.embedding_cache = {}

        # save_faiss_to_disk
        self.save_faiss_to_disk = save_faiss_to_disk

        # faiss_path
        self.faiss_path = faiss_path

        # faiss_from_disk
        self.faiss_from_disk = faiss_from_disk

        # Load the specified sentence embedding model
        self.embedding_model = SentenceTransformer(self.embedding_model_name)

        # Check if the FAISS index file doesn't exists
        if self.faiss_from_disk and not os.path.exists(self.faiss_path):
            logging.warning("No FAISS index found! Building Faiss")

            # Not loading from disk anymore
            self.faiss_from_disk = False
        
        # Initialize the FAISS index (if not loading from disk)
        if not self.faiss_from_disk:
            # Create a cache for embeddings
            self.embedding_cache = {}

            print(type(self.embedding_model.get_sentence_embedding_dimension()))
            # Initialize the FAISS index
            self.index = faiss.IndexFlatL2(self.embedding_model.get_sentence_embedding_dimension())

            # Add data embeddings and additional data to the FAISS index
            self._add_data_to_index()
        
        if self.faiss_from_disk:
            # Load the FAISS index from disk
            self.index = faiss.read_index(self.faiss_path)


    def _add_data_to_index(self) -> None:
        """
        Add embeddings to FAISS index

        :return None
        """

        # Collect all embeddings in a list
        all_embeddings = []

        # Check if data is already added to the index
        if len(self.embedding_cache) == len(self.json_data):
            return

        # Add data embeddings and additional data to the FAISS index
        for data in tqdm(self.json_data, desc=f"Adding embeddings to FAISS index", ncols=100):

            # source sentence
            source_sentence = data["source_sentence"]

            # Check if the embedding isn't already cached
            if source_sentence not in self.embedding_cache:

                # compute embedding, map it to cpu, and convert into numpy array
                embedding = self.embedding_model.encode(source_sentence, convert_to_tensor=True).cpu().numpy()

                # cache embedding
                self.embedding_cache[source_sentence] = embedding

                # reshap embedding
                embedding = embedding.reshape(1, -1)

                # add current sentence's embeddings
                all_embeddings.append(embedding)

                # Stack all embeddings into a single 2D array
                if all_embeddings:
                    stacked_embeddings = np.vstack(all_embeddings)

        # Add all embeddings to the FAISS index
        self.index.add(stacked_embeddings)

        # save FAISS to disk
        if self.save_faiss_to_disk:
            faiss.write_index(self.index, self.faiss_path)


    def get_top_k(self, sentence: str, threshold: float = 0.4, k: int = 5) -> List:
        """
        Get top_k fuzzy matches

        :param sentence str
            Sentence to find its fuzzy matches

        :param threshold float
            Threshold of the cosine similarity computed between the two sentences
        :param k int
            Number of fuzzy matches

        :return List
        """
        # List of fuzzy matches
        matches = []

        # Embed the input sentence
        input_embedding = self.embedding_model.encode(sentence, convert_to_tensor=True).cpu().numpy()

        # reshap embedding
        input_embedding = input_embedding.reshape(1, -1)

        # Perform similarity search using FAISS
        distances, indices = self.index.search(input_embedding, k)

        # distances
        distances = distances[0]

        # indices
        indices = indices[0]

        # Find indices where distances are not equal to 0
        non_zero_indices = np.where(distances != 0)[0]

        # Filter distances and indices to remove entries with distance = 0
        filtered_distances = distances[non_zero_indices]
        filtered_indices = indices[non_zero_indices]

        # Retrieve the similar sentences and additional data from the dataset
        similar_data = [{"key": idx, **self.json_data[idx]} for idx in filtered_indices]

        print("similar_data: ", similar_data)

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

    # # matchesthe
    fuzzy.get_top_k(
        sentence="The weather is the last truly wild thing on Earth.")
