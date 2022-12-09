FROM python:3.8.2
ENV HOME /root
WORKDIR /root
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
# remember to turn off debugger when deploying
CMD /wait && python -u -m flask --app app run --host=0.0.0.0 -p 8000

