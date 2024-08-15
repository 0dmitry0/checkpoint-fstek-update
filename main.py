from cpapi import APIClient, APIClientArgs


ips_listing = []
ips_listing_with_names = []

smart_console_host = '192.168.1.111'
smart_console_login = 'admin'
smart_console_password = 'P@ssw0rd'
ips_file = '/Users/dmitry/Desktop/ips.txt'
layer = 'url_filtering'
network_group = 'fstek'

def main_api_func(function_flag, ip, name, ips_with_names):
    client_args = APIClientArgs()
    client_args = APIClientArgs(server = smart_console_host)
    with APIClient(client_args) as client: 
        client = APIClient(client_args)
        if client.check_fingerprint() is False:
            print ('Fingerprint failed!')
            exit(1)
        else:
            login = client.login(smart_console_login, smart_console_password)
            if function_flag == 'add-host':
                add_host = client.api_call('add-host', {'name': name, 'ip-address': ip})
                print(add_host)
            add_host_to_group = client.api_call('set-group', {'name': network_group, 'members': ips_with_names})
            print(add_host_to_group)
            publish = client.api_call('publish')
            client.api_call('logout', {})

class rule:
    
    def __init__(self, ip, ips_with_names):
            self.ip = ip
            self.name = 'ip_for_block_' + ip
            self.ips_with_names = []
            self.ips_with_names = ips_with_names
    
    def add_hosts(self):
            main_api_func('add-host', self.ip, self.name, self.ips_with_names)

def ip_parser(filename):
    with open(filename, 'r') as f:
        for line in f:
            ip = line.strip()
            ips_listing.append(ip)
            ips_listing_with_names.append('ip_for_block_' + ip)
        return ips_listing

ips = ip_parser(ips_file)

for ip in ips:
    new = rule(ip, ips_listing_with_names)
    new.add_hosts()