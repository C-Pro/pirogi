FROM python

COPY finetune.py Pipfile Pipfile.lockdock /app/
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system

CMD ["python", "finetune.py"]
