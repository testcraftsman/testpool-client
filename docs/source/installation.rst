.. _InstallationAnchor:

Installation
************

Getting Testpool-client
=======================

Testpool is installed from source, download the latest from `GitHub <http://www.github.com/testcraftsman/testpool-client/releases>`_. This is also where we track issues and feature request. Make sure to download the version that 
matches the installed Testpool. If Python-testpool version X.Y.Z-M. Install 
any version of this client starting with X.Y.W. Where W can be any value.

What is Installed
=================

Testpool-client consists of a python library to acquire and release an available VM.

Testpool-client Installation on Ubuntu 16.04
--------------------------------------------

A single testpool server is required for store VM pool status. Here are the
steps for installing testpool's server:

#. Install several required packages::

  sudo pip install http://github.com/testcraftman/testpool-client/archive/v0.0.2.tar.gz
