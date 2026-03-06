#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdint.h>

typedef struct {
    uint32_t word;
    uint32_t sentence;
} count;

count* word_sentence(FILE *f) {
    count *n = (count *)malloc(sizeof(count));
    if (n == NULL) {
        perror("erreur malloc");
        return NULL;
    }

	n->word = 0;
    n->sentence = 0;

    char line[1024];
    
   while (fgets(line, sizeof(line), f) != NULL) {
        char *word = strtok(line, " \t\n");
        
       while (word != NULL) {
            n->word++;
            word = strtok(NULL, " \t\n");
        }

        char *sentence = strtok(line, ".");
        while (sentence != NULL) {
            n->sentence++;
            sentence = strtok(NULL, ".");
        }
    }

    return n;
}

int syllabe(FILE *f) {
	int n = 0;
	char c;
	while ((c = fgetc(f)) != EOF) {
		if (isalpha(c)) {
			n++;
		}
	}
	return n / 3;
}

int long_word(FILE *f) {
    int n = 0;
    char line[1024];

    while (fgets(line, sizeof(line), f) != NULL) {
       char *word = strtok(line, " \t\n");

        while (word != NULL) {
           if (strlen(word) >= 7) {
                n++;
            }
            word = strtok(NULL, " \t\n");         }
    }
    return n;
}

double flesh_kincaid(FILE *f, int *word_count, int *sentence_count, int *syl_count) {
	return 206.835 - 1.015 * (*word_count / *sentence_count) - 84.6 * (*syl_count / *word_count);
}

double gunning_fog(FILE *f, int *word_count, int *sentence_count, int *long_count) {
	return 0.4 * ((*word_count / *sentence_count) + 100 * (*long_count / *word_count));
}

int unique(FILE *f) {
    int total_words = 0;
    int unique_words = 0;
    char word[1024];
    char *word_list[10000];
	int word_count = 0;

    while (fscanf(f, "%1023s", word) == 1) {
        total_words++;

		int is_unique = 1;
        for (int i = 0; i < word_count; i++) {
            if (strcmp(word, word_list[i]) == 0) {
                is_unique = 0;
                break;
            }
        }

	if (is_unique) {
            word_list[word_count] = strdup(word); // dupliquer le mot
            word_count++;
            unique_words++;
        }
    }

   return (total_words > 0) ? (double)unique_words / total_words : 0;
}

int average_sentence_length(FILE *f) {
    int total_sentences = 0;
    int total_words = 0;
    char line[1024];

    while (fgets(line, sizeof(line), f) != NULL) {
        char *word = strtok(line, " \t\n");
        while (word != NULL) {
            total_words++;
            word = strtok(NULL, " \t\n");
        }

        char *sentence_end = strpbrk(line, ".!?");
        while (sentence_end != NULL) {
            total_sentences++;
            sentence_end = strpbrk(sentence_end + 1, ".!?");
        }
    }

   return (total_sentences > 0) ? total_words / total_sentences : 0;
}

#include <stdio.h>
#include <string.h>
#include <ctype.h>

int count_conjunctions(FILE *f) {
    int count = 0;
    char line[1024];
    
    char *conjunctions[] = {"et", "mais", "ou", "donc", "car", "ni", "puisque", "bien que", "quoique", ",", ";", ":", NULL};
    
    char conjunctions_punctuation[] = {'.', '!', '?', ',', ';', ':'};

    while (fgets(line, sizeof(line), f) != NULL) {
        char *word = strtok(line, " \t\n");
        while (word != NULL) {
            for (int i = 0; conjunctions[i] != NULL; i++) {
                if (strcasecmp(word, conjunctions[i]) == 0) {
					count++;
                    break;
                }
            }
            word = strtok(NULL, " \t\n");
        }
        for (int i = 0; line[i] != '\0'; i++) {
            if (strchr(conjunctions_punctuation, line[i]) != NULL) {
                count++;
            }
        }
    }

    return count;
}
