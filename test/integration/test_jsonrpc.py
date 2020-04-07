import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from bitcored import BitcoreDaemon
from bitcore_config import BitcoreConfig


def test_bitcored():
    config_text = BitcoreConfig.slurp_config_file(config.bitcore_conf)
    #network = 'main'
    network = 'main'
    is_testnet = False
    genesis_hash = u'604148281e5c4b7f2487e5d03cd60d8e6f69411d613f6448034508cea52e9574'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'02c5d66e8edb49984eb743c798bca069466ce457b7febfa3c3a01b33353b7bc6'

    creds = BitcoreConfig.get_rpc_creds(config_text, network)
    bitcored = BitcoreDaemon(**creds)
    assert bitcored.rpc_command is not None

    #assert hasattr(bitcored, 'rpc_connection')

    # Bitcore testnet block 0 hash == 02c5d66e8edb49984eb743c798bca069466ce457b7febfa3c3a01b33353b7bc6
    # test commands without arguments
    info = bitcored.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert bitcored.rpc_command('getblockhash', 0) == genesis_hash
