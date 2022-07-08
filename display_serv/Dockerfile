FROM python:3.10
COPY requirements.txt /display_serv/requirements.txt
WORKDIR /display_serv
RUN pip install -r requirements.txt
ENV PYTHONPATH /display_serv
COPY . /display_serv
ENTRYPOINT ["python"]
CMD ["/display_serv/runapp.py"]
# End of file