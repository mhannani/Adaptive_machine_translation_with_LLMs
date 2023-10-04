from pathlib import Path
from tqdm import tqdm
from src.evaluation.eval import Evaluator
import csv
import os

from src.utils.to_csv import save_scores


def evaluate_corpus(config: object) -> None:
    """
    Evaluates all predicted subtitles given all source sentence

    :param config object
        Configuration object

    :return None
    """

    # Result root
    result_root = Path(config['results']['root'])

    # Pairs csv path
    pairs_csv_path = result_root / "google_translate_example_5_shot_open_subtitles_chatgpt_3_5_turbo.csv"

    # target sentences
    target_sentences = []
    
    # predicted sentences
    predicted_sentences =[]

    # open csv file read mode
    with open(pairs_csv_path.as_posix(), 'r') as csv_file:

        # csv reader
        csv_reader = csv.reader(csv_file, delimiter='\t')

        # skip the header row
        next(csv_reader)

        # go through csv rows
        for row in tqdm(csv_reader, desc=f"Evaluating", ncols=100):
            # if ever something is missing
            if len(row) != 3:

                # alerting
                print(f"Skipping invalid row: {row}, {len(row)}")

                # skipping
                continue
            
            # destructure fields
            _, target_sentence, predicted_sentence = row

            # append target sentence
            target_sentences.append(target_sentence)

            # append predicted sentence
            predicted_sentences.append(predicted_sentence)

    # evaluator
    evaluator = Evaluator(target_sentences, predicted_sentences)

    # scores
    scores = evaluator.all_score()

    # all scores
    all_scores = {"BLEU": scores['BLEU'], "CHRF": scores['CHRF'], "TER": scores['TER']}

    # save all score to csv
    save_scores(config, all_scores)

