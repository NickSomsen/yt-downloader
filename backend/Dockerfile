FROM python:3.10
WORKDIR /code
# install requirements so this layer can be cached by docker when requirments don't change
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
COPY . .
EXPOSE 8000
# workdir is /code where main.py is also located
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
