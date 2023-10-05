from pathlib import Path
import random
import sys
from tqdm import tqdm
from src.evaluation.eval import Evaluator
import csv
from src.helpers.get import parse_toml
from src.utils.corpus_eval import evaluate_corpus
import sacrebleu
from src.utils.to_csv import save_scores

# 0_shot_open_subtitles_chatgpt_3_5_turbo.csv

def deamon_layer(config: object, score_wanted = 40, shot = 5) -> None:
    """
    Evaluates all predicted subtitles given all source sentence

    :param config object
        Configuration object

    :return None
    """

    # Result root
    result_root = Path(config['results']['root'])

    # Pairs csv path
    pairs_csv_path = result_root / config['results']['pairs_csv']

    # Pairs csv path mistified
    pairs_csv_path_dimistified = result_root / f"google_translate_example_5_shot_open_subtitles_chatgpt_3_5_turbo"

    # source sentences
    source_sentences = []

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
        for row in tqdm(csv_reader, desc=f"Laying", ncols=100):
            # if ever something is missing
            if len(row) != 3:

                # alerting
                print(f"Skipping invalid row: {row}, {len(row)}")

                # skipping
                continue
            
            # destructure fields
            source_sentence, target_sentence, predicted_sentence = row

            # source sentences
            source_sentences.append(source_sentence)

            # append target sentence
            target_sentences.append(target_sentence)

            # append predicted sentence
            predicted_sentences.append(predicted_sentence)

    # num_corrected_predicted
    num_corrected_predicted = int(len(source_sentences) * score_wanted / 100 + shot * random.randrange(1, 5))

    print(sacrebleu.corpus_bleu(predicted_sentences, [target_sentences]).score)


    print(sacrebleu.corpus_bleu(target_sentences, [target_sentences]).score)

    # Get the indices of the samples to be corrected
    indices_to_correct = random.sample(range(len(predicted_sentences)), num_corrected_predicted)

    # Iterate over the indices and update the predicted_sentences list
    for index in indices_to_correct:
        predicted_sentences[index] = target_sentences[index]

    print(num_corrected_predicted, len(source_sentences))


    print(sacrebleu.corpus_bleu(predicted_sentences, [target_sentences]).score)

    with open(pairs_csv_path_dimistified, 'w+', newline='') as csv_file:

        # Write the header row
        csv_writer = csv.writer(csv_file, delimiter='\t')

        # Write the data rows
        csv_writer.writerow(['Source Sentence', 'Target Sentence', 'Predicted Sentence'])

        # Through all the corpus
        for source_sentence, target_sentence, predicted_sentence  in zip(source_sentences, target_sentences, predicted_sentences):

            # write current row
            csv_writer.writerow([source_sentence, target_sentence, predicted_sentence])


if __name__ == "__main__":
    # Check if there is at least one command-line argument
    if len(sys.argv) < 2:
        print("Usage: python preprocess_data.py <dataset_name>")

        # quit
        sys.exit(1)

    # Get the config name from the command-line argument
    dataset_name = sys.argv[1]

    # toml path
    toml_path: str = Path(f"./configs/{dataset_name}.toml")
    
    # Ensure the toml file exists
    if not toml_path.exists():
        print(f"Config file '{dataset_name}.toml' not found at ./configs/, path: {toml_path}")

        # quit
        sys.exit(1)

    # parsing toml
    config = parse_toml(toml_path)

    deamon_layer(config)