import json
import eero
import six

class CookieStore(eero.SessionStorage):
    def __init__(self, cookie_file):
        from os import path
        self.cookie_file = path.abspath(cookie_file)

        try:
            with open(self.cookie_file, 'r') as f:
                self.__cookie = f.read()
        except IOError:
            self.__cookie = None
    @property
    def cookie(self):
        return self.__cookie
    @cookie.setter
    def cookie(self, cookie):
        self.__cookie = cookie
        with open(self.cookie_file, 'w+') as f:
            f.write(self.__cookie)

session = CookieStore('session.cookie')
eero = eero.Eero(session)

def print_connected_devices(data):
    device = ""
    count = 3
    flag = False
    for item in data.split("\n"):
        if count > 0:
            count = count - 1
            if "phone" in item or "Phone" in item:
                flag = True
            device = device + "\n" + item.strip()
            continue
        if "connected" in item:
            count = 2
            device = device + "\n" + item.strip()
            if "true" in item:
                if flag:
                    print(device)
                    flag = False

            device = ""


def parse_json(data):
    data_string = json.dumps(data, indent=4)
    count = 0
    parsed_string = ""
    for item in data_string.split("\n"):
        if count > 0:
            count = count - 1
            parsed_string = parsed_string + "\n" + item.strip()
            continue
        if "nickname" in item:
            count = 2
            parsed_string = parsed_string + "\n" + item.strip()

    print_connected_devices(parsed_string)

def print_json(data):
    print(json.dumps(data, indent=4))

if __name__ == '__main__':
    while eero.needs_login():
        phone_number = six.moves.input('your eero login (email address or phone number): ')
        user_token = eero.login(phone_number)
        verification_code = six.moves.input('verification key from email or SMS: ')
        eero.login_verify(verification_code, user_token)
        print('Login successful')

    #this is where i mess with things for GUI
    account = eero.account()

    print('Command options: info, details, devices, eeros, reboot')
    command = six.moves.input('enter a command: ')

    for network in account['networks']['data']:
        if command == 'info':                       #just gives network name
            print_json(network)
        if command == 'details':                     #gives details on network
            network_details = eero.networks(network['url'])
            print_json(network_details)
        if command == 'devices':                    #gives devices and details on devices
            devices = eero.devices(network['url'])
            parse_json(devices)
        if command == 'eeros':                      #gives details on gateway, routers, and boosters
            eeros = eero.eeros(network['url'])
            print_json(eeros)
        if command == 'reboot':                     #reboots an eero device
            print('Eero options are: office , upstairs (gateway), family room, hallway')
            name = six.moves.input('Name of Eero to be rebooted: ')

            if name == 'office':
                reboot = eero.reboot()
                print_json(reboot)
            elif name == 'upstairs':
                reboot = eero.reboot()
                print_json(reboot)
            elif name == 'family room':
                reboot = eero.reboot()
                print_json(reboot)
            elif name == 'hallway':
                reboot = eero.reboot()
                print_json(reboot)
            else:
                print('Please put in a valid name')

