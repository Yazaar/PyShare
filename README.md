# PyShare
### How does it work?

#### PyShare hosts a webserver which you can access on the same network, your local IP is printed in the console if on windows, else it might print localhost (127.0.0.1), but if you are on linux you should be able to figure it out yourself anyways :P

#### From the webserver are you able to upload files from your device to the webserver as well as download files to your device from the webserver. All files who should be accessible have to be within the shared folder which exists in the same directory

#### Run the executable if on windows, else run the Python script. If using Python make sure the module "flask" is installed

To install the dependencies run:

`pip install -r requirements.txt`
(make sure to be in the same directory as requirements.txt)

or

`pip install Flask==1.1.2`

(Flask 1.1.2 is confirmed to work but any version should work since there are no possible dependency conflicts)