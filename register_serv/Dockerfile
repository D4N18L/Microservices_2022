FROM python:3.10
COPY requirements.txt  /register_serv/requirements.txt
WORKDIR  /register_serv
RUN pip install -r requirements.txt
COPY . /register_serv
ENTRYPOINT ["python"]
CMD ["/register_serv/runapp.py"]
