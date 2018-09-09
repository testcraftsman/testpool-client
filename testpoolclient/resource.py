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


def _renew(*args, **kwargs):
    """ Renew VM acquisition. """

    hndl = args[0]
    hndl.renew()
    interval = hndl.expiration/2
    hndl.threading = threading.Timer(interval, _renew, args=(hndl,))


class Manager(object):
    """ Acquires a VM and renews its usage until this object is deleted.

    As long as the object exists, the VM acquired will be renewed.
    """
    def __init__(self, ip_addr, profile_name, expiration=60, interval=60):
        """ Acquire a VM given the parameters.

        @param expiration The time in seconds.
        """
        self.profile_name = profile_name
        self.ip_addr = ip_addr
        self.expiration = expiration
        self.interval = interval

    def acquire(self, blocking=True, expiration=None):
        """ Acquire an available VM. """

        if expiration is None:
            expiration = self.expiration

        params = {"expiration": expiration}

        while True:
            try:
                resp = requests.get(self._url_get("acquire"),
                                    urllib.urlencode(params))
                resp.raise_for_status()
                vm = json.loads(resp.text,
                                object_hook=lambda d: Namespace(**d))
                return vm
            except Exception:
                if blocking:
                    time.sleep(self.interval)
                    continue
                raise ResourceError("all VMs busy or pending")
        return None

    def release(self, vm):
        """ Release VM resource. """

        if vm is None:
            return
        requests.get(self._url_get("release"))

    def release_all(self):
        """ Release all resources. """

        requests.get(self._url_get("release-all"))

    def resource_wait(self, resource_available=None):
        """ Release all resources. """

        if resource_available:
            resource_available = details.resource_available

        details = self.detail_get()
        while resource_available < details.resource_max:
            time.sleep(self.interval)
            details = self.detail_get()

    def renew(self, vm):
        """ Return usage of the VM. """

        params = {"id": vm.id, "expiration": 100}
        resp = requests.get(self._url_get("renew"), urllib.urlencode(params))

    def _url_get(self, action):
        """ Create URL for the given action. """

        ##
        # This should be a config.
        url = "http://%s:8000/testpool/api/v1/" % self.ip_addr
        return url + "pool/%s/%s" % (action, self.profile_name)

    def detail_get(self):
        """ Create URL for the given action. """

        resp = requests.get(self._url_get("detail"))
        resp.raise_for_status()
        pool = json.loads(resp.text, object_hook=lambda d: Namespace(**d))
        return pool


class CtxtMgr(object):
    """ Context Manager for resources. """

    def __init__(self, mgr, blocking=True):
        """ Constructor.

        @param mgr (Manager) Handle to manager.
        @param blocking Wait for VM to be available.
        """

        self.mgr = mgr
        self.blocking = blocking
        self.vm = None

    def __enter__(self):
        """ Operations are handled in the constructor. """

        self.vm = self.mgr.acquire(self.blocking)
        return self.vm

    def __exit__(self, exception_type, exception_value, traceback):
        """ Operations are handled in the constructor. """

        self.mgr.release(self.vm)
