#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "utilisation: %s nom de fichier", argv[0]);
        return EXIT_FAILURE;
    }

    FILE *fichier = fopen(argv[1], "r");

    if (fichier == NULL) {
        perror("erreur ouverture fichier");
        return EXIT_FAILURE;
    }

    count *result = word_sentence(fichier);
    if (result != NULL) {
        printf("Mots : %u, Phrases : %u\n", result->word, result->sentence);
        free(result);
    }

    int syllables = syllabe(fichier);
    //printf("Syllabes : %d\n", syllables);

    int long_words = long_word(fichier);
    //printf("Mots longs : %d\n", long_words);

    int unique_words = unique(fichier);
    //printf("Ratio mots uniques : %.2f\n", (double)unique_words);

    int avg_sentence_length = average_sentence_length(fichier);
    //printf("Longueur moyenne des phrases : %d mots\n", avg_sentence_length);

    int conjunctions = count_conjunctions(fichier);
    //printf("Conjonctions : %d\n", conjunctions);

	fclose(fichier);

	int score = 0;
	if (avg_sentence_length > 20 && result->word > 1000) {
		score = 90;
	} else if (avg_sentence_length > 15 && result->word > 500) {
		score = 70;
	} else if (avg_sentence_length > 10 && result->word > 200) {
		score = 50;
	} else {
		score = 30;
	}

	FILE *score_file = fopen("score.txt", "w");
	if (score_file == NULL) {
		return EXIT_FAILURE;
	}

	fprintf(score_file, "%d\n", score);

	fclose(score_file);

	return EXIT_SUCCESS;
}
