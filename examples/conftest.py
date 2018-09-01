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
import testpool.core.pool

##
# In order to run the examples against a real hypervisor, change this
# IP address. These values are identical to the quick start guide on
# purpose. All that is needed, is a VM called test.template.
GLOBAL = {"hostname": "127.0.0.1",
          "connection": "qemu:///system",
          "profile": "example",
          "count": 3}
##


def teardown_db():
    """ Remove the fake profile used by testing. """

    profiles = testpool.core.pool.profile_list()
    for profile in profiles:
        if profile.hv.product != "fake":
            continue
        if profile.name != GLOBAL["profile"]:
            continue
        if profile.hv.connection != GLOBAL["connection"]:
            continue
        testpool.core.pool.profile_remove(GLOBAL["profile"], True)


@pytest.fixture(scope="session", autouse=True)
def setup_db(request):
    """ Setup test database for examples. """

    logging.info("setup database")
    ##
    # Check to see if the user has created an example test profile, if not
    # create a fake example profile. This code would normally not be
    # required. Refer to the quick start guide or installation instruction
    # for setting up a KVM hypervisor.
    profiles = testpool.core.pool.profile_list()
    profiles = [item for item in profiles if item.name == GLOBAL["profile"]]
    if len(profiles) == 0:  # pylint: disable=len-as-condition
        testpool.core.profile.profile_add(GLOBAL["connection"], "fake",
                                          GLOBAL["profile"], GLOBAL["count"],
                                          "test.template")

    request.addfinalizer(teardown_db)
