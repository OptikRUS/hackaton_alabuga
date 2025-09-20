FROM python:3.13.2-alpine

ENV APP_PATH=/project
ENV PYTHONPATH=$APP_PATH/
ENV CUSTOM_USER=python-user

EXPOSE 8080

RUN addgroup -S $CUSTOM_USER && adduser -S $CUSTOM_USER -G $CUSTOM_USER
RUN mkdir $APP_PATH && chown -R $CUSTOM_USER:$CUSTOM_USER $APP_PATH
RUN apk update && apk add --no-cache make curl && pip install uv==0.6.8

USER $CUSTOM_USER:$CUSTOM_USER
WORKDIR $APP_PATH

COPY --chown=$CUSTOM_USER:$CUSTOM_USER uv.lock pyproject.toml ./
RUN uv venv

COPY --chown=$CUSTOM_USER:$CUSTOM_USER . ./

CMD ["uv", "run", "python", "src/main.py"]
