FROM jupyter/tensorflow-notebook

ENV DEBIAN_FRONTEND=noninteractive

USER root

# Add Java and dependencies for Spark
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    curl \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Dynamically detect JAVA_HOME and create symlink for Spark compatibility
RUN JAVA_PATH=$(dirname $(dirname $(readlink -f $(which java)))) && \
    ln -s "$JAVA_PATH" /usr/lib/jvm/java-11-openjdk-amd64 && \
    echo "export JAVA_HOME=$JAVA_PATH" >> /etc/profile.d/java_home.sh && \
    echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> /etc/profile.d/java_home.sh

# Set the environment variables so Spark and subprocesses can find Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Download and install Apache Spark from the reliable archive URL
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
RUN curl -L https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    | tar -xz -C /opt/ && \
    ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYSPARK_PYTHON=python3

USER ${NB_UID}

# Install Python packages (includes plotly, dash, pyspark)
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    scipy==1.11.4 \
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
    beautifulsoup4 \
    Mastodon.py \
    geopy \
    tweet-preprocessor \
    openai \
    deepl \
    better_profanity \
    pyspark==3.5.0

# Download NLTK corpora and TextBlob data
RUN python -m textblob.download_corpora && \
    python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords')"

# Download spaCy English models
RUN python -m spacy download en_core_web_sm && \
    python -m spacy download en_core_web_md && \
    python -m spacy download en_core_web_lg

# copy repo files -- COMMENT OUT THIS LINE WHEN BUILDING A LOCAL DOCKER CONTAINER ON YOUR COMPUTER
COPY . /home/jovyan/

# Expose Jupyter, Spark UI, Dash ports
EXPOSE 8888 4040 8050
