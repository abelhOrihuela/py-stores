FROM python:3.7.1

LABEL Author="Abel Orihuela"
LABEL E-mail="abelorihuelamendoza@hotmail.com"
LABEL version="0.0.1"

ENV FLASK_APP "app.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

RUN mkdir /code
WORKDIR /code

COPY Pip* /code/

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --system --deploy --ignore-pipfile

ADD . /code

EXPOSE 5000

CMD flask run --host=0.0.0.0