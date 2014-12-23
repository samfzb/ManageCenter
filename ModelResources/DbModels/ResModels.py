# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship

from Desire.BaseFramework.Database.db_base import Base


class ModelResource(Base):
    __tablename__ = "resource"

    id = Column(Integer, primary_key=True, unique=True)

    name = Column(String(64), nullable=False, index=True)
    state = Column(Integer, default=0)
    type = Column(String(32), default='')

    created_time = Column(DateTime, default=datetime.now)
    updated_time = Column(DateTime, default=datetime.now)

    ref_resources = relationship("ModelResourceRelations", backref="resource_relations")


class ModelResourceRelations(Base):
    __tablename__ = "resource_relations"

    id = Column(Integer, primary_key=True, unique=True)

    res_id = Column(Integer, ForeignKey("resource.id"), index=True, nullable=False)
    ref_resources_id = Column(Integer, index=True, nullable=False)


class ModelServer(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, unique=True)
    res_id = Column(Integer, ForeignKey("resource.id"), nullable=False)

    uuid = Column(CHAR(36), index=True, nullable=False)
    role = Column(SMALLINT, default=0, nullable=False)
    location = Column(TEXT, nullable=False)

    num_of_processor = Column(SMALLINT, nullable=False)
    cores_of_per_processor = Column(SMALLINT, nullable=False)

    # 使用JSON描述处理器特征
    feature_of_processor = Column(TEXT, nullable=True)

    # memory size: GB
    memory_size = Column(Integer, nullable=False)

    # LOAD?负载信息？实时信息，不在此处更新


class ModelServerGroups(Base):
    __tablename__ = "server_groups"

    id = Column(Integer, primary_key=True, unique=True)
    res_id = Column(Integer, ForeignKey("resource.id"), nullable=False)

    name = Column(String(64), index=True, nullable=False)


__all__ = [
    "ModelResource",
    "ModelResourceRelations",
    "ModelServer",
    "ModelServerGroups"
]
