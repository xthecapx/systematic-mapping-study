FROM jupyter/datascience-notebook

WORKDIR /home/jovyan/work

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader punkt_tab
RUN python -m nltk.downloader averaged_perceptron_tagger_eng
