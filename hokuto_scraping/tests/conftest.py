import os
from betamax import Betamax


HERE = os.path.abspath(os.path.dirname(__file__))
# where betamax will store cassettes (http responses)
# https://stackoverflow.com/a/38214137/3036129
CASSETTE_DIR = os.path.abspath(os.path.join(HERE, "fixtures", "cassettes"))

with Betamax.configure() as config:
    config.cassette_library_dir = CASSETTE_DIR
    config.preserve_exact_body_bytes = True
