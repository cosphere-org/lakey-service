
import os

from setuptools import setup, find_packages
from lakey_service import __version__, __service_name__


# -- REQUIREMENTS
requirements_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')


def parse_requirements(requirements):

    return [
        r.strip()
        for r in requirements
        if (
            not r.strip().startswith('#') and
            not r.strip().startswith('-e') and
            r.strip())
    ]


with open(requirements_path) as f:
    requirements = parse_requirements(f.readlines())


setup(
    name=__service_name__,
    version=__version__,
    description='Lakey for opening up Data Lake for masses',
    # FIXME: change this!!!!!
    url='https://git.viessmann.com/projects/HAC/repos/laker',
    author='Viessmann Data Chapter Team',
    author_email='data-engineers@viessmann.com',
    packages=find_packages(),
    install_requires=requirements)
