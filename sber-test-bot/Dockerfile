FROM python:3.7-alpine

WORKDIR /usr/src/app
COPY Pipfile* ./
RUN apk update && apk add g++ gcc libxml2 libxslt-dev
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . ./
CMD ["python3", "main.py"]