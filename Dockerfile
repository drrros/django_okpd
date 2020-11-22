FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV APP_HOME=/code
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME
RUN addgroup --system app && adduser --disabled-password app --ingroup app
COPY . $APP_HOME
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir && \
    chmod +x entrypoint.sh && \
    chown -R app:app /code
USER app
ENTRYPOINT ["/code/entrypoint.sh"]
