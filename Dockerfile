FROM alpine:latest

RUN apk update && apk upgrade && apk add --no-cache \
    python3 \
    py3-pip

RUN adduser flask -D

WORKDIR azziTowing
RUN chown -R flask:flask /azziTowing
USER flask

ENV PATH=/home/flask/.local/bin:$PATH

COPY . . 
RUN pip3 install -r requirements.txt
RUN rm requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]