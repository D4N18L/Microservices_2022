FROM python:3.10
COPY requirements.txt /FrontendUI/requirements.txt
WORKDIR /FrontendUI
RUN pip install -r requirements.txt
COPY . /FrontendUI
ENTRYPOINT ["python"]
CMD ["/FrontendUI/runapp.py"]