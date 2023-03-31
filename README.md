# Scrap & Trace Backend Server (Django/Python)

## Install Instructions

Similarly, we developed a backend server for the mobile application. This server was developed using Django, a Python web framework. This repository contains the source code for the server. To get started with the server, you will need to install the following:

- Python 3.9 or higher
- pip
- python3-venv (optional, but recommended)
- tmux (optional, but recommended)

First, you will need to install Python 3.9.2. You can download the installer for your operating system from [here](https://www.python.org/downloads/release/python-392/). Once installed, you will need to install `pip`, which is the Python package manager. You can do this by running the following command:

```bash
python -m ensurepip --upgrade
```

Once `pip` has been installed, you will need to set up the virtual environment for the project. While optional, it is highly recommended that you use a virtual environment for the project. This will allow you to install the dependencies for the project without affecting the rest of your system. Once the virtual environment has been created, you will need to activate it. To do this, install `python3-venv` by running the following command:

Ubuntu/Debian:

```bash
sudo apt install python3-venv
```

Fedora/CentOS/RHEL:

```bash
sudo dnf install python3-venv
```

Once installed, navigate to a folder where you would like to store the project. Once there, you can create a virtual environment for the project by running the following command:

```bash
python -m venv venv
```

Once the virtual environment has been created, you will need to activate it. You can do this by running the following command:

```bash
source venv/bin/activate
```

Note that on Windows, you will need to run the following command instead:

```bash
venv\Scripts\activate.bat
```

Once the virtual environment has been activated, you will need to clone the repository from GitHub. You can do this by running the following command in your terminal or using the Visual Studio Code Git interface:

```bash
git clone https://github.com/scrap-and-trace/ScrapAppDjango.git
```

Note that at this time, the repository is private, so you will need to have access to the repository in order to clone it. It will be made public once the project is complete. Once you have downloaded the repository, you will need to install the dependencies for the project. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

Once the dependencies have been installed, you can run the server by running the following command:

```bash
python manage.py runserver 0.0.0.0:8000
```

This will allow the server to be accessible from other devices on the network. You can then access the server by navigating to `http://<ip-address>:8000` in your browser. Note that you will need to replace `<ip-address>` with the IP address of the device running the server.

If you would like to run the server in the background, you can use `tmux`. You can install `tmux` by running the following command(s):

Ubuntu/Debian:

```bash
sudo apt install tmux
```

Fedora/CentOS/RHEL:

```bash
sudo dnf install tmux
```

Once `tmux` has been installed, you can run the server in the background by running the following commands:

```bash
tmux
python manage.py runserver 0.0.0.0:8000
```

You can attach and detach from the server at any time using `tmux attach` and `tmux detach`, respectively.

If you would like for the server to be accessible from the internet, you will need to set up port forwarding on your router. You can find instructions on how to do this [here](https://portforward.com/router.htm). Note that you will need to forward port 8000 to the IP address of the device running the server with the protocol set to TCP.
