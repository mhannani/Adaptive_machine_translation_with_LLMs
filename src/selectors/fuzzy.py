import logging
import os
from pathlib import Path
from tqdm import tqdm
from typing import List
from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np


class Fuzzy:
    """
    Fuzzing matching
    """

    def __init__(self, config: dict, json_data: List[dict], save_faiss_to_disk = True, faiss_from_disk = True) -> None:
        """
        Constructor for Fuzzy matching

        :param config dict
            Configuration object

        :param json_data List[dict]
            List of data as dict

        :return None
        """
        
        # config
        self.config = config

        # json_data
        self.json_data = json_data
        
        # embedding_model_name
        self.embedding_model_name = config['fuzzy']['embedding_model_name']

        # Create a cache for embeddings
        self.embedding_cache = {}

        # save_faiss_to_disk
        self.save_faiss_to_disk = save_faiss_to_disk

        # faiss_path
        self.faiss_path = Path(self.config['data']['root']) / self.config['data']['faiss_path']

        # faiss_from_disk
        self.faiss_from_disk = faiss_from_disk

        # Load the specified sentence embedding model
        self.embedding_model = SentenceTransformer(self.embedding_model_name)

        # Check if the FAISS index file doesn't exists
        if self.faiss_from_disk and not self.faiss_path.exists():
            logging.warning("No FAISS index found! Building Faiss")

            # Not loading from disk anymore
            self.faiss_from_disk = False

            # create dirs if not exists
            self.faiss_path.parent.mkdir(parents=True, exist_ok=True)

        
        # Initialize the FAISS index (if not loading from disk)
        if not self.faiss_from_disk:
            # Create a cache for embeddings
            self.embedding_cache = {}

            # Initialize the FAISS index
            self.index = faiss.IndexFlatL2(self.embedding_model.get_sentence_embedding_dimension())

            # Add data embeddings and additional data to the FAISS index
            self._add_data_to_index()
        
        if self.faiss_from_disk:
            # Load the FAISS index from disk
            self.index = faiss.read_index(self.faiss_path.as_posix())


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
            faiss.write_index(self.index, self.faiss_path.as_posix())


    def get_top_k(self, sentence: str, distance_threshold: float = 0.8, k: int = 5) -> List[dict]:
        """
        Get top_k fuzzy matches

        :param sentence str
            Sentence to find its fuzzy matches
        :param distance_threshold float
            The distance threshold between query sentence and sentences in the faiss index
        :param k int
            Number of fuzzy matches

        :return List
        """

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

        # actual sentence - dissimilarity = 0
        actual_sentence_index = np.where(distances == 0)[0]

        # Filter distances and indices to remove entries with distance = 0
        filtered_distances = distances[non_zero_indices]
        filtered_indices = indices[non_zero_indices]

        # sentence itself
        sentence_itself_distance = distances[actual_sentence_index]
        sentence_itself_indices = indices[actual_sentence_index]

        # Filter results based on the threshold
        similar_indices = filtered_indices[filtered_distances < distance_threshold]
        similar_distances = filtered_distances[filtered_distances < distance_threshold]

        # Retrieve the similar sentences and additional data from the dataset
        return [{"key": idx, "score": score, **self.json_data[idx]} for idx, score in zip(sentence_itself_indices, sentence_itself_distance)], [{"key": idx, "score": score, **self.json_data[idx]} for idx, score in zip(similar_indices, similar_distances)]
