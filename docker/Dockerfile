FROM python:3.6

# set locales
RUN apt update && apt install -y --no-install-recommends locales
RUN echo "ja_JP UTF-8" > /etc/locale.gen
RUN locale-gen

# setup directory
COPY . /parts-classity-predict
WORKDIR /parts-classity-predict

# install python packages
RUN python -m pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt

# cleanup
RUN apt autoremove -y
RUN rm -rf /root/.cache/
RUN apt clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "api_server.py"]