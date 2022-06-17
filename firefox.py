from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from stem import Signal
from stem.control import Controller
from yaml import full_load
from typing import Dict
from time import sleep

CONFIG_FILE = "config.yaml"
URL = "http://check.torproject.org"


def load_yaml_config() -> Dict:
    try:
        with open(CONFIG_FILE) as file:
            config_dict = full_load(file)
        return config_dict
    except FileNotFoundError:
        print(f'No {CONFIG_FILE} folder.')
        exit(1)


def get_firefox_options(firefox_profile_path: str, firefox_binary_path: str) -> Options:
    options = Options()
    options.set_preference('profile', firefox_profile_path)
    options.set_preference('extensions.torlauncher.start_tor', False)
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.socks', '127.0.0.1')
    options.set_preference('network.proxy.socks_port', 9050)
    options.set_preference("network.proxy.socks_remote_dns", True)
    options.binary_location = firefox_binary_path
    return options


def get_driver(firefox_profile_path: str, firefox_binary_path: str) -> Firefox:
    return Firefox(
        options=get_firefox_options(firefox_profile_path, firefox_binary_path)
    )


def tor_request_new_circuit(password: str) -> None:
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM)


if __name__ == "__main__":
    config = load_yaml_config()
    driver = get_driver(config['firefox_profile_path'], config['firefox_binary_path'])
    driver.get(URL)
    print("Requesting new circuit")
    tor_request_new_circuit(config['password'])
    sleep(1)  # check the ip on the browser fast :)
    print("Reopening driver")
    driver.close()
    driver = get_driver(config['firefox_profile_path'], config['firefox_binary_path'])
    driver.get(URL)
