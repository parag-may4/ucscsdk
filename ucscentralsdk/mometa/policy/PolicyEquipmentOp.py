"""This module contains the general information for PolicyEquipmentOp ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class PolicyEquipmentOpConsts():
    SOURCE_LOCAL = "local"
    SOURCE_PENDING_POLICY = "pending-policy"
    SOURCE_POLICY = "policy"
    SOURCE_UNSPECIFIED = "unspecified"
    TRIGGER_STATUS_TRIGGER_ACKED = "trigger-acked"
    TRIGGER_STATUS_TRIGGER_FAILED = "trigger-failed"
    TRIGGER_STATUS_TRIGGERED = "triggered"
    TRIGGER_STATUS_UNKNOWN = "unknown"


class PolicyEquipmentOp(ManagedObject):
    """This is PolicyEquipmentOp class."""

    consts = PolicyEquipmentOpConsts()
    naming_props = set([])

    mo_meta = MoMeta("PolicyEquipmentOp", "policyEquipmentOp", "equipment-ctrl", None, "InputOutput", 0x3f, [], ["admin", "pn-equipment", "pn-policy"], [u'policyControlEpOp'], [u'faultInst'], [None])

    prop_meta = {
        "child_action": MoPropertyMeta("child_action", "childAction", "string", None, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", None, MoPropertyMeta.READ_ONLY, 0x2, 0, 256, None, [], []), 
        "last_modified": MoPropertyMeta("last_modified", "lastModified", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, r"""([0-9]){4}-([0-9]){2}-([0-9]){2}T([0-9]){2}:([0-9]){2}:([0-9]){2}((\.([0-9]){3})){0,1}""", [], []), 
        "remote_error_code": MoPropertyMeta("remote_error_code", "remoteErrorCode", "uint", None, MoPropertyMeta.READ_ONLY, None, None, None, None, [], []), 
        "remote_error_descr": MoPropertyMeta("remote_error_descr", "remoteErrorDescr", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", None, MoPropertyMeta.READ_ONLY, 0x4, 0, 256, None, [], []), 
        "source": MoPropertyMeta("source", "source", "string", None, MoPropertyMeta.READ_WRITE, 0x8, None, None, None, ["local", "pending-policy", "policy", "unspecified"], []), 
        "status": MoPropertyMeta("status", "status", "string", None, MoPropertyMeta.READ_WRITE, 0x10, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "trigger_status": MoPropertyMeta("trigger_status", "triggerStatus", "string", None, MoPropertyMeta.READ_WRITE, 0x20, None, None, None, ["trigger-acked", "trigger-failed", "triggered", "unknown"], []), 
    }

    prop_map = {
        "childAction": "child_action", 
        "dn": "dn", 
        "lastModified": "last_modified", 
        "remoteErrorCode": "remote_error_code", 
        "remoteErrorDescr": "remote_error_descr", 
        "rn": "rn", 
        "source": "source", 
        "status": "status", 
        "triggerStatus": "trigger_status", 
    }

    def __init__(self, parent_mo_or_dn, **kwargs):
        self._dirty_mask = 0
        self.child_action = None
        self.last_modified = None
        self.remote_error_code = None
        self.remote_error_descr = None
        self.source = None
        self.status = None
        self.trigger_status = None

        ManagedObject.__init__(self, "PolicyEquipmentOp", parent_mo_or_dn, **kwargs)

