"""This module contains the general information for FabricSanMonCloud ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class FabricSanMonCloudConsts():
    MODE_END_HOST = "end-host"
    MODE_SWITCH = "switch"


class FabricSanMonCloud(ManagedObject):
    """This is FabricSanMonCloud class."""

    consts = FabricSanMonCloudConsts()
    naming_props = set([])

    mo_meta = MoMeta("FabricSanMonCloud", "fabricSanMonCloud", "sanmon", None, "InputOutput", 0xf, [], ["admin", "ext-san-config", "ext-san-policy"], [u'fabricEp'], [u'fabricFcMonSan', u'statsThresholdPolicy'], [None])

    prop_meta = {
        "child_action": MoPropertyMeta("child_action", "childAction", "string", None, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", None, MoPropertyMeta.READ_ONLY, 0x2, 0, 256, None, [], []), 
        "mode": MoPropertyMeta("mode", "mode", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["end-host", "switch"], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", None, MoPropertyMeta.READ_ONLY, 0x4, 0, 256, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", None, MoPropertyMeta.READ_WRITE, 0x8, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
    }

    prop_map = {
        "childAction": "child_action", 
        "dn": "dn", 
        "mode": "mode", 
        "rn": "rn", 
        "status": "status", 
    }

    def __init__(self, parent_mo_or_dn, **kwargs):
        self._dirty_mask = 0
        self.child_action = None
        self.mode = None
        self.status = None

        ManagedObject.__init__(self, "FabricSanMonCloud", parent_mo_or_dn, **kwargs)

