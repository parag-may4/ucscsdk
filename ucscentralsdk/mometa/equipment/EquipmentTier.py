"""This module contains the general information for EquipmentTier ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class EquipmentTierConsts():
    APPLY_ON_ASSOCIATION = "onAssociation"
    APPLY_RUN_TIME = "runTime"
    INT_ID_NONE = "none"
    POLICY_OWNER_LOCAL = "local"
    POLICY_OWNER_PENDING_POLICY = "pending-policy"
    POLICY_OWNER_POLICY = "policy"
    POLICY_OWNER_UNSPECIFIED = "unspecified"


class EquipmentTier(ManagedObject):
    """This is EquipmentTier class."""

    consts = EquipmentTierConsts()
    naming_props = set([u'name'])

    mo_meta = MoMeta("EquipmentTier", "equipmentTier", "cp-tier-[name]", None, "InputOutput", 0xff, [], ["admin", "ls-compute", "ls-config", "ls-config-policy", "ls-server", "ls-server-policy"], [u'orgOrg'], [u'equipmentChassisProfile'], [None])

    prop_meta = {
        "apply": MoPropertyMeta("apply", "apply", "string", None, MoPropertyMeta.READ_WRITE, 0x2, None, None, None, ["onAssociation", "runTime"], []), 
        "child_action": MoPropertyMeta("child_action", "childAction", "string", None, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "descr": MoPropertyMeta("descr", "descr", "string", None, MoPropertyMeta.READ_WRITE, 0x4, None, None, r"""[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]{0,256}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", None, MoPropertyMeta.READ_ONLY, 0x8, 0, 256, None, [], []), 
        "int_id": MoPropertyMeta("int_id", "intId", "string", None, MoPropertyMeta.INTERNAL, None, None, None, None, ["none"], ["0-4294967295"]), 
        "name": MoPropertyMeta("name", "name", "string", None, MoPropertyMeta.NAMING, 0x10, None, None, r"""[\-\.:_a-zA-Z0-9]{1,16}""", [], []), 
        "policy_level": MoPropertyMeta("policy_level", "policyLevel", "uint", None, MoPropertyMeta.READ_ONLY, None, None, None, None, [], []), 
        "policy_owner": MoPropertyMeta("policy_owner", "policyOwner", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["local", "pending-policy", "policy", "unspecified"], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", None, MoPropertyMeta.READ_ONLY, 0x20, 0, 256, None, [], []), 
        "src_templ_name": MoPropertyMeta("src_templ_name", "srcTemplName", "string", None, MoPropertyMeta.READ_WRITE, 0x40, None, None, r"""[\-\.:_a-zA-Z0-9]{0,32}""", [], []), 
        "status": MoPropertyMeta("status", "status", "string", None, MoPropertyMeta.READ_WRITE, 0x80, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
    }

    prop_map = {
        "apply": "apply", 
        "childAction": "child_action", 
        "descr": "descr", 
        "dn": "dn", 
        "intId": "int_id", 
        "name": "name", 
        "policyLevel": "policy_level", 
        "policyOwner": "policy_owner", 
        "rn": "rn", 
        "srcTemplName": "src_templ_name", 
        "status": "status", 
    }

    def __init__(self, parent_mo_or_dn, name, **kwargs):
        self._dirty_mask = 0
        self.name = name
        self.apply = None
        self.child_action = None
        self.descr = None
        self.int_id = None
        self.policy_level = None
        self.policy_owner = None
        self.src_templ_name = None
        self.status = None

        ManagedObject.__init__(self, "EquipmentTier", parent_mo_or_dn, **kwargs)

