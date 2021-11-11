FROM python:3.9-slim

RUN groupadd --gid 1000 -r python && useradd --uid 1000 -r -g python python
RUN pip install virtualenv poetry

WORKDIR /home/python
RUN chown -R python:python /home/python
USER python

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Copy the requirements in a separate layer
COPY --chown=python:python pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-interaction --no-ansi

# Copy rest of the project
COPY --chown=python:python . ./
# "Install" the project
RUN poetry install --no-dev --no-interaction --no-ansi
