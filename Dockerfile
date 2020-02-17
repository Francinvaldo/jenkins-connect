FROM brumbrum/python3
COPY  requirements.txt notebooks/dynamic_time_wraping_v3.ipynb  /
RUN pip install -r  /requirements.txt
#CMD ["python","/server.py"]
#CMD ["python","notebooks/dynamic_time_wraping_v3.py"]
CMD ["jupyter notebook","notebooks/dynamic_time_wraping_v3.ipynb"]
