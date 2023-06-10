FROM prefecthq/prefect:2-python3.9

COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

ADD flows /opt/prefect/flows

COPY ./deploy.sh /deploy.sh
RUN chmod +x /deploy.sh

ENTRYPOINT /deploy.sh $0 $@