#!/bin/bash

awk '!a[$0]++' ./logs/get_lyric.csv > ./logs/uniq_get_lyric.csv
