FROM python:3.8

COPY . .

RUN pip install -r req.txt
RUN pip install finviz

EXPOSE 3000

RUN echo "Complete!"
