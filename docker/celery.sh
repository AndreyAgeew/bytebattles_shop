#!/bin/bash

sleep 10

celery --app=src.jobs.celery:celery worker -l INFO