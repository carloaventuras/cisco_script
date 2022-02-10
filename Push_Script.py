from netmiko import ConnectHandler
from csv import DictReader

# open file in read mode
with open('\\Users\\user_name\\cisco_script\\my_ip.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    csv_dict_reader = DictReader(read_obj)

    # iterate over each line as a ordered dictionary
    for row in csv_dict_reader:

        Fa = str(row['Fa'])         #fast port number
        Id = str(row['Id#'])        #Id Number

        IpNumber = str(IpOct + str(IpEnd+2))
        txtName   = str(Fa) + '_' + 'Id' +str(Id)

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
