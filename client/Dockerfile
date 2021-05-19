FROM python:3

# install dependencies
RUN apt update
RUN apt install -y git bison flex zlib1g-dev libreadline-dev lsb-release

# create user
RUN useradd -m -s /bin/bash perffarm-user

# copy directory and change ownership
WORKDIR /client
COPY . .
RUN chown perffarm-user /client

USER perffarm-user

# install python packages
RUN pip install -r requirements.txt

ENTRYPOINT ["bash"]
