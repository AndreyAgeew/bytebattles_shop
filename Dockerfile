FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir games_shop

WORKDIR games_shop

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN apt-get update && \
    apt-get install -y curl tar

RUN curl -O -L https://github.com/stripe/stripe-cli/releases/download/v1.18.0/stripe_1.18.0_linux_x86_64.tar.gz && \
    tar -xvf stripe_1.18.0_linux_x86_64.tar.gz && \
    mv stripe /usr/local/bin/

CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]