FROM brumbrum/python3
RUN apt-get update && apt-get -y install  python-dev && apt-get -y install build-essential 
#RUN sudo apt install python3-pip
#COPY  requirements.txt /notebooks/dynamic_time_wraping_v3.ipynb  /
WORKDIR /wise
#COPY requirements.txt /notebooks/dynamic_time_wraping_v3.py   /wise/
COPY requirements.txt notebooks/teste.py   /wise/
RUN pip install -r  /wise/requirements.txt
CMD ["python","./teste.py"]
#CMD ["jupyter notebook","notebooks/dynamic_time_wraping_v3.ipynb"]
