FROM alpine:latest

RUN apk update && apk upgrade && apk add --no-cache \
    python3 \
    py3-pip

RUN adduser flask -D

WORKDIR /home/flask/azziTowing
RUN chown -R flask:flask /home/flask/azziTowing

USER flask

ENV PATH=/home/flask/.local/bin:$PATH
ENV HOME=/home/flask/

COPY . . 
RUN pip3 install -r requirements.txt
RUN rm requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
