# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

from Desire.ManageCenter.ModelResources.ResCache import get_res_cache
from Desire.ManageCenter.ModelResources.Resource import store
from Desire.ManageCenter.Biz.errors import *


class ServerManager(object):
    def __init__(self):
        self.res_cache = get_res_cache()

    def register_server(self, server):
        assert(server)

        try:
            if server.get_state() == 0:
                server.set_state("unregistered")
        except:
            raise

    def add_server(self, server):
        assert(server)

        try:
            if server.get_state() == 0:
                server.set_state("online")
        except:
            raise

    def remove_server(self, server):
        assert(server)

        if server.is_new() or (not server.is_registered()):
            return

        server.remove_self()

    def poweron_server(self, server):
        # TODO: add code here
        pass

    def shutdown_server(self, server):
        # TODO: add code here
        pass

    def maintain_server(self, server):
        assert server

        if server.is_new() or (not server.is_registered()):
            raise ServerStateError("Server: %s(UUID:%s, location: %s) was not registered" %
                                   (
                                       server['name'], server['uuid'], server['location']
                                   ))

        try:
            server.set_state('maintaining')

            # TODO: add code here
            # migrate VMS? storage?
        except:
            pass

    def query_server_info(self, server):
        return server.to_dict()


    def ping_servers(self):
        # TODO: add code here
        pass

    def get_servers_list(self, limit={}):
        '''
        get all servers
        :param limit: {
            start: 0 (an integer),
            end : 100 (an integer)
        }
        :return:
        '''
        return store.load_resource_list("server", limit=limit)
