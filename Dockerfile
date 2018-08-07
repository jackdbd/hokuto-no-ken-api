# The FROM instruction initializes a new build stage and sets the Base Image
# for subsequent instructions.
FROM heroku/miniconda

# The LABEL instruction adds metadata to an image.
# To view an image’s labels, use the docker inspect command.
LABEL maintainer="jackdebidda@gmail.com"

# The ENV instruction sets the environment variable <key> to the value <value>.
ENV INSTALL_PATH /hokuto_app

# The RUN instruction will execute any commands in a new layer on top of the
# current image and commit the results. The resulting committed image will be
# used for the next step in the Dockerfile.
RUN mkdir -p $INSTALL_PATH

# The WORKDIR instruction sets the working directory for any RUN, CMD,
# ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile.
WORKDIR $INSTALL_PATH

# The COPY instruction copies new files or directories from <src> and adds them
# to the filesystem of the container at the path <dest>.
COPY conda-requirements.txt conda-requirements.txt

RUN conda create --name hokuto-app
RUN source activate hokuto-app

RUN conda install -c conda-forge scrapy
RUN conda install -c conda-forge Flask
RUN conda install -c conda-forge Flask-SQLAlchemy
RUN conda install -c conda-forge Flask-Migrate
RUN conda install -c conda-forge Flask-RESTPlus
RUN conda install -c conda-forge python-dotenv

RUN conda install -c conda-forge gunicorn

# COPY . .

# There can only be one CMD instruction in a Dockerfile.
# The main purpose of a CMD is to provide defaults for an executing container.
CMD gunicorn --bind 0.0.0.0:$PORT --access-logfile "app.wsgi:app"
