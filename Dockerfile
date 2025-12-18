FROM python:3.9

WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all files
COPY . .

# Set environment variables so Flask runs on the correct port automatically
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=7860
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask using the 'flask run' command instead of 'python app.py'
# This overrides whatever port is written in your script
CMD ["flask", "run"]