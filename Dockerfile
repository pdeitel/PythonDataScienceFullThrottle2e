FROM quay.io/jupyter/tensorflow-notebook:latest

ENV DEBIAN_FRONTEND=noninteractive

USER root

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN printf '%s\n' \
      'Acquire::Retries "5";' \
      'Acquire::http::Timeout "60";' \
      'Acquire::https::Timeout "60";' \
      > /etc/apt/apt.conf.d/99-retries \
   && apt-get update \
   && apt-get install -y --no-install-recommends \
      openjdk-17-jdk \
      build-essential \
      curl \
      ffmpeg \
      libjpeg-dev \
      libpng-dev \
      libsm6 \
      libxext6 \
      libxrender-dev \
      zlib1g-dev \
   && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV PYSPARK_PYTHON=python3

RUN pip install --no-cache-dir pyspark==3.5.0

RUN pip install --no-cache-dir \
    spacy \
    wordcloud \
    textblob \
    nltk \
    folium \
    plotly \
    dash \
    pymongo \
    dnspython \
    pubnub \
    'Mastodon.py>=2.1.4' \
    geopy \
    tweet-preprocessor \
    openai \
    deepl \
    better_profanity \
    playsound3

RUN python -m textblob.download_corpora \
 && python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords')"

RUN python -m spacy download en_core_web_sm \
 && python -m spacy download en_core_web_md \
 && python -m spacy download en_core_web_lg

RUN fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

COPY . /home/jovyan/

EXPOSE 8888 4040 8050