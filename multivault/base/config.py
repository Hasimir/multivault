#!/usr/bin/env python3

'''
    Configuration Module for the yaml config file
'''
import os
import sys
import yaml
from pathlib import Path


def load_config():
    # Suitable config paths
    config_path = None
    system_config_path = os.path.join('/etc', 'multivault.yml')
    user_config_dir_config_path = os.path.join(
        Path.home(), ".config", "multivault.yml")
    user_config_path = os.path.join(Path.home(), '.multivault.yml')

    if os.path.exists(system_config_path):
        config_path = system_config_path

    if os.path.exists(user_config_dir_config_path):
        config_path = user_config_dir_config_path

    if os.path.exists(user_config_path):
        config_path = user_config_path

    if not config_path:
        print('No Configuration under:')
        print('\t{}'.format(system_config_path))
        print("\t{}".format(user_config_dir_config_path))
        print("\t{}".format(user_config_path))
        sys.exit(1)
    else:
        init(conf_path=config_path)


def init(conf_path=os.path.join('/etc', 'multivault.yml')):
    '''
        initialize the configuration
        @param conf_path configuration path to be loaded
    '''
    # Disabled becaus global variables are only loaded,
    # when init(conf_path=something) was invoked
    # pylint: disable=W0601, C0103, R0912, R0915
    global GLOBAL_HOME_PATH
    global CONFIG_PATH
    global KEY_PATH
    global CONFIG
    global GPG_KEYSERVER
    global LDAP_URL
    global LDAP_SSH_HOP
    global LDAP_DC
    global LDAP_USER_OU
    global LDAP_SUDOER_OU
    global LDAP_HOST_ATTRIBUTE
    global LDAP_SUDOER_ATTRIBUTE
    global LDAP_MASTER_BEFORE
    global LDAP_MASTER_AFTER
    global LDAP_GPG_ATTRIBUTE
    GLOBAL_HOME_PATH = os.path.dirname(os.path.realpath(__file__))
    CONFIG_PATH = conf_path
    KEY_PATH = os.path.join("/tmp", "keys")
    with open(CONFIG_PATH, "r") as config:
        CONFIG = yaml.load(config)

    PRAEFIX = 'No '
    SUFFIX = ' in Configuration under {}.'.format(CONFIG_PATH)

    try:
        GPG_KEYSERVER = CONFIG['gpg_key_server']
    except KeyError:
        GPG_KEYSERVER = 'hkp://pool.sks-keyservers.net'

    try:
        LDAP = CONFIG['ldap']
    except KeyError:
        LDAP = None
        print(PRAEFIX, 'ldap:', SUFFIX)
        sys.exit(1)

    try:
        LDAP_URL = LDAP['url']
    except KeyError:
        LDAP_URL = None
        print(PRAEFIX, 'ldap:\n\turl:', SUFFIX)
        sys.exit(1)

    try:
        LDAP_CONNECTION = LDAP['connection']
    except KeyError:
        LDAP_CONNECTION = None
        print(PRAEFIX, 'ldap:\n\tconnection:', SUFFIX)
        sys.exit(1)

    try:
        LDAP_SSH_HOP = LDAP_CONNECTION['ssh_hop']
    except KeyError:
        LDAP_SSH_HOP = None

    try:
        LDAP_DC = LDAP['dc']
    except KeyError:
        LDAP_DC = None
        print(PRAEFIX, 'ldap:\n\tdc:', SUFFIX)
        sys.exit(1)

    try:
        LDAP_USER_OU = LDAP['user_ou']
    except KeyError:
        LDAP_USER_OU = None
        print(PRAEFIX, 'ldap:\n\tuser_ou: people # example', SUFFIX)
        sys.exit(1)

    try:
        LDAP_SUDOER_OU = LDAP['sudoer_ou']
    except KeyError:
        LDAP_USER_OU = None
        print(PRAEFIX, 'ldap:\n\tsudoer_ou: sudoers # example', SUFFIX)
        sys.exit(1)

    try:
        LDAP_SUDOER_ATTRIBUTE = LDAP['attribute_sudoer']
    except KeyError:
        LDAP_HOST_ATTRIBUTE = None
        print(PRAEFIX, 'ldap:\n\tattribute_sudoer: sudoUser # example', SUFFIX)
        sys.exit(1)

    try:
        LDAP_HOST_ATTRIBUTE = LDAP['attribute_hostname']
    except KeyError:
        LDAP_HOST_ATTRIBUTE = None
        print(PRAEFIX, 'ldap:\n\tattribute_hostname: cn # example', SUFFIX)
        sys.exit(1)

    try:
        LDAP_MASTER = LDAP['master']
    except KeyError:
        LDAP_MASTER = None
        print(PRAEFIX, 'ldap:\n\tmaster:', SUFFIX)
        sys.exit(1)

    try:
        LDAP_MASTER_BEFORE = LDAP_MASTER['before_equal']
    except KeyError:
        LDAP_MASTER_BEFORE = None
        print(PRAEFIX, 'ldap:\n\tmaster:\n\t\tbefore_equal', SUFFIX)

    try:
        LDAP_MASTER_AFTER = LDAP_MASTER['after_equal']
    except KeyError:
        LDAP_MASTER_AFTER = None
        print(PRAEFIX, 'ldap:\n\tmaster\n\t\tafter_equal', SUFFIX)
        sys.exit(1)

    try:
        LDAP_GPG_ATTRIBUTE = LDAP['attribute_gpg']
    except KeyError:
        LDAP_GPG_ATTRIBUTE = None
        print(PRAEFIX, 'ldap:\n\tattribute_gpg:', SUFFIX)
        sys.exit(1)
    # DEBUG: (Shows Global Variables read from config file)
    # for name, value in globals().items():
    #     print(name, value)
