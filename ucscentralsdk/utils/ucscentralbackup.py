# Copyright 2013 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains APIs to facilitate UcsCentral backup and import
"""

import os
import platform
import time
import datetime
import logging
from ..ucscentralexception import UcsCentralValidationException, \
    UcsCentralWarning, \
    UcsCentralOperationError

log = logging.getLogger('ucscentral')


ucscentral_base_dn = "org-root/deviceprofile-default"


def _validate_remote_host_args(protocol, hostname, username, password):
    if not protocol:
        raise UcsCentralValidationException("Missing protocol argument")
    if not hostname:
        raise UcsCentralValidationException("Missing hostname argument")
    if protocol == 'tftp':
        return

    if not username:
        raise UcsCentralValidationException("Missing username argument")
    if not password:
        raise UcsCentralValidationException("Missing password argument")


def _backup(handle, file_dir, file_name, timeout=600,
            remote_enabled=False, protocol=None,
            hostname="localhost", username=None, password="",
            remove_from_ucscentral=False,
            preserve_pooled_values=False):
    """
    _backup internal method helps create UcsCentral full-state backup and
    download it locally or to remote location.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download backup file to
        file_name (str): name for the backup file
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.
        remote_enabled (boolean): True if Remote backup is enabled
                                  False - by default
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        username (str): Username for remote backup
        password (str): Password for remote backup
        remove_from_ucscentral (boolean): True/False, False - by default
        preserve_pooled_values (boolean): True/False, False - by default

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_backup.tgz"\n
        _backup(handle, file_dir=file_dir, file_name=file_name)\n

        _backup(handle, file_dir=file_dir, file_name=file_name,
                remote_enabled=True, protocol='scp',hostname='192.168.1.1',
                username='admin',password='password')\n

    """
    from ..mometa.mgmt.MgmtBackup import MgmtBackup, MgmtBackupConsts
    from ..mometa.top.TopSystem import TopSystem
    from .ucscentralfirmware import is_local_download_supported

    backup_type = "full-state"
    preserve_pooled_values = False

    if not file_dir:
        raise UcsCentralValidationException("Missing file_dir argument")
    if not file_name:
        raise UcsCentralValidationException("Missing file_name argument")

    top_system = TopSystem()

    if remote_enabled:
        _validate_remote_host_args(protocol, hostname, username, password)
        if (not file_name.endswith('.tgz')):
            raise UcsCentralValidationException(
                "file_name must be .tgz format")

        file_path = os.path.join(file_dir, file_name)
        mgmt_backup = MgmtBackup(
                parent_mo_or_dn=top_system,
                hostname=hostname,
                admin_state=MgmtBackupConsts.ADMIN_STATE_ENABLED,
                proto=protocol,
                type=backup_type,
                remote_file=file_path,
                user=username,
                pwd=password)
    else:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file_string = platform.node().lower() \
            + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "/" + file_string + "_" + backup_type + "_backup.tgz"

        mgmt_backup = MgmtBackup(
                parent_mo_or_dn=top_system,
                hostname=hostname,
                admin_state=MgmtBackupConsts.ADMIN_STATE_ENABLED,
                proto=MgmtBackupConsts.PROTO_HTTP,
                type=backup_type,
                remote_file=file_path)

    if preserve_pooled_values:
        mgmt_backup.preserve_pooled_values = \
            MgmtBackupConsts.PRESERVE_POOLED_VALUES_YES
    else:
        mgmt_backup.preserve_pooled_values = \
            MgmtBackupConsts.PRESERVE_POOLED_VALUES_NO

    handle.add_mo(mgmt_backup, modify_present=True)
    handle.commit()

    mgmt_backup = handle.query_dn(dn=mgmt_backup.dn)
    admin_state_temp = mgmt_backup.admin_state
    # Checking for the backup to compete.
    duration = timeout
    poll_interval = 2

    log.debug("Starting Backup ")
    while True:
        mgmt_backup = handle.query_dn(dn=mgmt_backup.dn)
        admin_state_temp = mgmt_backup.admin_state

        # Break condition:- if state id disabled then break
        if admin_state_temp == MgmtBackupConsts.ADMIN_STATE_DISABLED:
            break

        time.sleep(min(duration, poll_interval))
        duration = max(0, (duration - poll_interval))
        if duration == 0:
            handle.remove_mo(mgmt_backup)
            handle.commit()
            raise UcsCentralOperationError(
                  "Backup UcsCentral", " operation timed out")

    # download backup
    log.debug("Backup done")

    if not remote_enabled:
        file_source = "backupfile" + file_path
        if is_local_download_supported(handle):
            try:
                log.debug("Starting Download ")
                handle.file_download(url_suffix=file_source,
                                     file_dir=file_dir,
                                     file_name=file_name)
            except Exception as err:
                UcsCentralWarning(str(err))
                handle.remove_mo(mgmt_backup)
                handle.commit()
                raise UcsCentralOperationError(
                      "Download backup", "download failed")
        else:
            log.error("Local download not supported from sdk for this "
                      "version of UcsCentral, skipping it")

    if remove_from_ucscentral:
        # remove backup from ucscentral
        log.debug("Removing backup from UcsCentral")
        handle.remove_mo(mgmt_backup)
        handle.commit()


def backup_local(handle, file_dir, file_name, preserve_pooled_values=False,
                 remove_from_ucscentral=False, timeout=600):
    """
    backup_local helps create UcsCentral full-state backup and dowload it
    locally.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download ucs backup file to
        file_name (str): name for the backup file
        preserve_pooled_values (boolean): True/False, False - by default
        remove_from_ucscentral (boolean): True/False, False - by default
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_backup.tgz"\n
        backup_local(handle, file_dir=test_support, file_name=file_name)\n
    """

    _backup(handle, file_dir=file_dir, file_name=file_name,
            remote_enabled=False, hostname="localhost",
            preserve_pooled_values=preserve_pooled_values,
            remove_from_ucscentral=remove_from_ucscentral,
            timeout=timeout)


def backup_remote(handle, file_dir, file_name, hostname,
                  protocol="scp", username=None, password="",
                  preserve_pooled_values=False,
                  remove_from_ucscentral=False,
                  timeout=600):
    """
    backup_remote helps create and download UcsCentral full-state backup to
    remote location.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download ucs backup file to
        file_name (str): name for the backup file
                         (supported file extension '.tgz')
        hostname (str): Hostname/IP for the remote backup
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        username (str): Username for remote backup
        password (str): Password for remote backup
        preserve_pooled_values (boolean): True/False, False - by default
        remove_from_ucscentral (boolean): True/False, False - by default
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_backup.tgz"\n
        backup_remote(handle, file_dir=file_dir, file_name=file_name,
                      protocol='scp',hostname='192.168.1.1',
                      username='admin',password='password')\n

    """
    _backup(handle, file_dir=file_dir, file_name=file_name,
            remote_enabled=True,
            hostname=hostname, protocol=protocol,
            username=username, password=password,
            preserve_pooled_values=preserve_pooled_values,
            remove_from_ucscentral=remove_from_ucscentral,
            timeout=timeout)


def _export_config(handle, file_dir, file_name, timeout=600,
                   remote_enabled=False, protocol=None,
                   hostname="localhost", username=None, password="",
                   remove_from_ucscentral=False,
                   preserve_pooled_values=False):
    """
    _export_config internal method helps export UcsCentral config-all backup
    and download it locally or to remote location.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download ucs backup file to
        file_name (str): name for the backup file
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.
        remote_enabled (boolean): True if Remote backup is enabled
                                  False - by default
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        username (str): Username for remote backup
        password (str): Password for remote backup
        remove_from_ucscentral (boolean): True/False, False - by default
        preserve_pooled_values (boolean): True/False, False - by default

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "export_config.tgz"\n
        _export_config(handle, file_dir=test_support,
                       file_name=file_name)\n

        _export_config(handle, file_dir=test_support,
                    file_name=file_name,remote_enabled=True,
                    protocol='scp',hostname='192.168.1.1',
                    username='admin',password='password')\n

    """
    from ..mometa.mgmt.MgmtDataExporter import MgmtDataExporter, \
        MgmtDataExporterConsts
    from ..mometa.top.TopSystem import TopSystem
    from .ucscentralfirmware import is_local_download_supported

    backup_type = "config-all"
    if not file_dir:
        raise UcsCentralValidationException("Missing file_dir argument")
    if not file_name:
        raise UcsCentralValidationException("Missing file_name argument")

    top_system = TopSystem()

    if remote_enabled:
        _validate_remote_host_args(protocol, hostname, username, password)
        if (not file_name.endswith('.tgz')):
            raise UcsCentralValidationException(
                "file_name must be .tgz format")

        file_path = os.path.join(file_dir, file_name)
        mgmt_export = MgmtDataExporter(
                parent_mo_or_dn=top_system,
                hostname=hostname,
                admin_state=MgmtDataExporterConsts.ADMIN_STATE_ENABLED,
                proto=protocol,
                type=backup_type,
                remote_file=file_path,
                user=username,
                pwd=password)
    else:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file_string = platform.node().lower() \
            + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "/" + file_string + "_" + backup_type + "_backup.tgz"

        mgmt_export = MgmtDataExporter(
                parent_mo_or_dn=top_system,
                hostname=hostname,
                admin_state=MgmtDataExporterConsts.ADMIN_STATE_ENABLED,
                proto=MgmtDataExporterConsts.PROTO_HTTP,
                type=backup_type,
                remote_file=file_path)

    if preserve_pooled_values:
        mgmt_export.preserve_pooled_values = \
            MgmtDataExporterConsts.PRESERVE_POOLED_VALUES_YES
    else:
        mgmt_export.preserve_pooled_values = \
            MgmtDataExporterConsts.PRESERVE_POOLED_VALUES_NO

    handle.add_mo(mgmt_export, modify_present=True)
    handle.commit()

    mgmt_export = handle.query_dn(dn=mgmt_export.dn)
    admin_state_temp = mgmt_export.admin_state
    log.debug("Starting export config")
    # Checking for the backup to compete.
    duration = timeout
    poll_interval = 2

    while True:
        mgmt_export = handle.query_dn(dn=mgmt_export.dn)
        admin_state_temp = mgmt_export.admin_state

        # Break condition:- if state id disabled then break
        if admin_state_temp == MgmtDataExporterConsts.ADMIN_STATE_DISABLED:
            break

        time.sleep(min(duration, poll_interval))
        duration = max(0, (duration - poll_interval))
        if duration == 0:
            handle.remove_mo(mgmt_export)
            handle.commit()
            raise UcsCentralOperationError(
                "Config Export UcsCentral", "operation timed out")

    # download backup
    log.debug("Config exported")

    if not remote_enabled:
        file_source = "backupfile" + file_path
        if is_local_download_supported(handle):
            try:
                log.debug("Starting download")
                handle.file_download(url_suffix=file_source,
                                     file_dir=file_dir,
                                     file_name=file_name)
            except Exception as err:
                UcsCentralWarning(str(err))
                handle.remove_mo(mgmt_export)
                handle.commit()
                raise UcsCentralOperationError(
                    "Download of export_config", "download failed")
        else:
            log.error("Local download not supported from sdk for this "
                      "version of UcsCentral, skipping it")

    if remove_from_ucscentral:
        # remove backup from ucscentral
        log.debug("Removing export config from UcsCentral")
        handle.remove_mo(mgmt_export)
        handle.commit()


def export_config_local(handle, file_dir, file_name,
                        preserve_pooled_values=False,
                        remove_from_ucscentral=False,
                        timeout=600):
    """
    export_config_local helps export UcsCentral config-all backup and download
    it locally.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download ucs backup file to
        file_name (str): name for the backup file
        preserve_pooled_values (boolean): True/False, False - by default
        remove_from_ucscentral (boolean): True/False, False - by default
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "export_config.tgz"\n
        export_config_ucscentral(handle, file_dir=file_dir,
                                         file_name=file_name)\n
    """

    _export_config(handle, file_dir=file_dir, file_name=file_name,
                   remote_enabled=False, hostname="localhost",
                   preserve_pooled_values=preserve_pooled_values,
                   remove_from_ucscentral=remove_from_ucscentral,
                   timeout=timeout)


def export_config_remote(handle, file_dir, file_name, hostname,
                         protocol="scp", username=None, password="",
                         preserve_pooled_values=False,
                         remove_from_ucscentral=False,
                         timeout=600):
    """
    export_config_remote helps export UcsCentral config-all backup and
    download it to remote location.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download ucs backup file to
        file_name (str): name for the backup file
                         (supported file extension '.tgz')
        hostname (str): Hostname/IP for the remote backup
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        username (str): Username for remote backup
        password (str): Password for remote backup
        preserve_pooled_values (boolean): True/False, False - by default
        remove_from_ucscentral (boolean): True/False, False - by default
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "export_config.tgz"\n

        export_config_remote(handle, file_dir=file_dir,
                    file_name=file_name,
                    protocol='scp',hostname='192.168.1.1',
                    username='admin',password='password')\n

    """
    _export_config(handle, file_dir=file_dir, file_name=file_name,
                   remote_enabled=True,
                   hostname=hostname, protocol=protocol,
                   username=username, password=password,
                   preserve_pooled_values=preserve_pooled_values,
                   remove_from_ucscentral=remove_from_ucscentral,
                   timeout=timeout)


def _fail_and_remove_domain_backup(handle, backup_status_mo, err):
    if backup_status_mo:
        handle.remove_mo(backup_status_mo)
        handle.commit(dme="resource-mgr")
    raise UcsCentralOperationError("Domain backup/export_config", err)


def _backup_or_exportconfig_domain(handle, backup_type, file_dir, file_name,
                                   domain_ip, domain_name, hostname,
                                   preserve_pooled_values, protocol,
                                   username, password, timeout):
    """
    This internal function helps create domain full_state backup or export
    config to remote location
    Note: This is internal function, should use either backup_domain or
    backup_export_config
    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download ucs backup file to
        file_name (str): name for the backup file
                         (supported file extension is '.tgz')
        backup_type (str): Either full-state or config-all.
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.
        domain_ip(str): IP of domain, set 'None' if domain_name is valid
        domain_name(str): Domain name, valid only if domain_ip is None
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        username (str): Username for remote backup
        password (str): Password for remote backup
        preserve_pooled_values (boolean): True/False,
                                          False - by default

    """
    from ..mometa.mgmt.MgmtBackupOperation import MgmtBackupOperation, \
        MgmtBackupOperationConsts
    from ..mometa.mgmt.MgmtBackup import MgmtBackupConsts
    from .ucscentraldomain import get_domain, _is_domain_available

    preserve_pooled_values = False

    if not file_dir:
        raise UcsCentralValidationException("Missing file_dir argument")
    if not file_name:
        raise UcsCentralValidationException("Missing file_name argument")
    if not domain_ip:
        raise UcsCentralValidationException("Missing domain_ip argument")

    if backup_type == 'full-state':
        if (not file_name.endswith('.tgz')):
            raise UcsCentralValidationException(
                "file_name must be .tgz format")
    elif backup_type == 'config-all':
        if (not file_name.endswith('.xml')):
            raise UcsCentralValidationException(
                "file_name must be .xml format")
    _validate_remote_host_args(protocol, hostname, username, password)

    domain = get_domain(handle, domain_ip, domain_name)

    if _is_domain_available(handle, domain.id):
        domain_dn = domain.dn
    else:
        raise UcsCentralOperationError("Backup or Export_config",
                                       "Domain with IP %s or name %s not "
                                       "registered or lost visibility "
                                       "with UcsCentral" %
                                       (domain_ip, domain_name))

    file_path = os.path.join(file_dir, file_name)

    mgmt_backup = MgmtBackupOperation(
            parent_mo_or_dn=domain_dn,
            hostname=hostname,
            admin_state=MgmtBackupOperationConsts.ADMIN_STATE_ENABLED,
            proto=protocol,
            type=backup_type,
            remote_file=file_path,
            user=username,
            pwd=password)
    if preserve_pooled_values:
        mgmt_backup.preserve_pooled_values = \
            MgmtBackupOperationConsts.PRESERVE_POOLED_VALUES_YES
    else:
        mgmt_backup.preserve_pooled_values = \
            MgmtBackupOperationConsts.PRESERVE_POOLED_VALUES_NO

    handle.set_mo(mgmt_backup)
    handle.commit()

    log.debug("Triggering Domain Backup ")
    duration = 30
    poll_interval = 2
    backup_status_dn = "extpol/reg/clients/client-" + \
        domain.id + "/backup-" + hostname
    while True:
        backup_status = handle.query_dn(
            dn=backup_status_dn, dme="resource-mgr")
        if backup_status is not None:
            break

        time.sleep(min(duration, poll_interval))
        duration = max(0, (duration - poll_interval))
        if duration == 0:
            raise UcsCentralOperationError(
                "Backup or export config of domain", "not triggered")

    log.debug("Domain Backup Triggered")

    # Checking for the backup to become available.
    log.debug("Waiting for Domain Backup to become available")
    duration = timeout
    poll_interval = 5

    while True:
        backup_status = handle.query_dn(backup_status_dn, dme="resource-mgr")
        if backup_status.over_all_status == \
                MgmtBackupConsts.OVER_ALL_STATUS_ALL_SUCCESS:
            break
        if backup_status.over_all_status != \
                MgmtBackupConsts.OVER_ALL_STATUS_WORK_IN_PROGRESS:
            _fail_and_remove_domain_backup(
                handle, backup_status, 'operation failed')
        time.sleep(min(duration, poll_interval))
        duration = max(0, (duration - poll_interval))
        if duration == 0:
            _fail_and_remove_domain_backup(
                handle, backup_status, 'operation timed out')

    log.debug("Domain backup is available")


def backup_domain_remote(handle, file_dir, file_name,
                         domain_ip,  protocol, hostname,
                         username=None, password="",
                         domain_name=None, preserve_pooled_values=False,
                         timeout=600):
    """
    backup_domain_remote  helps create domain full_state backup and download
    it to remote location.
    Note: Domain backup will always be remote backup
    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download ucs backup file to
        file_name (str): name for the backup file
                         (supported file extension is '.tgz')
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.
        domain_ip(str): IP of domain, set 'None' if domain_name is valid
        domain_name(str): Domain name, valid only if domain_ip is None
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        username (str): Username for remote backup
        password (str): Password for remote backup
        preserve_pooled_values (boolean): True/False,
                                          False - by default

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_backup.tgz"\n

        backup_domain_remote(handle, file_dir=file_dir, file_name=file_name,
                    domain_ip='10.10.10.1', protocol='scp',
                    hostname='192.168.1.1',
                    username='admin',password='password')\n

    """
    backup_type = "full-state"
    return _backup_or_exportconfig_domain(handle, backup_type, file_dir,
                                          file_name, domain_ip, domain_name,
                                          hostname, preserve_pooled_values,
                                          protocol, username, password,
                                          timeout)


def export_config_domain_remote(handle, file_dir, file_name,
                                domain_ip, hostname,  protocol,
                                username=None, password="",
                                domain_name=None, preserve_pooled_values=False,
                                timeout=600):
    """
    export_config_domain_remote helps create domain export config and download
    it to remote location.
    Note: Domain export export config will always be remote export

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        file_dir (str): directory to download ucs backup file to
        file_name (str): name for the backup file
                         (supported file extension is '.xml')
        timeout (number) : time in seconds for which method waits
                              for the backUp file to generate before it exits.
        domain_ip(str): IP of domain, set 'None' if domain_name is valid
        domain_name(str): Domain name, valid only if domain_ip is None
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        username (str): Username for remote backup
        password (str): Password for remote backup
        preserve_pooled_values (boolean): True/False,
                                          False - by default

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_backup.xml"\n
        export_config_domain(handle, file_dir=test_support,
                    file_name=file_name,
                    username='admin', password='password',
                    domain_ip='10.10.10.1', protocol='scp',
                    hostname='192.168.1.1')
    """
    backup_type = "config-all"
    return _backup_or_exportconfig_domain(handle, backup_type, file_dir,
                                          file_name, domain_ip, domain_name,
                                          hostname, preserve_pooled_values,
                                          protocol, username, password,
                                          timeout)


def _is_backup_file_on_server(handle, hostname_str, backup_file):

    backup_path_str = "/" + hostname_str + "/cfg-backups"
    filter_str = '(file_path, %s, type="eq")' % backup_path_str

    backups = handle.query_classid(
        class_id='ConfigBackup', filter_str=filter_str)

    for backup in backups:
        if backup.file_name == backup_file:
            log.debug("Backup file '%s' exist on ucscentral" % backup_file)
            return True
    return False


def _import_config(handle, file_name, file_location="ucscentral",
                   file_dir=None, merge=True, protocol=None,
                   hostname="localhost",
                   username=None, password="", timeout=120):
    """
    This internal method imports a UcsCentral config from local, remote or
    ucscentral

    Args:
        handle (UcsCentralHandle): connection handle
        file_name (str): backup file name to be imported
        file_location (str): file location where the config file is, it can be:
                             ['ucscentral','local','remote']
        file_dir (str): directory containing ucscentral backup file,
                        used only for import from local or remote
        merge (boolean): True/False, specifies whether to merge the backup
                        config with the existing UCS Central configuration

        protocol (str): Transfer protocol for remote import
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote import
        username (str): Username for remote import
        password (str): Password for remote import
        timeout (number) : time in seconds for which method waits for
                                  import operation success before timing out

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_export.tgz"\n
        import from ucscentral:
        _import_config(handle, file_name=file_name,
                       file_location="ucscentral")

        import from local:
        _import_config(handle, file_name=file_name,
                       file_location="local",
                       file_dir=file_dir,
                       merge=True)\n

        import from remote:
        _import_config(handle, file_name=file_name,
                       file_location="remote",
                       file_dir=file_dir
                       protocol='scp',hostname='192.168.1.1',
                       username='admin',password='password')\n

    """

    from ..mometa.top.TopSystem import TopSystem
    from ..mometa.mgmt.MgmtDataImporter import MgmtDataImporter, \
        MgmtDataImporterConsts

    if not file_name:
        raise UcsCentralValidationException("Missing file_name argument")

    if file_location != "ucscentral":
        if not file_dir:
            raise UcsCentralValidationException("Missing file_dir argument")

    if (not file_name.endswith('.tgz')):
        raise UcsCentralValidationException("file_name must be .tgz format")

    top_system = TopSystem()

    if file_location == "remote":
        file_path = os.path.join(file_dir, file_name)
        _validate_remote_host_args(protocol, hostname, username, password)
        mgmt_importer = MgmtDataImporter(
            parent_mo_or_dn=top_system,
            hostname=hostname,
            remote_file=file_path,
            proto=protocol,
            user=username,
            pwd=password,
            admin_state=MgmtDataImporterConsts.ADMIN_STATE_ENABLED)

    elif file_location == "local":
        file_path = os.path.join(file_dir, file_name)
        if not os.path.exists(file_path):
            raise UcsCentralOperationError("Import config",
                                           "Backup File '%s' not found" %
                                           file_path)
        mgmt_importer = MgmtDataImporter(
            parent_mo_or_dn=top_system,
            hostname="localhost",
            remote_file='/' + file_name,
            proto=MgmtDataImporterConsts.PROTO_HTTP,
            admin_state=MgmtDataImporterConsts.ADMIN_STATE_ENABLED)

    elif file_location == "ucscentral":
        if not _is_backup_file_on_server(handle, "ucs-central", file_name):
            raise UcsCentralOperationError("Import config",
                                           "Backup File '%s' not found "
                                           "on ucscentral" % file_name)
        mgmt_importer = MgmtDataImporter(
            parent_mo_or_dn=top_system,
            hostname="localhost",
            remote_file='/ucs-central/cfg-backups/' + file_name,
            proto=MgmtDataImporterConsts.PROTO_TFTP,
            admin_state=MgmtDataImporterConsts.ADMIN_STATE_ENABLED)

    else:
        raise UcsCentralOperationError(
                "Import config",
                "Invalid file_location argument."
                "It must be either ucscentral,local or remote")

    if merge:
        mgmt_importer.action = MgmtDataImporterConsts.ACTION_MERGE
    else:
        mgmt_importer.action = MgmtDataImporterConsts.ACTION_REPLACE

    if file_location == "local":
        try:
            log.debug("Start uploading config")
            uri_suffix = "operations/file-%s/importconfig.txt?Cookie=%s" % (
                         file_name, handle.cookie)
            handle.file_upload(url_suffix=uri_suffix,
                               file_dir=file_dir,
                               file_name=file_name)

        except Exception as err:
            UcsCentralWarning(str(err))
            raise UcsCentralOperationError("Upload config", "upload failed")

    handle.add_mo(mgmt_importer, modify_present=True)
    handle.commit()

    duration = timeout
    poll_interval = 2
    log.debug("Importing ucscentral config")
    while True:
        mgmt_importer = handle.query_dn(dn=mgmt_importer.dn)
        admin_state = mgmt_importer.admin_state

        # Break condition:- if state id disabled then break
        if admin_state == MgmtDataImporterConsts.ADMIN_STATE_DISABLED:
            break

        time.sleep(min(duration, poll_interval))
        duration = max(0, (duration - poll_interval))
        if duration == 0:
            raise UcsCentralOperationError(
                  "Import config", "operation timed out")

    if mgmt_importer.over_all_status != \
            MgmtDataImporterConsts.OVER_ALL_STATUS_ALL_SUCCESS:
            raise UcsCentralOperationError(
                  "Import config",
                  ("operational status %s " % mgmt_importer.over_all_status))

    log.debug("Import config to ucscentral was successfull")
    return mgmt_importer


def import_config_ucscentral(handle, file_name, merge=True,
                             timeout=120):
    """
    import_config_ucscentral imports exisiting UcsCentral config ie.available
    on UcsCentral(taken via schedule_export_config) to the UcsCentral

    Args:
        handle (UcsCentralHandle): connection handle
        file_name (str): backup file name to be imported
        merge (boolean): True/False, specifies whether to merge the backup
                        config with the existing UCS Central configuration
        timeout (number) : time in seconds for which method waits for
                                  import operation success before timing out

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_export.tgz"\n
        import from ucscentral:
        import_config_ucscentral(handle, file_name=file_name)
    """
    _import_config(handle, file_name=file_name, merge=merge,
                   file_location="ucscentral",
                   hostname="localhost",
                   timeout=timeout)


def import_config_local(handle, file_dir, file_name, merge=True,
                        timeout=120):
    """
    import_config_ucscentral imports UcsCentral config available locally to
    UcsCentral

    Args:
        handle (UcsCentralHandle): connection handle
        file_dir (str): directory containing ucscentral backup file,
        file_name (str): backup file name to be imported
        merge (boolean): True/False, specifies whether to merge the backup
                        config with the existing UCS Central configuration
        timeout (number) : time in seconds for which method waits for
                                  import operation success before timing out

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_export.tgz"\n

        import from local:
        import_config_local(handle, file_name=file_name,
                            file_dir=file_dir,
                            merge=True)\n

    """
    _import_config(handle, file_name=file_name, file_dir=file_dir, merge=merge,
                   file_location="local",
                   hostname="localhost",
                   timeout=timeout)


def import_config_remote(handle, file_dir, file_name, hostname,
                         merge=True,
                         protocol="scp",
                         username=None, password="",
                         timeout=120):
    """
    import_config_remote imports UcsCentral config from remote location to
    UcsCentral

    Args:
        handle (UcsCentralHandle): connection handle
        file_dir (str): directory containing ucscentral backup file,
        file_name (str): backup file name to be imported
        hostname (str): Hostname/IP for the remote import
        merge (boolean): True/False, specifies whether to merge the backup
                        config with the existing UCS Central configuration
        protocol (str): Transfer protocol for remote import
                        ['ftp','sftp','tftp','scp']
        username (str): Username for remote import
        password (str): Password for remote import
        timeout (number) : time in seconds for which method waits for
                                  import operation success before timing out

    Example:
        file_dir = "/home/user/backup"\n
        file_name = "config_export.tgz"\n

        import from remote:
        import_config_remote(handle, file_name=file_name,
                             file_dir=file_dir
                             protocol='scp',hostname='192.168.1.1',
                             username='admin',password='password')\n

    """
    _import_config(handle, file_name=file_name, file_dir=file_dir, merge=merge,
                   file_location="remote",
                   protocol=protocol, hostname=hostname,
                   username=username, password=password,
                   timeout=timeout)


def import_config_domain(handle, to_domain_ip, from_domain_ip, config_file,
                         merge=True,
                         to_domain_name=None, from_domain_name=None,
                         timeout=120):
    """
    This operation imports UcsCentral Domain's config created earlier via
    schedule backup of the same or other Domains.
    Note: Only config-all backup on UcsCentral are available for import, local
    or remote import is not supported for domain

    Args:
        handle (UcsCentralHandle): connection handle
        to_domain_ip(str): IP of domain To which you want to import
                           set 'None' if domain_name is valid
        from_domain_ip(str): IP of domain From which you want to import
                             set 'None' if domain_name is valid
        config_file(str): From domain's config file which you want to import
        merge (boolean): True/False, specifies whether to merge the backup
                         config with the existing domain configuration
        to_domain_name(str): to domain name, valid only if to_domain_ip is None
        from_domain_name(str): from domain name, valid only if
                               from_domain_ip is None
        timeout (number) : time in seconds for which method waits for
                                  import operation success before timing out

    Example:
        import_config_domain(handle, to_domain_ip="10.10.10.100",
                             from_domain_ip="192.168.1.1",
                             config_file="all-cfg.1.tgz")\n

    """

    from ..mometa.mgmt.MgmtImporter import MgmtImporter, MgmtImporterConsts
    from .ucscentraldomain import get_domain, _is_domain_available

    to_domain = get_domain(handle, to_domain_ip, to_domain_name)

    if not _is_domain_available(handle, to_domain.id):
        raise UcsCentralOperationError("Import config domain",
                                       "Domain with IP %s or name %s not "
                                       "registered or lost visibility "
                                       "with UcsCentral" %
                                       (to_domain_ip, to_domain_name))

    from_domain = get_domain(handle, from_domain_ip, from_domain_name)

    if not _is_domain_available(handle, from_domain.id):
        raise UcsCentralOperationError("Import config domain",
                                       "Domain with IP %s or name %s not "
                                       "registered or lost visibility "
                                       "with UcsCentral" %
                                       (from_domain_ip, from_domain_name))

    if not _is_backup_file_on_server(handle, from_domain.address, config_file):
        raise UcsCentralOperationError("Import config domain",
                                       "Backup File '%s' not found "
                                       "on ucscentral" % config_file)

    filter_str = '(connector_id, %s, type="eq")' % to_domain.id

    consumer_inst = handle.query_classid(
        class_id='ConsumerInst', filter_str=filter_str)

    if (len(consumer_inst) <= 0):
        raise UcsCentralOperationError("Import config domain",
                                       "Unable to get Domain instance"
                                       "with IP %s for import " %
                                       to_domain.address)

    consumer_dn = consumer_inst[0].dn
    top_system = handle.query_dn("sys")

    mgmt_importer = MgmtImporter(
        parent_mo_or_dn=consumer_dn,
        hostname=top_system.address,
        remote_file='/' + from_domain.address + '/cfg-backups/' + config_file,
        proto=MgmtImporterConsts.PROTO_TFTP,
        admin_state=MgmtImporterConsts.ADMIN_STATE_ENABLED)

    if merge:
        mgmt_importer.action = MgmtImporterConsts.ACTION_MERGE
    else:
        mgmt_importer.action = MgmtImporterConsts.ACTION_REPLACE

    handle.add_mo(mgmt_importer, modify_present=True)
    handle.commit(dme="operation-mgr")

    duration = timeout
    poll_interval = 2
    log.debug("Importing domain config")
    while True:
        mgmt_importer = handle.query_dn(
                dn=mgmt_importer.dn,
                dme="operation-mgr")
        admin_state = mgmt_importer.admin_state

        # Break condition:- if state id disabled then break
        if admin_state == MgmtImporterConsts.ADMIN_STATE_DISABLED:
            break

        time.sleep(min(duration, poll_interval))
        duration = max(0, (duration - poll_interval))
        if duration == 0:
            raise UcsCentralOperationError(
                  "Import config", "operation timed out")

    if mgmt_importer.op_status != \
            MgmtImporterConsts.OP_STATUS_ALL_SUCCESS:
            raise UcsCentralOperationError(
                  "Import config",
                  ("operational status %s " % mgmt_importer.op_status))

    log.debug("Import config to domain was successfull")
    return mgmt_importer


def _schedule_backup(handle, descr, sched_name, max_bkup_files, remote_enabled,
                     protocol, hostname, file_path,
                     username, password, parent_mo_or_dn):

    """
    Internal method to schedule and take remote backup of UcsCentral and Domain
    full-state backup
    """
    from ..mometa.mgmt.MgmtBackupPolicy import MgmtBackupPolicy, \
        MgmtBackupPolicyConsts

    if remote_enabled:
        if not file_path:
            raise UcsCentralValidationException("Missing file_path argument")

        _validate_remote_host_args(protocol, hostname, username, password)
        proto = protocol
        host = hostname
        remote_file = file_path
        user = username
        pwd = password
    else:
        proto = MgmtBackupPolicyConsts.PROTO_NFS_COPY
        host = ""
        remote_file = " "
        user = ""
        pwd = ""

    backup_pol = MgmtBackupPolicy(
            parent_mo_or_dn=parent_mo_or_dn,
            descr=descr,
            admin_state=MgmtBackupPolicyConsts.ADMIN_STATE_ENABLE,
            sched_name=sched_name,
            max_files=str(max_bkup_files),
            proto=proto,
            host=host,
            remote_file=remote_file,
            user=user,
            pwd=pwd,
            name="default")

    handle.add_mo(backup_pol, modify_present=True)
    handle.commit()

    return backup_pol


def schedule_backup(handle, descr="Database Backup Policy",
                    sched_name="global-default", max_bkup_files="2",
                    remote_enabled=False, protocol=None,
                    hostname=None, file_path=None,
                    username=None, password=""):
    """
    schedule_backup helps schedule and optionally take remote backup of
    UcsCentral full-state backup.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        descr (str): Description of the policy
        sched_name (str): Name of the schedule
        max_bkup_files (str): Number of files to keep as backup
        remote_enabled (boolean): True if Remote backup is enabled
                                  False - by default
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        file_path (str): Absolute file path on remote host
        username (str): Username for remote backup
        password (str): Password for remote backup

    Example:
        file_path = "/ws/usr-admin/backup.tgz"\n
        schedule_backup(handle, max_bkup_files=3)

        schedule_backup(handle, file_path=file_path,
                        remote_enabled=True,
                        protocol='scp',hostname='192.168.1.1',
                        username='admin',password='password')\n

    """

    return _schedule_backup(
           handle, descr=descr, sched_name=sched_name,
           max_bkup_files=max_bkup_files,
           remote_enabled=remote_enabled, protocol=protocol,
           hostname=hostname, file_path=file_path,
           username=username, password=password,
           parent_mo_or_dn=ucscentral_base_dn)


def schedule_backup_domain(handle, descr="Database Backup Policy",
                           sched_name="global-default", max_bkup_files="2",
                           remote_enabled=False, protocol=None,
                           hostname=None, file_path=None,
                           username=None, password="",
                           domain_group="root"):
    """
    schedule_backup_domain helps schedule and optionally take remote backup of
    domain's full-state backup.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        descr (str): Description of the policy
        sched_name (str): Name of the schedule
        max_bkup_files (str): Number of files to keep as backup
        remote_enabled (boolean): True if Remote backup is enabled
                                  False - by default
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        file_path (str): Absolute file path on remote host
        username (str): Username for remote backup
        password (str): Password for remote backup
        domain_group (str): Fully qualified domain group name

    Example:
        file_path = "/ws/usr-admin/backup.tgz"\n
        schedule_backup_domain(handle, max_bkup_files=3)

        schedule_backup_domain(handle, file_path=file_path,
                               remote_enabled=True,
                               protocol='scp',hostname='192.168.1.1',
                               username='admin',password='password',
                               domain_group="root/demo_domgrp")\n

    """

    from ucscentralsdk.utils.ucscentraldomain import get_domain_group_dn
    domain_group_dn = get_domain_group_dn(handle, domain_group)

    return _schedule_backup(
           handle, descr=descr, sched_name=sched_name,
           max_bkup_files=max_bkup_files,
           remote_enabled=remote_enabled, protocol=protocol,
           hostname=hostname, file_path=file_path,
           username=username, password=password,
           parent_mo_or_dn=domain_group_dn)


def _schedule_export_config(handle, descr, sched_name,
                            max_bkup_files, remote_enabled,
                            protocol, hostname, file_path,
                            username, password,
                            parent_mo_or_dn):

    """
    Internal method to schedule and take remote backup of UcsCentral and Domain
    config-all backup
    """
    from ..mometa.mgmt.MgmtCfgExportPolicy import MgmtCfgExportPolicy, \
        MgmtCfgExportPolicyConsts

    if remote_enabled:
        if not file_path:
            raise UcsCentralValidationException("Missing file_path argument")

        _validate_remote_host_args(protocol, hostname, username, password)
        proto = protocol
        host = hostname
        remote_file = file_path
        user = username
        pwd = password
    else:
        proto = MgmtCfgExportPolicyConsts.PROTO_NFS_COPY
        host = ""
        remote_file = " "
        user = ""
        pwd = ""

    cfg_export_pol = MgmtCfgExportPolicy(
            parent_mo_or_dn=parent_mo_or_dn,
            descr=descr,
            admin_state=MgmtCfgExportPolicyConsts.ADMIN_STATE_ENABLE,
            sched_name=sched_name,
            max_files=str(max_bkup_files),
            proto=proto,
            host=host,
            remote_file=remote_file,
            user=user,
            pwd=pwd,
            name="default")

    handle.add_mo(cfg_export_pol, modify_present=True)
    handle.commit()

    return cfg_export_pol


def schedule_export_config(handle, descr="Configuration Export "
                           "Policy", sched_name="global-default",
                           max_bkup_files="2",
                           remote_enabled=False, protocol=None,
                           hostname="", file_path="",
                           username=None, password=""):
    """
    schedule_export_config helps schedule and optionally take remote backup of
    UcsCentral's config-all backup.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        descr (str): Description of the policy
        sched_name (str): Name of the schedule
        max_bkup_files (str): Number of files to keep as backup
        remote_enabled (boolean): True if Remote backup is enabled
                                  False - by default
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        file_path (str): Absolute file path on remote host
        username (str): Username for remote backup
        password (str): Password for remote backup

    Example:
        file_path = "/ws/usr-admin/config.tgz"\n
        schedule_export_config(handle, max_bkup_files=3)

        schedule_export_config(handle, file_path=file_path,
                               remote_enabled=True,
                               protocol='scp',hostname='192.16.1.1',
                               username='admin',password='pass')\n

    """

    return _schedule_export_config(
           handle, descr=descr, sched_name=sched_name,
           max_bkup_files=max_bkup_files,
           remote_enabled=remote_enabled, protocol=protocol,
           hostname=hostname, file_path=file_path,
           username=username, password=password,
           parent_mo_or_dn=ucscentral_base_dn)


def schedule_export_config_domain(handle, descr="Configuration Export "
                                  "Policy", sched_name="global-default",
                                  max_bkup_files="2",
                                  remote_enabled=False, protocol=None,
                                  hostname="", file_path="",
                                  username=None, password=None,
                                  domain_group="root"):
    """
    schedule_export_config_domain helps schedule and optionally take remote
    backup of domain's config-all backup.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        descr (str): Description of the policy
        sched_name (str): Name of the schedule
        max_bkup_files (str): Number of files to keep as backup
        remote_enabled (boolean): True if Remote backup is enabled
                                  False - by default
        protocol (str): Transfer protocol for remote backup
                        ['ftp','sftp','tftp','scp']
        hostname (str): Hostname/IP for the remote backup
        file_path (str): Absolute file path on remote host
        username (str): Username for remote backup
        password (str): Password for remote backup
        domain_group (str): Fully qualified domain group name

    Example:
        file_path = "/ws/usr-admin/config.tgz"\n
        schedule_export_config_domain(handle, max_bkup_files=3)

        schedule_export_config_domain(handle, file_path=file_path,
                                      remote_enabled=True,
                                      protocol='scp',hostname='192.16.1.1',
                                      username='admin',password='pass',
                                      domain_group="root/demo_domgrp")\n

    """
    from ucscentralsdk.utils.ucscentraldomain import get_domain_group_dn
    domain_group_dn = get_domain_group_dn(handle, domain_group)

    return _schedule_export_config(
           handle, descr=descr, sched_name=sched_name,
           max_bkup_files=max_bkup_files,
           remote_enabled=remote_enabled, protocol=protocol,
           hostname=hostname, file_path=file_path,
           username=username, password=password,
           parent_mo_or_dn=domain_group_dn)


def remove_schedule_backup(handle):
    """
    remvove_schedule_backup removes the schedule of UcsCentral's
    full backup.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle

    Example:
        remove_schedule_backup(handle)

    """

    from ..mometa.mgmt.MgmtBackupPolicy import MgmtBackupPolicyConsts
    dn = ucscentral_base_dn + "/db-backup-policy-default"

    mo = handle.query_dn(dn=dn)
    if not mo:
        raise UcsCentralOperationError("Remove backup schedule",
                                       "Backup Schedule doesn't exist")

    mo.admin_state = MgmtBackupPolicyConsts.ADMIN_STATE_DISABLE

    handle.set_mo(mo)
    handle.commit()


def remove_schedule_export_config(handle):
    """
    remvove_schedule_export_config removes the schedule of
    UcsCentral config-all backup.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle

    Example:
        remove_schedule_export_config(handle)

    """

    from ..mometa.mgmt.MgmtCfgExportPolicy import MgmtCfgExportPolicyConsts
    dn = ucscentral_base_dn + "/cfg-exp-policy-default"

    mo = handle.query_dn(dn=dn)
    if not mo:
        raise UcsCentralOperationError("Remove export config",
                                       "Export config schedule doesn't exist")

    mo.admin_state = MgmtCfgExportPolicyConsts.ADMIN_STATE_DISABLE

    handle.set_mo(mo)
    handle.commit()


def remove_schedule_backup_domain(handle, domain_group="root"):
    """
    remvove_schedule_backup_domain removes the schedule policy of Domain's
    full backup.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        domain_group (str): Fully qualified domain group name

    Example:
        remove_schedule_backup_domain(handle, domain_group="root/demo_domgrp")

    """

    from ..mometa.mgmt.MgmtBackupPolicy import MgmtBackupPolicyConsts
    from ucscentralsdk.utils.ucscentraldomain import get_domain_group_dn
    domain_group_dn = get_domain_group_dn(handle, domain_group)

    dn = domain_group_dn + "/db-backup-policy-default"

    mo = handle.query_dn(dn=dn)
    if not mo:
        raise UcsCentralOperationError("Remove backup schedule",
                                       "Backup Schedule doesn't exist")

    mo.admin_state = MgmtBackupPolicyConsts.ADMIN_STATE_DISABLE

    handle.set_mo(mo)
    if domain_group != "root":
        handle.remove_mo(mo)
    handle.commit()


def remove_schedule_export_config_domain(handle, domain_group="root"):
    """
    remvove_schedule_export_config_domain removes the schedule policy of
    Domain's config-all backup.

    Args:
        handle (UcsCentralHandle): UcsCentral Connection handle
        domain_group (str): Fully qualified domain group name

    Example:
        remove_schedule_export_config_domain(handle,
                               domain_group="root/demo_domgrp")\n

    """

    from ..mometa.mgmt.MgmtCfgExportPolicy import MgmtCfgExportPolicyConsts
    from ucscentralsdk.utils.ucscentraldomain import get_domain_group_dn
    domain_group_dn = get_domain_group_dn(handle, domain_group)

    dn = domain_group_dn + "/cfg-exp-policy-default"

    mo = handle.query_dn(dn=dn)
    if not mo:
        raise UcsCentralOperationError("Remove export config",
                                       "Export config schedule doesn't exist")

    mo.admin_state = MgmtCfgExportPolicyConsts.ADMIN_STATE_DISABLE

    handle.set_mo(mo)
    if domain_group != "root":
        handle.remove_mo(mo)
    handle.commit()
