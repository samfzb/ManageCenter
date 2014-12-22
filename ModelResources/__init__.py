# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

from Desire.BaseFramework.Database import db_base

from .DbModels.ResModels import *


def init():
    db_base.setup()