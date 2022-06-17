### Tor Selenium example

Example of using Selenium with Tor Browser.

#### Install

Install Tor using instructions from here https://support.torproject.org/apt/ (you can simply use `apt install tor` but it's not recommended by tor project website). Enable control port and password-protect it:

```commandline
torpass=$(tor --hash-password "my-tor-password")
printf "HashedControlPassword $torpass\nControlPort 9051\n" | sudo tee -a /etc/tor/torrc
```

Confirm that password was properly included and restart tor service:

```commandline
tail -2 /etc/tor/torrc
sudo systemctl restart tor
```

Clone the repo and run the following:

```commandline
cd tor-selenium-example
source source_me.sh
create_venv
```

#### Usage

TODO

Make sure that Tor service is running.
