FROM python
COPY . /work
WORKDIR /work
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "src/__main__.py" ]