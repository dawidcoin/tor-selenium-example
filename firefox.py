from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from stem import Signal
from stem.control import Controller
from yaml import full_load
from typing import Dict
from time import sleep

FIREFOX_PROFILE_PATH = '/usr/local/bin/Browser/TorBrowser/Data/Browser/profile.default'
FIREFOX_BINARY_PATH = '/usr/local/bin/Browser/firefox'
CONFIG_FILE = "config.yaml"


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


def tor_request_new_circuit(password: str) -> None:
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM)


if __name__ == "__main__":
    config = load_yaml_config()
    driver = Firefox(
        options=get_firefox_options(config['firefox_profile_path'], config['firefox_binary_path'])
    )
    driver.get("http://check.torproject.org")
    print("Requesting new circuit")
    tor_request_new_circuit(config['password'])
    print("Wait 5 seconds...")
    sleep(5)
    driver.get("http://check.torproject.org")
