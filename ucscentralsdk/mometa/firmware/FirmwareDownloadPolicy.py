"""This module contains the general information for FirmwareDownloadPolicy ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class FirmwareDownloadPolicyConsts():
    ADMIN_EULASTATUS_FALSE = "false"
    ADMIN_EULASTATUS_NO = "no"
    ADMIN_EULASTATUS_TRUE = "true"
    ADMIN_EULASTATUS_YES = "yes"
    DOWNLOAD_INTERVAL_1DAY = "1day"
    DOWNLOAD_INTERVAL_1WEEK = "1week"
    DOWNLOAD_INTERVAL_2WEEK = "2week"
    DOWNLOAD_INTERVAL_ON_DEMAND = "on-demand"
    INT_ID_NONE = "none"
    POLICY_ADMIN_STATE_DISABLE = "disable"
    POLICY_ADMIN_STATE_ENABLE = "enable"
    POLICY_OWNER_LOCAL = "local"
    POLICY_OWNER_PENDING_POLICY = "pending-policy"
    POLICY_OWNER_POLICY = "policy"
    POLICY_OWNER_UNSPECIFIED = "unspecified"
    PROXY_PWD_SET_FALSE = "false"
    PROXY_PWD_SET_NO = "no"
    PROXY_PWD_SET_TRUE = "true"
    PROXY_PWD_SET_YES = "yes"
    PWD_SET_FALSE = "false"
    PWD_SET_NO = "no"
    PWD_SET_TRUE = "true"
    PWD_SET_YES = "yes"
    TYPE_CISCO = "Cisco"
    TYPE_LOCAL = "local"


class FirmwareDownloadPolicy(ManagedObject):
    """This is FirmwareDownloadPolicy class."""

    consts = FirmwareDownloadPolicyConsts()
    naming_props = set([u'type'])

    mo_meta = MoMeta("FirmwareDownloadPolicy", "firmwareDownloadPolicy", "dl-policy-[type]", VersionMeta.Version101a, "InputOutput", 0x3ffff, [], ["admin"], [u'firmwareSource', u'orgDomainGroup'], [u'faultInst'], ["Get", "Set"])

    prop_meta = {
        "admin_eula_status": MoPropertyMeta("admin_eula_status", "adminEULAStatus", "string", None, MoPropertyMeta.READ_WRITE, 0x2, None, None, None, ["false", "no", "true", "yes"], []), 
        "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version101a, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "descr": MoPropertyMeta("descr", "descr", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x4, None, None, r"""[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]{0,256}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, 0x8, 0, 256, None, [], []), 
        "download_interval": MoPropertyMeta("download_interval", "downloadInterval", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x10, None, None, None, ["1day", "1week", "2week", "on-demand"], []), 
        "enc_password": MoPropertyMeta("enc_password", "encPassword", "string", VersionMeta.Version111a, MoPropertyMeta.READ_WRITE, 0x20, None, None, None, [], []), 
        "enc_proxy_pwd": MoPropertyMeta("enc_proxy_pwd", "encProxyPwd", "string", VersionMeta.Version111a, MoPropertyMeta.READ_WRITE, 0x40, None, None, None, [], []), 
        "http_proxy": MoPropertyMeta("http_proxy", "httpProxy", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x80, None, None, r"""^([a-zA-Z0-9][a-zA-Z0-9_.@-]{0,63}(:[0-9]|:[1-9][0-9]|:[1-9][0-9][0-9]|:[1-9][0-9][0-9][0-9]|:[1-5][0-9][0-9][0-9][0-9]|:6[0-4][0-9][0-9][0-9]|:65[0-4][0-9][0-9]|:655[0-2][0-9]|:6553[0-5])?)?$""", [], []), 
        "http_url": MoPropertyMeta("http_url", "httpURL", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x100, 0, 510, None, [], []), 
        "int_id": MoPropertyMeta("int_id", "intId", "string", VersionMeta.Version101a, MoPropertyMeta.INTERNAL, None, None, None, None, ["none"], ["0-4294967295"]), 
        "name": MoPropertyMeta("name", "name", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x200, None, None, r"""[\-\.:_a-zA-Z0-9]{0,16}""", [], []), 
        "password": MoPropertyMeta("password", "password", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x400, 0, 64, None, [], []), 
        "policy_admin_state": MoPropertyMeta("policy_admin_state", "policyAdminState", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x800, None, None, None, ["disable", "enable"], []), 
        "policy_level": MoPropertyMeta("policy_level", "policyLevel", "uint", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, None, None, None, None, [], []), 
        "policy_owner": MoPropertyMeta("policy_owner", "policyOwner", "string", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, None, None, None, None, ["local", "pending-policy", "policy", "unspecified"], []), 
        "proxy_pwd": MoPropertyMeta("proxy_pwd", "proxyPwd", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x1000, 0, 64, None, [], []), 
        "proxy_pwd_set": MoPropertyMeta("proxy_pwd_set", "proxyPwdSet", "string", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, None, None, None, None, ["false", "no", "true", "yes"], []), 
        "proxy_user": MoPropertyMeta("proxy_user", "proxyUser", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x2000, None, None, r"""^([a-zA-Z0-9_.@-]{0,64})?$""", [], []), 
        "pwd_set": MoPropertyMeta("pwd_set", "pwdSet", "string", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, None, None, None, None, ["false", "no", "true", "yes"], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, 0x4000, 0, 256, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x8000, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "type": MoPropertyMeta("type", "type", "string", VersionMeta.Version101a, MoPropertyMeta.NAMING, 0x10000, None, None, None, ["Cisco", "local"], []), 
        "username": MoPropertyMeta("username", "username", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x20000, None, None, r"""^([a-zA-Z0-9_.@-]{0,64})?$""", [], []), 
    }

    prop_map = {
        "adminEULAStatus": "admin_eula_status", 
        "childAction": "child_action", 
        "descr": "descr", 
        "dn": "dn", 
        "downloadInterval": "download_interval", 
        "encPassword": "enc_password", 
        "encProxyPwd": "enc_proxy_pwd", 
        "httpProxy": "http_proxy", 
        "httpURL": "http_url", 
        "intId": "int_id", 
        "name": "name", 
        "password": "password", 
        "policyAdminState": "policy_admin_state", 
        "policyLevel": "policy_level", 
        "policyOwner": "policy_owner", 
        "proxyPwd": "proxy_pwd", 
        "proxyPwdSet": "proxy_pwd_set", 
        "proxyUser": "proxy_user", 
        "pwdSet": "pwd_set", 
        "rn": "rn", 
        "status": "status", 
        "type": "type", 
        "username": "username", 
    }

    def __init__(self, parent_mo_or_dn, type, **kwargs):
        self._dirty_mask = 0
        self.type = type
        self.admin_eula_status = None
        self.child_action = None
        self.descr = None
        self.download_interval = None
        self.enc_password = None
        self.enc_proxy_pwd = None
        self.http_proxy = None
        self.http_url = None
        self.int_id = None
        self.name = None
        self.password = None
        self.policy_admin_state = None
        self.policy_level = None
        self.policy_owner = None
        self.proxy_pwd = None
        self.proxy_pwd_set = None
        self.proxy_user = None
        self.pwd_set = None
        self.status = None
        self.username = None

        ManagedObject.__init__(self, "FirmwareDownloadPolicy", parent_mo_or_dn, **kwargs)

