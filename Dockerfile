FROM python:3.6
LABEL maintainer "Marius Stanca <me@marius.xyz>"

ADD code /code

WORKDIR /code
RUN pip install -r requirements.txt

EXPOSE 8080 6543 3031
CMD ["bash", "/code/entry.sh"]
