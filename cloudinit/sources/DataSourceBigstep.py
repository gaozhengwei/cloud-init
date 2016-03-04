#
#    Copyright (C) 2015-2016 Bigstep Cloud Ltd.
#
#    Author: Alexandru Sirbu <alexandru.sirbu@bigstep.com>
#

import json

from cloudinit import log as logging
from cloudinit import sources
from cloudinit import util
from cloudinit import url_helper

LOG = logging.getLogger(__name__)


class DataSourceBigstep(sources.DataSource):
    def __init__(self, sys_cfg, distro, paths):
        sources.DataSource.__init__(self, sys_cfg, distro, paths)
        self.metadata = {}
        self.vendordata_raw = ""
        self.userdata_raw = ""

    def get_data(self, apply_filter=False):
        url = get_url_from_file()
        response = url_helper.readurl(url)
        decoded = json.loads(response.contents)
        self.metadata = decoded["metadata"]
        self.vendordata_raw = decoded["vendordata_raw"]
        self.userdata_raw = decoded["userdata_raw"]
        return True


def get_url_from_file():
    content = util.load_file("/var/lib/cloud/data/seed/bigstep/url")
    return content

# Used to match classes to dependencies
datasources = [
    (DataSourceBigstep, (sources.DEP_FILESYSTEM, sources.DEP_NETWORK)),
]


# Return a list of data sources that match this set of dependencies
def get_datasource_list(depends):
    return sources.list_from_depends(depends, datasources)