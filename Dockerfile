# BASE
FROM python:3.12.4-slim AS base
RUN apt-get update && apt-get install -y curl wget
RUN pip install poetry==1.7.1
RUN apt-get install -y poppler-utils ffmpeg

# CODEBASE
FROM base AS codebase
WORKDIR /app
COPY . .

# DEVELOPMENT TARGET
FROM codebase AS development
RUN poetry install --no-directory
EXPOSE 8000
CMD poetry run start


# PRODUCTION TARGET
FROM codebase AS production
RUN poetry install --no-directory
EXPOSE 8000
CMD poetry run start