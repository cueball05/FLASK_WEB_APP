FROM python:3.9

WORKDIR /main
COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]