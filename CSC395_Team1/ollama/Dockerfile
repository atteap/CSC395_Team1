FROM ollama/ollama:latest

RUN ollama pull orca-mini:3b-q4_1

EXPOSE 11434

CMD ["ollama", "serve"]