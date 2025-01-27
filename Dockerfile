FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
# LVD MODIFICATION START
  POETRY_VERSION=1.5.1 \
  PEP517_BUILD_BACKEND=setuptools.build_meta
# LVD MODIFICATION END

RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code
# LVD MODIFICATION START
RUN chmod 777 /code
RUN chmod +x /code/start_all.sh
RUN chmod +x /code/start_all_no_filters.sh
RUN chmod +x /code/start_chroma.sh
RUN chmod +x /code/start_chroma_no_filters.sh
RUN chmod +x /code/start_weaviate.sh
RUN chmod +x /code/start_weaviate_no_filters.sh
RUN chmod +x /code/start_lvd_no_filters.sh
RUN chmod +x /code/start_milvus_all.sh
RUN chmod +x /code/start_milvus_no_filters.sh
RUN chmod +x /code/start_lvd.sh
RUN chmod +x /code/start_qdrant.sh
RUN chmod +x /code/start_qdrant_no_filters.sh

CMD ["./start_chroma.sh"]
# LVD MODIFICATION END