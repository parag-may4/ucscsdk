"""This module contains the general information for FabricDceSwSrv ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class FabricDceSwSrvConsts():
    ID_A = "A"
    ID_B = "B"
    ID_NONE = "NONE"
    ID_MGMT = "mgmt"


class FabricDceSwSrv(ManagedObject):
    """This is FabricDceSwSrv class."""

    consts = FabricDceSwSrvConsts()
    naming_props = set([u'id'])

    mo_meta = MoMeta("FabricDceSwSrv", "fabricDceSwSrv", "sw-[id]", VersionMeta.Version121a, "InputOutput", 0x3f, [], ["admin", "ls-network-policy"], [u'fabricDceSrv'], [u'fabricDceSwSrvEp', u'fabricDceSwSrvEpOperation', u'fabricDceSwSrvPc', u'fabricDceSwSrvPcOperation', u'fabricSubGroup'], ["Get"])

    prop_meta = {
        "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version121a, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version121a, MoPropertyMeta.READ_ONLY, 0x2, 0, 256, None, [], []), 
        "id": MoPropertyMeta("id", "id", "string", VersionMeta.Version121a, MoPropertyMeta.NAMING, 0x4, None, None, None, ["A", "B", "NONE", "mgmt"], []), 
        "locale": MoPropertyMeta("locale", "locale", "string", VersionMeta.Version121a, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|unknown|server|chassis|internal|external),){0,5}(defaultValue|unknown|server|chassis|internal|external){0,1}""", [], []), 
        "name": MoPropertyMeta("name", "name", "string", VersionMeta.Version121a, MoPropertyMeta.CREATE_ONLY, 0x8, None, None, r"""[\-\.:_a-zA-Z0-9]{0,16}""", [], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version121a, MoPropertyMeta.READ_ONLY, 0x10, 0, 256, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version121a, MoPropertyMeta.READ_WRITE, 0x20, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "transport": MoPropertyMeta("transport", "transport", "string", VersionMeta.Version121a, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|unknown|ether|dce|fc),){0,4}(defaultValue|unknown|ether|dce|fc){0,1}""", [], []), 
        "type": MoPropertyMeta("type", "type", "string", VersionMeta.Version121a, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|unknown|lan|san|ipc),){0,4}(defaultValue|unknown|lan|san|ipc){0,1}""", [], []), 
    }

    prop_map = {
        "childAction": "child_action", 
        "dn": "dn", 
        "id": "id", 
        "locale": "locale", 
        "name": "name", 
        "rn": "rn", 
        "status": "status", 
        "transport": "transport", 
        "type": "type", 
    }

    def __init__(self, parent_mo_or_dn, id, **kwargs):
        self._dirty_mask = 0
        self.id = id
        self.child_action = None
        self.locale = None
        self.name = None
        self.status = None
        self.transport = None
        self.type = None

        ManagedObject.__init__(self, "FabricDceSwSrv", parent_mo_or_dn, **kwargs)

