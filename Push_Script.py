from netmiko import ConnectHandler
from csv import DictReader



# open file in read mode
with open('C:\Users\ctoro\Documents\EBCS Config\Script\mr_auto_script\pi_ip.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    csv_dict_reader = DictReader(read_obj)

    # iterate over each line as a ordered dictionary
    for row in csv_dict_reader:

        IpNumber = str(row['ip'])
        txtName   = str(row['txtName'])

        cisco_device = {
                'device_type': 'cisco_ios',
                'ip': str(IpNumber),
                'username': 'admin',
                'password': 'P@ssw0rd',
                'port': 22,
                'secret': 'P@ssw0rd',
                'verbose':True
                }

        connection = ConnectHandler(**cisco_device)

        print('Entering enable mode...')
        connection.enable()

        print('Running commads from file...')
        output = connection.send_config_from_file(txtName + '.txt')
        print(output)

        connection.disconnect()


#Netmiko commonly-used methods:
#
#net_connect.send_command() - Send command down the channel, return output back (pattern based)
#net_connect.send_command_timing() - Send command down the channel, return output back (timing based)
#net_connect.send_config_set() - Send configuration commands to remote device
#net_connect.send_config_from_file() - Send configuration commands loaded from a file
#net_connect.save_config() - Save the running-config to the startup-config
#net_connect.enable() - Enter enable mode
#net_connect.find_prompt() - Return the current router prompt
#net_connect.commit() - Execute a commit action on Juniper and IOS-XR
#net_connect.disconnect() - Close the connection
#net_connect.write_channel() - Low-level write of the channel
#net_connect.read_channel() - Low-level write of the channel