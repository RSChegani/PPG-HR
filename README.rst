.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/SteadyPulse.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/SteadyPulse
    .. image:: https://readthedocs.org/projects/SteadyPulse/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://SteadyPulse.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/SteadyPulse/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/SteadyPulse
    .. image:: https://img.shields.io/pypi/v/SteadyPulse.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/SteadyPulse/
    .. image:: https://img.shields.io/conda/vn/conda-forge/SteadyPulse.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/SteadyPulse
    .. image:: https://pepy.tech/badge/SteadyPulse/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/SteadyPulse
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/SteadyPulse

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===========
SteadyPulse
===========


    Estimate HR with IMU noise removal


This repo provides an introduction to analysis of PPG and IMU data using an open source data set. There is a notebook in each module that walks through the analysis step by step. 
For Gyro and ACC see: src/imu/analysis.ipynb
And for PPG see: src/ppg/analysis.ipynb

===========
Setting up the Virtual Environment
===========

1. Clone the repository:

..  code-block:: bash
| git clone https://github.com/yourusername/SteadyPulse.git  
| cd SteadyPulse


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
