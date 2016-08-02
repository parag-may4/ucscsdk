"""This module contains the general information for MessageEntry ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class MessageEntryConsts():
    SEVERITY_ALERT = "alert"
    SEVERITY_CRITICAL = "critical"
    SEVERITY_DEBUGGING = "debugging"
    SEVERITY_EMERGENCY = "emergency"
    SEVERITY_ERROR = "error"
    SEVERITY_INFORMATION = "information"
    SEVERITY_NOTIFICATION = "notification"
    SEVERITY_WARNING = "warning"


class MessageEntry(ManagedObject):
    """This is MessageEntry class."""

    consts = MessageEntryConsts()
    naming_props = set([u'id'])

    mo_meta = MoMeta("MessageEntry", "messageEntry", "entry-[id]", VersionMeta.Version141a, "InputOutput", 0x1f, [], ["admin"], [u'lsSPMeta', u'messageEp'], [], ["Get"])

    prop_meta = {
        "action_code": MoPropertyMeta("action_code", "actionCode", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "action_msg": MoPropertyMeta("action_msg", "actionMsg", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "action_values": MoPropertyMeta("action_values", "actionValues", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version141a, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, 0x2, 0, 256, None, [], []), 
        "error_code": MoPropertyMeta("error_code", "errorCode", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "error_msg": MoPropertyMeta("error_msg", "errorMsg", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "error_values": MoPropertyMeta("error_values", "errorValues", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "id": MoPropertyMeta("id", "id", "uint", VersionMeta.Version141a, MoPropertyMeta.NAMING, 0x4, None, None, None, [], []), 
        "iscsi_config_issues": MoPropertyMeta("iscsi_config_issues", "iscsiConfigIssues", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|not-applicable|static-target-mix|native-vlan|auto-target-auth|iscsi-config|missing-vlan|invalid-target-name|initiator-name|ip-addr-dhcp|init-target-passwd|auto-target-init|iscsi-initiator-ip-address|iqn-pool-name|vnic-name|no-luns|unclassified|init-identity|target-name|no-vlan-ip|invalid-mac|iscsi-cardinality|allowed-vlan|internal-cfg-error|auth-profile-same),){0,24}(defaultValue|not-applicable|static-target-mix|native-vlan|auto-target-auth|iscsi-config|missing-vlan|invalid-target-name|initiator-name|ip-addr-dhcp|init-target-passwd|auto-target-init|iscsi-initiator-ip-address|iqn-pool-name|vnic-name|no-luns|unclassified|init-identity|target-name|no-vlan-ip|invalid-mac|iscsi-cardinality|allowed-vlan|internal-cfg-error|auth-profile-same){0,1}""", [], []), 
        "issue": MoPropertyMeta("issue", "issue", "string", None, MoPropertyMeta.READ_ONLY, None, 0, 510, None, [], []), 
        "mo_dn": MoPropertyMeta("mo_dn", "moDn", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, 0, 256, None, [], []), 
        "network_config_issues": MoPropertyMeta("network_config_issues", "networkConfigIssues", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|not-applicable|network-feature-capability-mismatch|switch-virtual-if-capacity|conflicting-vlan-access|unsupported-usnic-config|named-vlan-inaccessible|unsupported-multicast-policy|permit-unresolved|unsupported-vmq-config|vlan-port-capacity|pinning-invalid),){0,11}(defaultValue|not-applicable|network-feature-capability-mismatch|switch-virtual-if-capacity|conflicting-vlan-access|unsupported-usnic-config|named-vlan-inaccessible|unsupported-multicast-policy|permit-unresolved|unsupported-vmq-config|vlan-port-capacity|pinning-invalid){0,1}""", [], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, 0x8, 0, 256, None, [], []), 
        "server_config_issues": MoPropertyMeta("server_config_issues", "serverConfigIssues", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|not-applicable|insufficient-power-budget|server-position-requirement|boot-configuration-unsupported|processor-type-bios-downgrade-restriction|unsupported-cimc-version-for-power-capping|compute-undiscovered|power-group-requirement|imgsec-policy-invalid|soft-pinning-vlan-mismatch|embedded-controller-not-supported|power-state-change|missing-firmware-image|resource-ownership-conflict|boot-order-pxe|vmedia-policy-unsupported|on-next-boot-unsupported|insufficient-resources|mac-address-assignment|remote-service-profile|server-feature-capability-mismatch|boot-order-jbod-image-path|boot-dev-no-support|incompat-bios-for-sriov-vnics|processor-requirement|provsrv-policy-invalid|cimc-downgrade-restriction|unsupported-vic-slot|board-controller-update-unsupported|non-interrupt-fsm-running|boot-order-san-image-path|bootip-policy-invalid|boot-policy-vmedia-invalid|server-type-bios-downgrade-restriction|memory-requirement|system-uuid-assignment|domain-requirement|qualified-pool-without-binding|boot-configuration-invalid|incompatible-bios-image|remote-policy|qos-policy-invalid|processor-type-cimc-downgrade-restriction|unsupported-bios-for-tpm|compute-unavailable|physical-requirement|hostimg-policy-invalid|vmedia-mount-config-invalid|server-type-cimc-downgrade-restriction|migration|wwnn-derivation-from-vhba|duplicate-address-conflict|unsupported-bios-for-vnic-cdn|boot-order-iscsi),){0,54}(defaultValue|not-applicable|insufficient-power-budget|server-position-requirement|boot-configuration-unsupported|processor-type-bios-downgrade-restriction|unsupported-cimc-version-for-power-capping|compute-undiscovered|power-group-requirement|imgsec-policy-invalid|soft-pinning-vlan-mismatch|embedded-controller-not-supported|power-state-change|missing-firmware-image|resource-ownership-conflict|boot-order-pxe|vmedia-policy-unsupported|on-next-boot-unsupported|insufficient-resources|mac-address-assignment|remote-service-profile|server-feature-capability-mismatch|boot-order-jbod-image-path|boot-dev-no-support|incompat-bios-for-sriov-vnics|processor-requirement|provsrv-policy-invalid|cimc-downgrade-restriction|unsupported-vic-slot|board-controller-update-unsupported|non-interrupt-fsm-running|boot-order-san-image-path|bootip-policy-invalid|boot-policy-vmedia-invalid|server-type-bios-downgrade-restriction|memory-requirement|system-uuid-assignment|domain-requirement|qualified-pool-without-binding|boot-configuration-invalid|incompatible-bios-image|remote-policy|qos-policy-invalid|processor-type-cimc-downgrade-restriction|unsupported-bios-for-tpm|compute-unavailable|physical-requirement|hostimg-policy-invalid|vmedia-mount-config-invalid|server-type-cimc-downgrade-restriction|migration|wwnn-derivation-from-vhba|duplicate-address-conflict|unsupported-bios-for-vnic-cdn|boot-order-iscsi){0,1}""", [], []), 
        "severity": MoPropertyMeta("severity", "severity", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, None, None, None, ["alert", "critical", "debugging", "emergency", "error", "information", "notification", "warning"], []), 
        "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version141a, MoPropertyMeta.READ_WRITE, 0x10, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "storage_config_issues": MoPropertyMeta("storage_config_issues", "storageConfigIssues", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|not-applicable|flexflash-metadata|unsupported-disk-controller-config|unsupported-expand-to-available|unsupported-use-remaining-disks|unsupported-strip-size-change|zone-capacity|duplicated-lun-name|unsupported-hotspare-change|unsupported-vd-modification|invalid-disk-slot-ownership|disk-role-mismatch|missing-raid-key|orphaned-lun-ref-missing|virtual-drive-access-denied|unsupported-disk-slot-zoning|destructive-local-disk-config|storage-feature-capability-mismatch|insufficient-disks|conflicting-lun-config|unsupported-global-hotspares|drive-cache-not-supported|unsupported-chassis-disk-zoning|flexflash-controller|unsupported-controller|invalid-storage-profile-binding|lun-in-use|disk-sharing-not-supported|incompatible-disk-types|storage-path-configuration-error|disk-type-mismatch|orphaned-lun-ref-access-denied|virtual-drive-deletion-in-progress|unsupported-partial-disk-group-zoning|virtual-drive-hidden-or-transport-ready|unsupported-raid-level|incomplete-lun-config|unsupported-order|embedded-controller-not-supported|unsupported-io-policy|incompatible-number-of-local-disks|flexflash-card|unsupported-destructive-change|invalid-local-lun-disk-policy-reference|set-proper-order|unsupported-chassis-spare-controller|wwnn-assignment|unsupported-orphan-lun-modification|unsupported-lun-map-modification|unsupported-write-cache-policy|invalid-zoning-virtual-drive-state|insufficient-storage-space|order-should-be-unique|virtual-drive-capacity|incompatible-raid-level|invalid-dzp-reference),){0,56}(defaultValue|not-applicable|flexflash-metadata|unsupported-disk-controller-config|unsupported-expand-to-available|unsupported-use-remaining-disks|unsupported-strip-size-change|zone-capacity|duplicated-lun-name|unsupported-hotspare-change|unsupported-vd-modification|invalid-disk-slot-ownership|disk-role-mismatch|missing-raid-key|orphaned-lun-ref-missing|virtual-drive-access-denied|unsupported-disk-slot-zoning|destructive-local-disk-config|storage-feature-capability-mismatch|insufficient-disks|conflicting-lun-config|unsupported-global-hotspares|drive-cache-not-supported|unsupported-chassis-disk-zoning|flexflash-controller|unsupported-controller|invalid-storage-profile-binding|lun-in-use|disk-sharing-not-supported|incompatible-disk-types|storage-path-configuration-error|disk-type-mismatch|orphaned-lun-ref-access-denied|virtual-drive-deletion-in-progress|unsupported-partial-disk-group-zoning|virtual-drive-hidden-or-transport-ready|unsupported-raid-level|incomplete-lun-config|unsupported-order|embedded-controller-not-supported|unsupported-io-policy|incompatible-number-of-local-disks|flexflash-card|unsupported-destructive-change|invalid-local-lun-disk-policy-reference|set-proper-order|unsupported-chassis-spare-controller|wwnn-assignment|unsupported-orphan-lun-modification|unsupported-lun-map-modification|unsupported-write-cache-policy|invalid-zoning-virtual-drive-state|insufficient-storage-space|order-should-be-unique|virtual-drive-capacity|incompatible-raid-level|invalid-dzp-reference){0,1}""", [], []), 
        "vnic_config_issues": MoPropertyMeta("vnic_config_issues", "vnicConfigIssues", "string", VersionMeta.Version141a, MoPropertyMeta.READ_ONLY, None, None, None, r"""((defaultValue|not-applicable|adaptor-protected-eth-capability|vif-resources-overprovisioned|ungrouped-domain|unsupported-nvgre|unsupported-adaptor-for-vnic-cdn|unresolved-remote-vlan-name|invalid-wwn|service-profile-virtualization-conflict|unsupported-roce-netflow|unsupported-vxlan-netflow|redundancy-vnicpair-not-in-sync|fcoe-capacity|wwpn-derivation-virtualized-port|unresolved-vlan-name|vnic-virtualization-netflow-conflict|unsupported-vxlan-usnic|unsupported-roce-properties|pinning-vlan-mismatch|adaptor-requirement|vnic-not-ha-ready|missing-ipv4-inband-mgmt-addr|unsupported-nvgre-dynamic-vnic|duplicate-vnic-cdn-name|unresolved-remote-vsan-name|mac-derivation-virtualized-port|vnic-virtualization-conflict|unsupported-roce|unsupported-nvgre-netflow|vnic-vlan-assignment-error|insufficient-vhba-capacity|inaccessible-vlan|unable-to-update-ucsm|soft-pinning-vlan-mismatch|unsupported-roce-usnic|unsupported-nvgre-vmq|connection-placement|vnic-vcon-provisioning-change|missing-ipv6-inband-mgmt-addr|unsupported-nvgre-usnic|insufficient-roce-resources|missing-primary-vlan|adaptor-fcoe-capability|vfc-vnic-pvlan-conflict|virtualization-not-supported|unsupported-vxlan|unsupported-roce-nvgre|unresolved-vsan-name|insufficient-vnic-capacity|unassociated-vlan|unsupported-roce-vmq|unsupported-roce-vxlan|unsupported-vxlan-vmq|redundancy-vnic-not-in-pair|dynamic-vf-vnic|wwpn-assignment|missing-ipv4-addr|unsupported-vxlan-dynamic-vnic|pinned-target-misconfig|unsupported-vmq-resources),){0,60}(defaultValue|not-applicable|adaptor-protected-eth-capability|vif-resources-overprovisioned|ungrouped-domain|unsupported-nvgre|unsupported-adaptor-for-vnic-cdn|unresolved-remote-vlan-name|invalid-wwn|service-profile-virtualization-conflict|unsupported-roce-netflow|unsupported-vxlan-netflow|redundancy-vnicpair-not-in-sync|fcoe-capacity|wwpn-derivation-virtualized-port|unresolved-vlan-name|vnic-virtualization-netflow-conflict|unsupported-vxlan-usnic|unsupported-roce-properties|pinning-vlan-mismatch|adaptor-requirement|vnic-not-ha-ready|missing-ipv4-inband-mgmt-addr|unsupported-nvgre-dynamic-vnic|duplicate-vnic-cdn-name|unresolved-remote-vsan-name|mac-derivation-virtualized-port|vnic-virtualization-conflict|unsupported-roce|unsupported-nvgre-netflow|vnic-vlan-assignment-error|insufficient-vhba-capacity|inaccessible-vlan|unable-to-update-ucsm|soft-pinning-vlan-mismatch|unsupported-roce-usnic|unsupported-nvgre-vmq|connection-placement|vnic-vcon-provisioning-change|missing-ipv6-inband-mgmt-addr|unsupported-nvgre-usnic|insufficient-roce-resources|missing-primary-vlan|adaptor-fcoe-capability|vfc-vnic-pvlan-conflict|virtualization-not-supported|unsupported-vxlan|unsupported-roce-nvgre|unresolved-vsan-name|insufficient-vnic-capacity|unassociated-vlan|unsupported-roce-vmq|unsupported-roce-vxlan|unsupported-vxlan-vmq|redundancy-vnic-not-in-pair|dynamic-vf-vnic|wwpn-assignment|missing-ipv4-addr|unsupported-vxlan-dynamic-vnic|pinned-target-misconfig|unsupported-vmq-resources){0,1}""", [], []), 
    }

    prop_map = {
        "actionCode": "action_code", 
        "actionMsg": "action_msg", 
        "actionValues": "action_values", 
        "childAction": "child_action", 
        "dn": "dn", 
        "errorCode": "error_code", 
        "errorMsg": "error_msg", 
        "errorValues": "error_values", 
        "id": "id", 
        "iscsiConfigIssues": "iscsi_config_issues", 
        "issue": "issue", 
        "moDn": "mo_dn", 
        "networkConfigIssues": "network_config_issues", 
        "rn": "rn", 
        "serverConfigIssues": "server_config_issues", 
        "severity": "severity", 
        "status": "status", 
        "storageConfigIssues": "storage_config_issues", 
        "vnicConfigIssues": "vnic_config_issues", 
    }

    def __init__(self, parent_mo_or_dn, id, **kwargs):
        self._dirty_mask = 0
        self.id = id
        self.action_code = None
        self.action_msg = None
        self.action_values = None
        self.child_action = None
        self.error_code = None
        self.error_msg = None
        self.error_values = None
        self.iscsi_config_issues = None
        self.issue = None
        self.mo_dn = None
        self.network_config_issues = None
        self.server_config_issues = None
        self.severity = None
        self.status = None
        self.storage_config_issues = None
        self.vnic_config_issues = None

        ManagedObject.__init__(self, "MessageEntry", parent_mo_or_dn, **kwargs)

