FROM python:3.11

WORKDIR /home

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && mkdir -p /root/.local/bin \
    && chmod -R 777 /root/.local/bin

RUN apt-get update && apt-get install -y vim


# add .local/bin to PATH
ENV PATH="/root/.local/bin:$PATH"
