FROM python:3.7

WORKDIR /usr/src/app
COPY Pipfile* ./
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . ./
CMD ["python3", "main.py"]