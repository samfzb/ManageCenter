# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

from .Server import Server
from .ServerGroup import ServerGroup
from .VirtualMachine import VirtualMachine
from .StorageDevice import StorageDevice
from .VirtualDisk import VirtualDisk
from .Network import Network
from .NetworkInterfaceController import NIC


_RES_MAP = {
    "server": Server,
    "server_group": ServerGroup,
    "virtual_machine": VirtualMachine,
    "storage_device": StorageDevice,
    "virtual_disk": VirtualDisk,
    "network": Network,
    "network_interface_controller": NIC
}


def get_res_map():
    global _RES_MAP

    return _RES_MAP