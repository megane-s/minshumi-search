FROM python:3.11

ARG GCS_BUCKET

WORKDIR /app

COPY ./searcher/requirements.txt ./searcher/requirements.txt

RUN pip install --no-cache-dir -r ./searcher/requirements.txt

COPY . . 

ENV GOOGLE_APPLICATION_CREDENTIALS secret/service-account.json
ENV GCS_BUCKET $GCS_BUCKET

RUN python -m searcher.build

RUN rm secret/service-account.json
ENV GOOGLE_APPLICATION_CREDENTIALS ""


EXPOSE 8000

CMD ["uvicorn", "searcher.app:app", "--host", "0.0.0.0", "--port", "8000"]
