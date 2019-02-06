#!/bin/bash
for i in 1 2 3 4 5 6 7 8
do
    python3 run_remote.py ~/.ssh/beam_competitions_key.pem ${i} Exploration_3 random_inputs
done
