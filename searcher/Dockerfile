FROM python:3.11

ARG DATABASE_URL
ENV DATABASE_URL ${DATABASE_URL}

ARG CERTIFICATE_URL
ENV CERTIFICATE_URL ${CERTIFICATE_URL}

WORKDIR /app

COPY ./searcher/requirements.txt ./searcher/requirements.txt

RUN pip install --no-cache-dir -r ./searcher/requirements.txt

COPY . . 

# 証明書のダウンロード
RUN curl --create-dirs -o /home/.postgresql/root.crt $CERTIFICATE_URL

# modelの学習とビルド
RUN python -m searcher.build

RUN rm -f secret/service-account.json
# ENV GOOGLE_APPLICATION_CREDENTIALS ""

EXPOSE 8000

CMD ["uvicorn", "searcher.app:app", "--host", "0.0.0.0", "--port", "8000"]
