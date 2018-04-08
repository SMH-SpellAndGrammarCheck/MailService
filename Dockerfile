FROM python:2

ADD src/ /srv/py/src
ADD res/ /srv/py/res

EXPOSE 8080

CMD /srv/py/src/http/http.py 8080