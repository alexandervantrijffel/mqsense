mqsense
=======

|pre-commit| |Black|

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

Usage
-------

Step 1: run the Mosquitto server::
  
  docker-compose up -d

Step 2: subscribe to all topics::

  make run_subscribe

Step 3: publish a message to the Mosquitto server::

  make run_publish

License
-------

Distributed under the terms of the `MIT license`_,
*mqsense* is free and open source software.
