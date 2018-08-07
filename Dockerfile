# The FROM instruction initializes a new build stage and sets the Base Image
# for subsequent instructions.
FROM heroku/miniconda

# The LABEL instruction adds metadata to an image.
# To view an image's labels, use the docker inspect command.
LABEL maintainer="jackdebidda@gmail.com"

# https://docs.docker.com/engine/reference/builder/#env
ENV APP_ROOT=/hokuto_app CONDA_ENV_NAME=hokuto-env

# The RUN instruction will execute any commands in a new layer on top of the
# current image and commit the results. The resulting committed image will be
# used for the next step in the Dockerfile.
RUN mkdir -p ${APP_ROOT}

# The WORKDIR instruction sets the working directory for any RUN, CMD,
# ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile.
WORKDIR ${APP_ROOT}

# Update conda and setup environment
RUN conda update conda -y && conda create --name ${CONDA_ENV_NAME} python=3.6 -y

# Using the docker ENV instruction it is possible to add the virtual environment
# path persistently to PATH
ENV PATH /opt/conda/envs/${CONDA_ENV_NAME}/bin:$PATH
ENV CONDA_DEFAULT_ENV ${CONDA_ENV_NAME}
ENV CONDA_PREFIX /opt/conda/envs/${CONDA_ENV_NAME}

# This is for checking that the conda environment was created and activated.
RUN conda env list

# TODO: install these dependencies from a environment.yml or requirements.txt
RUN conda install scrapy -y
RUN conda install flask -y
RUN conda install --channel conda-forge flask-sqlalchemy -y
RUN conda install --channel conda-forge flask-migrate -y
RUN conda install --channel conda-forge flask-restplus -y
RUN conda install --channel conda-forge python-dotenv -y

# gunicorn is not a dependency in development, so we have to install it now.
RUN conda install --channel conda-forge gunicorn -y

COPY . .

# Either one of these commands is fine.
# CMD gunicorn --bind 0.0.0.0:$PORT --access-logfile - "app.app:create_app()"
CMD gunicorn --bind 0.0.0.0:$PORT --access-logfile - "app.wsgi:application"
