"""This module contains the general information for TagDef ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class TagDefConsts():
    MULTIPLE_FALSE = "false"
    MULTIPLE_NO = "no"
    MULTIPLE_TRUE = "true"
    MULTIPLE_YES = "yes"
    RESTRICTED_FALSE = "false"
    RESTRICTED_NO = "no"
    RESTRICTED_TRUE = "true"
    RESTRICTED_YES = "yes"
    SYSTEM_DEFINED_FALSE = "false"
    SYSTEM_DEFINED_NO = "no"
    SYSTEM_DEFINED_TRUE = "true"
    SYSTEM_DEFINED_YES = "yes"


class TagDef(ManagedObject):
    """This is TagDef class."""

    consts = TagDefConsts()
    naming_props = set([u'name'])

    mo_meta = MoMeta("TagDef", "tagDef", "type-[name]", None, "InputOutput", 0x1ff, [], ["admin", "tag"], [u'tagDefEp'], [u'tagItem'], [None])

    prop_meta = {
        "child_action": MoPropertyMeta("child_action", "childAction", "string", None, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "color": MoPropertyMeta("color", "color", "string", None, MoPropertyMeta.READ_WRITE, 0x2, 0, 510, None, [], []), 
        "descr": MoPropertyMeta("descr", "descr", "string", None, MoPropertyMeta.READ_WRITE, 0x4, None, None, r"""[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]{0,256}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", None, MoPropertyMeta.READ_ONLY, 0x8, 0, 256, None, [], []), 
        "multiple": MoPropertyMeta("multiple", "multiple", "string", None, MoPropertyMeta.READ_WRITE, 0x10, None, None, None, ["false", "no", "true", "yes"], []), 
        "name": MoPropertyMeta("name", "name", "string", None, MoPropertyMeta.NAMING, 0x20, None, None, r"""[ !#$%&\(\)\*\+,\-\.:;=\?@\[\]_\{\|\}~a-zA-Z0-9]{1,32}""", [], []), 
        "restricted": MoPropertyMeta("restricted", "restricted", "string", None, MoPropertyMeta.READ_WRITE, 0x40, None, None, None, ["false", "no", "true", "yes"], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", None, MoPropertyMeta.READ_ONLY, 0x80, 0, 256, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", None, MoPropertyMeta.READ_WRITE, 0x100, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "system_defined": MoPropertyMeta("system_defined", "systemDefined", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["false", "no", "true", "yes"], []), 
    }

    prop_map = {
        "childAction": "child_action", 
        "color": "color", 
        "descr": "descr", 
        "dn": "dn", 
        "multiple": "multiple", 
        "name": "name", 
        "restricted": "restricted", 
        "rn": "rn", 
        "status": "status", 
        "systemDefined": "system_defined", 
    }

    def __init__(self, parent_mo_or_dn, name, **kwargs):
        self._dirty_mask = 0
        self.name = name
        self.child_action = None
        self.color = None
        self.descr = None
        self.multiple = None
        self.restricted = None
        self.status = None
        self.system_defined = None

        ManagedObject.__init__(self, "TagDef", parent_mo_or_dn, **kwargs)

