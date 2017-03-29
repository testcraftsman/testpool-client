.. _QuickStartAnchor:

Quick Start
===============

Testpool-client provides a python library for `Testpool <http://testpool-client.readthedocs.io/en/latest/>`_  on top of Testpool's REST API.

First follow Testpool's quick start `quick start <http://testpool.readthedocs.io/en/latest/quickstart.html>`_. Once Testpool is setup, return to this guide.

Testpool-client Installation
----------------------------

Run examples from source.

  #. setup Testpool for developmentInstall Testpool -client from github release area::
  #. Download testpool-client from github release area::

       wget https://github.com/testcraftsman/testpool-client/archive/v0.1.0.tar.gz
       tar -xf testpool-client-0.1.0.tar.gz

A Short Tour
------------

Using the profile established in the Testpool `quickstart <http://testpool.readthedocs.io/en/latest/quickstart.html>`_ guide::

  ./bin/tpl profile add example kvm qemu:///system test.template 3

The example directory in this repository provides an an example on how to
use the python API. The example is written as a py.test. To see it in action::

  py.test -s example/python_api.py

Please refer to the file's documentation.

.. literalinclude:: /../../examples/python_api.py
