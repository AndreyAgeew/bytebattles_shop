#!/bin/bash

sleep 5

alembic upgrade head

python src/commands/fill_goods_table.py

stripe listen --forward-to 0.0.0.0:8000/webhook &

gunicorn src.main:app --workers 4 --worker-clas uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
