#!/bin/bash
poetry run pytest \
    -vvl \
    --color=yes \
    --cov=subete.repo \
    --cov-branch \
    --cov-report term-missing \
    --cov-report=html:html_cov/ \
    "$@" \
    tests/
