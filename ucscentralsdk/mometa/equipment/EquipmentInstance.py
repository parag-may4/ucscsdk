"""This module contains the general information for EquipmentInstance ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class EquipmentInstanceConsts():
    ASSIGN_STATE_ASSIGNED = "assigned"
    ASSIGN_STATE_FAILED = "failed"
    ASSIGN_STATE_UNASSIGNED = "unassigned"
    ASSOC_STATE_ASSOCIATED = "associated"
    ASSOC_STATE_ASSOCIATING = "associating"
    ASSOC_STATE_DISASSOCIATING = "disassociating"
    ASSOC_STATE_FAILED = "failed"
    ASSOC_STATE_UNASSOCIATED = "unassociated"
    CONFIG_STATE_APPLIED = "applied"
    CONFIG_STATE_APPLYING = "applying"
    CONFIG_STATE_FAILED_TO_APPLY = "failed-to-apply"
    CONFIG_STATE_NOT_APPLIED = "not-applied"
    INT_ID_NONE = "none"
    OPER_STATE_CHASSIS_FAILED = "chassis-failed"
    OPER_STATE_CHASSIS_MISMATCH = "chassis-mismatch"
    OPER_STATE_CONFIG = "config"
    OPER_STATE_CONFIG_FAILURE = "config-failure"
    OPER_STATE_DECOMISSIONING = "decomissioning"
    OPER_STATE_DEGRADED = "degraded"
    OPER_STATE_DIAGNOSTICS = "diagnostics"
    OPER_STATE_DIAGNOSTICS_FAILED = "diagnostics-failed"
    OPER_STATE_DISABLED = "disabled"
    OPER_STATE_DISCOVERY = "discovery"
    OPER_STATE_DISCOVERY_FAILED = "discovery-failed"
    OPER_STATE_INACCESSIBLE = "inaccessible"
    OPER_STATE_INDETERMINATE = "indeterminate"
    OPER_STATE_INOPERABLE = "inoperable"
    OPER_STATE_MAINTENANCE = "maintenance"
    OPER_STATE_MAINTENANCE_FAILED = "maintenance-failed"
    OPER_STATE_OK = "ok"
    OPER_STATE_OPERABLE = "operable"
    OPER_STATE_PENDING_REASSOCIATION = "pending-reassociation"
    OPER_STATE_PENDING_REBOOT = "pending-reboot"
    OPER_STATE_POWER_OFF = "power-off"
    OPER_STATE_REMOVED = "removed"
    OPER_STATE_RESTART = "restart"
    OPER_STATE_TEST = "test"
    OPER_STATE_TEST_FAILED = "test-failed"
    OPER_STATE_UNASSOCIATED = "unassociated"
    OPER_STATE_UNCONFIG = "unconfig"
    OPER_STATE_UNCONFIG_FAILED = "unconfig-failed"
    POLICY_OWNER_LOCAL = "local"
    POLICY_OWNER_PENDING_POLICY = "pending-policy"
    POLICY_OWNER_POLICY = "policy"
    POLICY_OWNER_UNSPECIFIED = "unspecified"


class EquipmentInstance(ManagedObject):
    """This is EquipmentInstance class."""

    consts = EquipmentInstanceConsts()
    naming_props = set([u'id'])

    mo_meta = MoMeta("EquipmentInstance", "equipmentInstance", "inst-[id]", None, "InputOutput", 0x7f, [], ["admin", "ls-compute", "ls-config", "ls-server"], [u'equipmentChassisRequirement'], [u'cpmaintAck', u'equipmentChassisIssues'], [None])

    prop_meta = {
        "assign_state": MoPropertyMeta("assign_state", "assignState", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["assigned", "failed", "unassigned"], []), 
        "assoc_state": MoPropertyMeta("assoc_state", "assocState", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["associated", "associating", "disassociating", "failed", "unassociated"], []), 
        "child_action": MoPropertyMeta("child_action", "childAction", "string", None, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "config_qualifier": MoPropertyMeta("config_qualifier", "configQualifier", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|not-applicable|chassis-profile-not-supported|migration|non-interrupt-fsm-running|insufficient-resources|firmware-version-mismatch|physical-requirement|chassis-undiscovered|resource-ownership-conflict|chassis-unavailable|invalid-chassis-pack|missing-firmware-image|insufficient-power-budget),){0,13}(defaultValue|not-applicable|chassis-profile-not-supported|migration|non-interrupt-fsm-running|insufficient-resources|firmware-version-mismatch|physical-requirement|chassis-undiscovered|resource-ownership-conflict|chassis-unavailable|invalid-chassis-pack|missing-firmware-image|insufficient-power-budget){0,1}""", [], []), 
        "config_state": MoPropertyMeta("config_state", "configState", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["applied", "applying", "failed-to-apply", "not-applied"], []), 
        "descr": MoPropertyMeta("descr", "descr", "string", None, MoPropertyMeta.READ_WRITE, 0x2, None, None, r"""[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]{0,256}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", None, MoPropertyMeta.READ_ONLY, 0x4, 0, 256, None, [], []), 
        "flt_aggr": MoPropertyMeta("flt_aggr", "fltAggr", "ulong", None, MoPropertyMeta.INTERNAL, None, None, None, None, [], []), 
        "global_cp_dn": MoPropertyMeta("global_cp_dn", "globalCpDn", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 256, None, [], []), 
        "guid": MoPropertyMeta("guid", "guid", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "id": MoPropertyMeta("id", "id", "uint", None, MoPropertyMeta.NAMING, 0x8, None, None, None, [], []), 
        "int_id": MoPropertyMeta("int_id", "intId", "string", None, MoPropertyMeta.INTERNAL, None, None, None, None, ["none"], ["0-4294967295"]), 
        "mgmt_ip_addr": MoPropertyMeta("mgmt_ip_addr", "mgmtIpAddr", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 256, r"""((([0-9]){1,3}\.){3}[0-9]{1,3})""", [], []), 
        "name": MoPropertyMeta("name", "name", "string", None, MoPropertyMeta.READ_WRITE, 0x10, None, None, r"""[\-\.:_a-zA-Z0-9]{1,128}""", [], []), 
        "oper_state": MoPropertyMeta("oper_state", "operState", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["chassis-failed", "chassis-mismatch", "config", "config-failure", "decomissioning", "degraded", "diagnostics", "diagnostics-failed", "disabled", "discovery", "discovery-failed", "inaccessible", "indeterminate", "inoperable", "maintenance", "maintenance-failed", "ok", "operable", "pending-reassociation", "pending-reboot", "power-off", "removed", "restart", "test", "test-failed", "unassociated", "unconfig", "unconfig-failed"], []), 
        "phys_dn": MoPropertyMeta("phys_dn", "physDn", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 256, None, [], []), 
        "policy_level": MoPropertyMeta("policy_level", "policyLevel", "uint", None, MoPropertyMeta.READ_ONLY, None, None, None, None, [], []), 
        "policy_owner": MoPropertyMeta("policy_owner", "policyOwner", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, None, ["local", "pending-policy", "policy", "unspecified"], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", None, MoPropertyMeta.READ_ONLY, 0x20, 0, 256, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", None, MoPropertyMeta.READ_WRITE, 0x40, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "system_name": MoPropertyMeta("system_name", "systemName", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, r"""[\-\.:_a-zA-Z0-9]{0,16}""", [], []), 
        "templ_dn": MoPropertyMeta("templ_dn", "templDn", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 256, None, [], []), 
        "usr_lbl": MoPropertyMeta("usr_lbl", "usrLbl", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, r"""[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]{0,32}""", [], []), 
        "uuid": MoPropertyMeta("uuid", "uuid", "string", None, MoPropertyMeta.READ_ONLY, None, None, None, r"""(([0-9a-fA-F]){8}\-([0-9a-fA-F]){4}\-([0-9a-fA-F]){4}\-([0-9a-fA-F]){4}\-([0-9a-fA-F]){12})|0""", [], []), 
        "version": MoPropertyMeta("version", "version", "uint", None, MoPropertyMeta.READ_ONLY, None, None, None, None, [], []), 
    }

    prop_map = {
        "assignState": "assign_state", 
        "assocState": "assoc_state", 
        "childAction": "child_action", 
        "configQualifier": "config_qualifier", 
        "configState": "config_state", 
        "descr": "descr", 
        "dn": "dn", 
        "fltAggr": "flt_aggr", 
        "globalCpDn": "global_cp_dn", 
        "guid": "guid", 
        "id": "id", 
        "intId": "int_id", 
        "mgmtIpAddr": "mgmt_ip_addr", 
        "name": "name", 
        "operState": "oper_state", 
        "physDn": "phys_dn", 
        "policyLevel": "policy_level", 
        "policyOwner": "policy_owner", 
        "rn": "rn", 
        "status": "status", 
        "systemName": "system_name", 
        "templDn": "templ_dn", 
        "usrLbl": "usr_lbl", 
        "uuid": "uuid", 
        "version": "version", 
    }

    def __init__(self, parent_mo_or_dn, id, **kwargs):
        self._dirty_mask = 0
        self.id = id
        self.assign_state = None
        self.assoc_state = None
        self.child_action = None
        self.config_qualifier = None
        self.config_state = None
        self.descr = None
        self.flt_aggr = None
        self.global_cp_dn = None
        self.guid = None
        self.int_id = None
        self.mgmt_ip_addr = None
        self.name = None
        self.oper_state = None
        self.phys_dn = None
        self.policy_level = None
        self.policy_owner = None
        self.status = None
        self.system_name = None
        self.templ_dn = None
        self.usr_lbl = None
        self.uuid = None
        self.version = None

        ManagedObject.__init__(self, "EquipmentInstance", parent_mo_or_dn, **kwargs)

