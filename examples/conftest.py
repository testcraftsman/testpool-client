# Copyright (c) 2015-2018 Mark Hamilton, All rights reserved

""" Populate test database with an example.

Check to see if the user has created an example test profile, if not
create a fake example profile. A fake example profile uses an in memory
pretent hypervisor. This is sufficient for seeing the Testpool client
API in action and for debugging. However following the Qickstart
guide in Testpool shows how to provide an example profile for a KVM
hypervisor.ster1

This code would normally not be required. Refer to the quick start guide or
installation instruction for setting up a KVM hypervisor.

"""

import logging
import pytest
import testpoolclient.pool


##
# In order to run the examples against a real hypervisor, change this
# IP address. These values are identical to the quick start guide on
# purpose. All that is needed, is a VM called test.template.
class Global(object):
    """ Content for tests. """
    # pylint: disable=too-many-arguments
    # pylint: disable=too-few-public-methods

    def __init__(self, name, connection, product, template_name, count):
        self.name = name
        self.connection = connection
        self.product = product
        self.template_name = template_name
        self.count = count


##
# "connection": "qemu:///system",
GLOBAL = Global("testpoolexample", "127.0.0.1", "fake", "test.template", 3)


def teardown_db():
    """ Remove the fake profile used by testing. """

    pool_mgr = testpoolclient.pool.Manager("127.0.0.1")
    pools = pool_mgr.list()
    for pool in pools:
        if pool["name"] != GLOBAL.name:
            continue
        pool_mgr.remove(GLOBAL.name, True)


@pytest.fixture(scope="session", autouse=True)
def setup_db(request):
    """ Setup test database for examples. """

    logging.info("setup database")
    ##
    # Check to see if the user has created an example test profile, if not
    # create a fake example profile. This code would normally not be
    # required. Refer to the quick start guide or installation instruction
    # for setting up a KVM hypervisor.
    pool_mgr = testpoolclient.pool.Manager(GLOBAL.connection)
    pools = pool_mgr.list()
    pools = [item for item in pools if item["name"] == GLOBAL.name]
    if len(pools) == 0:  # pylint: disable=len-as-condition
        logging.info("add pool %s", GLOBAL.name)
        pool_mgr.add(GLOBAL.name, GLOBAL.product, GLOBAL.connection,
                     GLOBAL.template_name, GLOBAL.count)

    request.addfinalizer(teardown_db)
