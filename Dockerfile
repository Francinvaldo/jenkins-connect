FROM brumbrum/python3
RUN apt-get update && apt-get -y install  python-dev && apt-get -y install build-essential 
WORKDIR /wise
COPY requirements.txt notebooks/teste.py   /wise/
RUN pip install -r  /wise/requirements.txt
CMD ["python","./teste.py"]

