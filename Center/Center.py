# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

from Desire.BaseFramework.Database.db_base import setup
from Desire.ManageCenter.ModelResources.DbModels.ResModels import *
from Desire.ManageCenter.ModelResources.Resource.Server import Server
from Desire.BaseFramework.Resource.CacheManager import ResCacheManager
from Desire.ManageCenter.ModelResources.Resource.store import load_resource_by_id

class CenterApp(object):
    def __init__(self, *args, **kwargs):
        setup()
        self.test()

    def test(self):
        # server = ResCacheManager.create(
        #     name="FirstServer",
        #     type="server",
        #     state=0,
        #     ref_resources=[],
        #     uuid="50b9ce6c-ba04-4212-a8dc-a6d39339a762",
        #     role=1,
        #     location='localhost',
        #     num_of_processor=2,
        #     cores_of_per_processor=2,
        #     memory_size=1024
        # )
        #
        # server.store_to_db()
        server = load_resource_by_id(7)
        print server['id']
        print server['name']

        pass
