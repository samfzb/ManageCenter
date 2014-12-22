# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

from Desire.BaseFramework.Database import db_session
from Desire.BaseFramework.Resource.comm import *
from Desire.BaseFramework.Resource.errors import ResourceNotExist

from Desire.ManageCenter.ModelResources.DbModels.ResModels import *

from .store import ResStore


_SERVER_STATE = {
    0 : 'unregistered',
    1 : 'online',
    2 : 'offline',
    3 : 'maintaining',
    'unregistered': 0,
    'online': 1,
    'offline': 2,
    'maintaining': 3
}

class Server(ResServer, ResStore):
    def set_state(self, new_state):
        global _SERVER_STATE

        if new_state not in _SERVER_STATE:
            raise ValueError('Invalid server state: %s' % new_state if new_state else 'None')

        self.state = new_state if isinstance(new_state, (int, long)) else _SERVER_STATE[new_state]
        self.store_to_db()

    def get_state(self):
        return self.state

    def get_state_string(self):
        global _SERVER_STATE
        return _SERVER_STATE[self.state]

    def is_registered(self):
        global _SERVER_STATE
        return self.state != _SERVER_STATE['unregistered']

    def map_from_model(self):
        session = db_session.get_session()
        self.model_server = session.query(ModelServer).filter(ModelServer.res_id==self.id).one()
        if self.model_server is None:
            raise ResourceNotExist("Server: id=%d, name=%s name does not exist!" % (self.id, self['name']))

        self.attributes['uuid'] = self.model_server.uuid
        self.attributes['role'] = self.model_server.role
        self.attributes['location'] = self.model_server.location
        self.attributes['num_of_processor'] = self.model_server.num_of_processor
        self.attributes['cores_of_per_processor'] = self.model_server.cores_of_per_processor
        # TODO: features of processor
        self.attributes['memory_size'] = self.model_server.memory_size

    def map_to_model(self):
        if not hasattr(self, 'model_server'):
            self.model_server = ModelServer()

        self.model_server.res_id = self.id
        self.model_server.uuid = self.attributes['uuid']
        self.model_server.role = self.attributes['role']
        self.model_server.location = self.attributes['location']
        self.model_server.num_of_processor = self.attributes['num_of_processor']
        self.model_server.cores_of_per_processor = self.attributes['cores_of_per_processor']
        self.model_server.memory_size = self.attributes['memory_size']

        return self.model_server,

    def remove_self(self):
        pass
