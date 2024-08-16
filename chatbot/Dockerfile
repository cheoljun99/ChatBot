FROM python:latest

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt/bbot

COPY ./* /opt/bbot/
WORKDIR /opt/bbot

RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install --upgrade pip
RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r requirements.txt

RUN chmod +x /opt/bbot/start.sh

CMD ["bash", "-c", "/opt/bbot/start.sh"]