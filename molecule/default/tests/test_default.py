import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_disable_thp(host):
    f = host.file('/etc/init.d/disable-transparent-hugepages')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert oct(f.mode) == '0755'

    f = host.file('/sys/kernel/mm/transparent_hugepage/defrag')
    assert f.exists
    assert f.contains('[never]')

    f = host.file('/sys/kernel/mm/transparent_hugepage/enabled')
    assert f.exists
    assert f.contains('[never]')
