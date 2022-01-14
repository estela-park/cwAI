FROM python:3.8
RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev
COPY . /app
# copy everything to /app
WORKDIR /app
# cwd = /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]