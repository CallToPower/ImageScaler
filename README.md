# ImageScaler

* Scales images
* Option for creating a PDF containing all images

GUI written in PyQt 5. Graphical installers for both, Mac OS and Windows.



## Prerequisites

* Python 3
* Windows
  * Install NSIS - http://nsis.sourceforge.net
  * Add Python to PATH variable in environment
  * Add NSIS to PATH variable in environment

## Usage

* Start shell
  * Windows
    * Start shell as administrator
    * `Set-ExecutionPolicy Unrestricted -Force`
* Create a virtual environment
  * `python -m venv venv`
* Activate the virtual environment
  * Mac/Linux
    * `source venv/bin/activate`
  * Windows
    * `.\venv\scripts\activate`
* Install the required libraries
  * `pip install -r requirements.txt`
* Run the app
  * `python -m fbs run`

## Shipping

* Freeze the app (create an executable)
  * `python -m fbs freeze`
* Build an installer (create an installer)
  * `python -m fbs installer`
