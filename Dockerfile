FROM python:3.6-alpine

## move to python workdir
WORKDIR /usr/src/app

## install all requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

## download nltk resources
RUN python -c "import nltk; nltk.download('punkt')"

## expose port and run web-server
EXPOSE 8080
CMD [ "python", "./exec/web_interface.py" ]