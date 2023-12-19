# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11.4-slim-buster

# Add user that will be used in the container.
RUN groupadd -g 1000 faceauth && \
    useradd -ms /bin/bash -N faceauth -u 1000 -g 1000

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable. This should match "EXPOSE" command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown faceauth:faceauth /app

# Copy the source code of the project into the container.
COPY --chown=faceauth:faceauth . .

## Install the project requirements.
RUN pip install -r /app/requirements.txt


# Use user "wagtail" to run the build commands below and the server itself.
USER faceauth

ENTRYPOINT ["/app/entrypoint/entrypoint.sh"]
