# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

from Desire.ManageCenter.Center.Center import CenterApp
from Desire.ManageCenter.ModelResources import Resource


DEBUG = True

APP_CLASS = CenterApp

RESOURCE_DEF = Resource.get_res_map()

DATABASE = "mysql://root:1987426@localhost/desire?charset=utf8"

LOGGER_FILE = "c:/desire/var/log/desire/managecenter.log"
LOGGER_DB = True
LOGGER_LEVEL = "DEBUG"
