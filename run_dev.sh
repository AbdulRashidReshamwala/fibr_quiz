#!/bin/sh
export PROJECT_ID=fibr-quiz
uvicorn app.main:app --reload