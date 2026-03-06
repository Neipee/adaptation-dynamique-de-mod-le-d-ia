#ifndef TEXT_ANALYSIS_H
#define TEXT_ANALYSIS_H

#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint32_t word;
    uint32_t sentence;
} count;

count* word_sentence(FILE *f);
int syllabe(FILE *f);
int long_word(FILE *f);                   
double flesh_kincaid(FILE *f, int *word_count, int *sentence_count, int *syl_count);
double gunning_fog(FILE *f, int *word_count, int *sentence_count, int *long_count);
int unique(FILE *f);
int average_sentence_length(FILE *f);
int count_conjunctions(FILE *f);
#endif
