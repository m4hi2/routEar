# routEar

Receives JSON data from router to notify the user (Through Desktop Notification) about various network information. The information can be sent via scripts from the router.

Very basic network related automation tool. Basically written for people too lazy to refresh the web page to check if their network is back online or not after a connection dropout. Also, notifies when the internet goes down so no more guessing game if the router crashed or something else happened.

The fucntionality can be adapted to show any kind of network related diagnostic information sent from the router by changing the messages inside the code and/or creating more API endpoints. This can show port status and so on, limited by the necessity of the user.

## OS Support

[✔] Windows 10

[❌] macOS

[❌] GNU/Linux

PS: I hope people will implement the other OS supports as needed. I'll probably add macOS support myself. But don't angry mail me please. 🥺

## Usage

Get the code:

``` bash
git clone https://github.com/m4hi2/routEar.git
```

Install the required packages with:

``` bash
pip install -r requirements.txt
```

Run the app with:

``` bash
python main.py
```

Don't forget to click `allow` on the firewall prompt when prompted.

### Using the exe file from release

I've created a windows binary using `pyinstaller` and it can be found under [releases](https://github.com/m4hi2/routEar/releases/tag/v0.1.0-alpha). This exe file can be directly ran by double clicking it or you can put it in your startup directory. Don't forget the icon file though 🤣

## Setup/Scripting on the router side

### Mikrotik

Mikrotik routers have a very handy feature called `tools/netwatch` that automatically pings given IP addresses and sends an interrupt based on the latency to the host. This information can be used to determined if there is internet connectivity or not. `netwatch` can also be used to trigger scripts based on host availability. Using this we can easily send a request to our flask webserver that's been running on our host machine.

Example:

Netwatch Up:

``` bash
/tool fetch http-method=post http-data="{\"affected\":\"internet\",\"status\":\"up\"}" output=none url="http://X.X.X.X:8000/"  http-header-field="content-type: application/json"
```

Netwatch Down:

``` bash
/tool fetch http-method=post http-data="{\"affected\":\"internet\",\"status\":\"down\"}" output=none url="http://X.X.X.X:8000/"  http-header-field="content-type: application/json"
```

Don't forget to change X.X.X.X with the IP of your desktop. Also, use static IP for the host.

### OpenWRT

IDK man, don't have any OpenWrt box right now. Maybe some `curl` stuff? no clue. If you know, please write and send a pull request. Thank You !

## Awesome Discord

Join Linux Bangladesh community at [kill -9](https://discord.gg/kyaRT22wqZ). The language of the server is : Bengali (BN_BD 😉) but I'm certain we understand English as well.

## Credits

Project name credit goes to [Aniruddha Adhikary](https://github.com/aniruddha-adhikary) (I initially named it, "windowsNetworkNotifier-withRouterScripts" 🤦‍♂️)
