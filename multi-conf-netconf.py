import paramiko,time

devices = ['172.16.13.15','172.16.13.14']

conn = paramiko.SSHClient()
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy)

for device in devices:
    print(f'Connecting to {device}')
    conn.connect(device,
                 username='admin',
                 password='admin',
                 port=22,
                 look_for_keys=False)
    
    ch = conn.get_transport().open_session()
    ch.invoke_subsystem('netconf')
    print(f'Sending hello message to {device}')
    hello = '<?xml version="1.0"?><nc:hello xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"><nc:capabilities><nc:capability>urn:ietf:params:xml:ns:netconf:base:1.0</nc:capability></nc:capabilities></nc:hello>]]>]]>'
    ch.send(hello)
    print(f'Sending rpc message to {device}')
    cmd = '''<?xml version="1.0"?>
    <nc:rpc message-id="1" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"
      xmlns="http://www.cisco.com/nxos:1.0:if_manager">
      <nc:edit-config>
        <nc:target>
          <nc:running/>
        </nc:target>
        <nc:config>
          <configure>
            <__XML__MODE__exec_configure>
              <interface>
                <ethernet>
                  <interface>1/42</interface>
                  <__XML__MODE_if-ethernet>
                    <__XML__MODE_if-eth-base>
                      <description>
                        <desc_line>CSCO_CSSN</desc_line>
                      </description>
                    </__XML__MODE_if-eth-base>
                  </__XML__MODE_if-ethernet>
              </ethernet>
            </interface>
            </__XML__MODE__exec_configure>
          </configure>
        </nc:config>
      </nc:edit-config>
    </nc:rpc>]]>]]>'''
    ch.send(cmd)
    conn.close()
