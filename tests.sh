#!/bin/bash
poetry run pylint .
poetry run mypy .
