# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

import datetime

from Desire.BaseFramework.Database import db_session

from Desire.ManageCenter.ModelResources.DbModels.ResModels import *
from Desire.ManageCenter.ModelResources import ResCache



class ResStoreError(Exception):
    pass


class ResStore(object):
    def map_to_model(self):
        raise NotImplementedError("method 'map_to_model' was not implemented")

    def map_from_model(self):
        raise NotImplementedError("method 'map_from_model' was not implemented")

    def remove_self(self):
        raise NotImplementedError("method 'remove_self' was not implemented")

    def store_common(self):
        if self.id is None:
            self.model_comm = ModelResource()
        else:
            self.model_comm.updated_time = datetime.datetime.now()

        self.model_comm.name = self.attributes['name']
        self.model_comm.state = self.state
        self.model_comm.type = self.type

        return self.model_comm

    def store_relations(self):
        ref_resources = self.model_comm.ref_resources
        refs = set(self.ref_resources)
        db_exist_refs = set([res.id for res in ref_resources])

        add_refs = refs.difference(db_exist_refs)
        remove_refs = db_exist_refs.difference(refs)

        models_add = [ModelResourceRelations(res_id=self.id, ref_resources_id=i)
                      for i in add_refs
                    ]


        return models_add, remove_refs

    def store_to_db(self):
        session = db_session.get_session(autocommit=False)
        is_new_res = True if self.id is None else False
        try:
            comm_model = self.store_common()

            session.add(comm_model)
            session.flush()
            if is_new_res:
                self.id = self.model_comm.id

            models = []
            models.extend(self.map_to_model())

            # TODO: store all data
            session.add_all(models)
            session.flush()

            _add, _del = self.store_relations()
            if len(_add):
                session.add(_add)

            if len(_del):
                session.query(ModelResourceRelations).filter(
                    ModelResourceRelations.res_id==self.id,
                    ModelResourceRelations.ref_resources_id.in_(_del)
                ).delete(synchronize_session=False)

            session.flush()

            session.commit()
        except Exception as e:
            session.rollback()
            if is_new_res:
                self.id = None
            raise ResStoreError('Can not store resource(type: %s), error: %s!' % (self.type, str(e)))

    def set_common(self, model_comm):
        assert model_comm

        self.model_comm = model_comm


def load_resource_by_id(res_id):
    session = db_session.get_session()
    try:
        res_cache = ResCache.get_res_cache()

        model_res = session.query(ModelResource).filter(ModelResource.id==res_id).one()

        ref_res = [ref.ref_resources_id for ref in model_res.ref_resources]

        res = res_cache.create(id=model_res.id,
                               type=model_res.type,
                               name=model_res.name,
                               state=model_res.state,
                               ref_resources=ref_res)

        if hasattr(res, 'set_common'):
            res.set_common(model_res)

        if hasattr(res, 'map_from_model'):
            res.map_from_model()

        return res
    except:
        raise ValueError("Invalid resource id: %d" % res_id)


def load_resource_list(res_type, limit={}):
    session = db_session.get_session()
    res_list = []
    try:
        res_cache = ResCache.get_res_cache()

        # TODO: process parameter limit
        all_resources = session.query(ModelResource).filter(ModelResource.type==res_type)

        for res_item in all_resources:
            res = res_cache.get(res_item, load_from_db=False)
            if res is None:
                ref_res = [ref.ref_resources_id for ref in res_item.ref_resources]
                res = res_cache.create(id=res_item.id,
                                       type=res_item.type,
                                       name=res_item.name,
                                       state=res_item.state,
                                       ref_resources=ref_res)
                res_cache.store(res, save_to_db=False)

            res_list.append(res)

        return res_list
    except:
        raise ValueError('invalid resource type: %s' % res_type)


def store_resource(res):
    res.store_to_db()
