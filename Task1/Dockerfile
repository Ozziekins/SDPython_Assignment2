FROM python
COPY . /work
WORKDIR /work
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "main.py" ]