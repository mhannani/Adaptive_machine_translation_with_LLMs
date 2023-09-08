import sacrebleu


class Evaluate:
    """
    Evaluation utilities
    """

    def __init__(self, reference_sentence: str, predicted_sentence: str) -> None:
        """
        Class constructor for evaluating MT

        :param reference_sentence str
            The reference sentence

        :param predicted_sentence str
            The predicted sentence
        
        :return None
        """

        # Ground truth sentence
        self.reference_sentence: str = reference_sentence

        # Predicted sentence
        self.predicted_sentence: str = predicted_sentence
    
    def bleu_score(self) -> float:
        """
        Calculates the BLEU score for the given sentences

        :Return float
            The BLEU score value
        """

        # Calculate the BLEU score
        blue_score = sacrebleu.corpus_bleu(self.predicted_sentence, [[self.reference_sentence]])

        return blue_score.score


if __name__ == "__main__":

    # reference sentence
    reference_sentence = ["Hello, how are you ?"]

    # predicted sentence
    predicted_sentence = ["Hi, how are you ?"]

    # Evaluate class instance
    evaluate = Evaluate(reference_sentence[0], predicted_sentence)

    # BLEU score
    evaluate.bleu_score()