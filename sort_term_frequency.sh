#!/bin/bash

cat ./term_frequency/karaoke.csv | sort -rn > ./term_frequency/sorted_karaoke.csv
cat ./term_frequency/usen.csv | sort -rn > ./term_frequency/sorted_usen.csv
