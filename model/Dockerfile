FROM python:3.8.13 as base

# Pending to set .env variables
# ARG UID
# ARG GID

# Add a non-root user
# RUN addgroup --gid $GID app
# RUN adduser --disabled-login --geco '' --uid $UID --gid $GID app

# Append /home/app/.local/bin/ to PATH variable because
# gunicorn is installed there.
ENV PYTHONPATH=$PYTHONPATH:/src/
ENV PATH=$PATH:/home/app/.local/bin/

COPY ./ /src/

WORKDIR /src
# recursively add permissions of the current user inside of the src directory
# user app and group app 
# (currently executing command as a root user)

# RUN chown -R app:app /src/
# # add read and write permissions for users
# # give only read permissions for group
# # recursively in src directory
# RUN chmod u+rw,g=r -R /src/

# change app user after of chown command 
# USER app

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

FROM base as test
RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["python3", "/src/ml_service.py"]