# Heating Devices Fake Data Generator

## Installation

Currently those instructions should work perfectly fine on Linux Ubuntu and MacOS:

```bash
sudo apt-get install --reinstall build-essential
sudo apt-get install libsnappy-dev libbz2-dev python3-bz2file bzip2
make install

```

On MacOS installation of snappy will be necessary:

```bash
brew install snappy

```

It is assumed that `python` binary points to python version `3.6+`

## Working with virtual env and jupyter:

After installation it is possible to run:

```bash
source .venv/bin/activate
jupyter notebook

```

It should open jupyter in default browser.

## How to connect my laptop AS WORKER?

NOTE! It is not necessary to work with cluster as a client.

After installing everything just run:

```bash
.venv/bin/dask-worker --name <your_kurz_here> --reconnect bda01.fuewroclaw.com:8786 --memory-limit <number_of_gb>GB --nthreads <number_of_proc_threads>

```
