#!/bin/bash
DAY=${1-"01"}
poetry run python -m aoc2024.day${DAY}
