"""This module contains the general information for EquipmentPoolable ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class EquipmentPoolableConsts():
    OWNER_END_POINT = "end-point"
    OWNER_POOL = "pool"


class EquipmentPoolable(ManagedObject):
    """This is EquipmentPoolable class."""

    consts = EquipmentPoolableConsts()
    naming_props = set([u'id'])

    mo_meta = MoMeta("EquipmentPoolable", "equipmentPoolable", "chassis-pool-[id]", None, "InputOutput", 0x1f, [], ["read-only"], [], [], [None])

    prop_meta = {
        "assigned_to_dn": MoPropertyMeta("assigned_to_dn", "assignedToDn", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 256, None, [], []), 
        "child_action": MoPropertyMeta("child_action", "childAction", "string", None, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", None, MoPropertyMeta.READ_ONLY, 0x2, 0, 256, None, [], []), 
        "id": MoPropertyMeta("id", "id", "ulong", None, MoPropertyMeta.NAMING, 0x4, None, None, None, [], []), 
        "owner": MoPropertyMeta("owner", "owner", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["end-point", "pool"], []), 
        "pool_dn": MoPropertyMeta("pool_dn", "poolDn", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 256, None, [], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", None, MoPropertyMeta.READ_ONLY, 0x8, 0, 256, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", None, MoPropertyMeta.READ_WRITE, 0x10, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "sys_id": MoPropertyMeta("sys_id", "sysId", "uint", None, MoPropertyMeta.READ_ONLY, None, None, None, None, [], []), 
    }

    prop_map = {
        "assignedToDn": "assigned_to_dn", 
        "childAction": "child_action", 
        "dn": "dn", 
        "id": "id", 
        "owner": "owner", 
        "poolDn": "pool_dn", 
        "rn": "rn", 
        "status": "status", 
        "sysId": "sys_id", 
    }

    def __init__(self, parent_mo_or_dn, id, **kwargs):
        self._dirty_mask = 0
        self.id = id
        self.assigned_to_dn = None
        self.child_action = None
        self.owner = None
        self.pool_dn = None
        self.status = None
        self.sys_id = None

        ManagedObject.__init__(self, "EquipmentPoolable", parent_mo_or_dn, **kwargs)

