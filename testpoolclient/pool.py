# Copyright (c) 2015-2018 Mark Hamilton, All rights reserved

""" Client python API to reserve VMs. """
import json
import time
import requests
import urllib
import threading
from argparse import Namespace
import testpool.core.exceptions


class ResourceError(testpool.core.exceptions.TestpoolError):
    """ Thrown when a resource is not available. """
    def __init__(self, message):
        super(testpool.core.exceptions.TestpoolError, self).__init__(message)


class Manager(object):
    """ Retrieve Pool information. """
    def __init__(self, ip_addr, version=None):
        """ Construct Python API to TestPool information.
        @param id_addr Address of Test Pool server.
        @param version The version of the REST API.
        """

        if not version:
            version = "v1"

        self._version = version
        self.ip_addr = ip_addr

    def _url_get(self, action):
        """ Create URL for the given action. """

        fmt = "http://%s:8000/testpool/api/%s/pool/%s"
        url = fmt % (self.ip_addr, self._version, action)
        return url

    def list(self):
        """ Return the list of pools. """

        resp = requests.get(self._url_get("list"))
        resp.raise_for_status()
        return json.loads(resp.text)

    def detail_get(self, pool_name):
        """ Create URL for the given action. """

        url = self._url_get("detail/%s" % pool_name)
        resp = requests.get(url)
        resp.raise_for_status()
        return json.loads(resp.text)

    def remove(self, name, immediate=False):
        """ Remove a pool.

        When immediate is False, resources in a pool are given time to
        shutdown. Resources are then removed when successfully shutdown.
        The pool is removed once all resources have been removed.
        When immediate is True, resource and pool are removed from the
        database immediately.

        @param name Name of the pool to remove.
        :param immediate (bool): False by default. When true force removal
                                 of Testpool content. Do not wait for resources
                                 to gracefully shutdown.
        """

        url = self._url_get("remove/%s?immediate=%s" % (name, immediate))
        resp = requests.delete(url)
        resp.raise_for_status()
        return json.loads(resp.text)

    def add(self, name, product, connection, template_name, resource_max):
        """ Add a pool given the name and additional parameters.

        @param name (str): Name of the pool used to identify the profile.
        @param product: A supported product i.e. docker.
        @param connection: Depends on the product.
        @param template_name: The template name which depends on the product. 
        @param resource_max: The maximum number of resources.
        """

        params = {
            "connection": connection,
            "product": product,
            "resource_max": resource_max,
            "template_name": template_name,
        }

        url = self._url_get("add/%s" % name)
        resp = requests.post(url, params=params)
        resp.raise_for_status()
        return json.loads(resp.text)
