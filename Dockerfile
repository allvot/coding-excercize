FROM python:3.11-slim

ENV PYTHONPATH=/app/src
ENV ROOT_PROJECT_PATH=/app/
WORKDIR /app

RUN echo 'PS1="\[\e[38;5;81m\]ThoughtFul Test\[\e[m\]\[\e[38;5;15m\] : \[\e[m\]\[\e[38;5;250m\]\w\[\e[m\]\[\e[38;5;231m\] λ \[\e[m\]"' >> ~/.bashrc