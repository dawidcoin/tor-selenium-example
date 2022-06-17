### Tor Selenium example

Example of using Selenium with Tor Browser (firefox driver).

#### Install

Install Tor using instructions from here https://support.torproject.org/apt/tor-deb-repo/ (you can simply use `apt install tor` but it's not recommended by [tor project website](https://support.torproject.org/apt/)). Enable control port and password-protect it:

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

Start script with:

```commandline
python3 firefox.py
```

This should open browser on [tor project website](http://check.torproject.org) displaying your ip (you have one second to memorize it :D). Then browser will restart and the same page will open (this time with different IP hopefully).

Note: Make sure that Tor service is running.
