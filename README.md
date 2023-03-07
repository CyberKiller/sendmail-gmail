# sendmail-gmail

A Python script that works a bit like sendmail except it uses the Gmail oauth API.

This script requires Python 3 to run

## Setup

1. Go to "[Set up you environment](https://developers.google.com/gmail/api/quickstart/python#set_up_your_environment)" in the google gmail python quickstart guide and complete the steps [Enable the API](https://developers.google.com/gmail/api/quickstart/python#enable_the_api) and [Authorize credentials for a desktop application](https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application) then save `credentials.json` as `.gmail_credentials.json` to the same directory as this script. 
2. Then go to: [Install the Google client library](https://developers.google.com/gmail/api/quickstart/python#install_the_google_client_library) and pip install the listed requirements (I recommend using a python virtual environment for this).
3. Copy the file `config.json.example` to `config.json`.
4. Set `rewrite_to` in the config to change the `to` header to redirect all emails to a specific email address. Set to `false` to disable `to` header writing.
5. ~~Set `console_oauth` in the config to `false` to enable easier browser based authorisation flow. Set to `true` for console based authorisation flow if the system doesn't have have a desktop or web browser.~~ **Unforntunatly google has disabled console based oauth_flow so this feature isn't available anymore.**
6. Run the script once without any arguments or input and follow the instructions in the console to complete the authorisation flow.

### Notes

* The from address will always be the gmail account used to setup the script.
* The config file is optional but the script will still display an error about being unable to read the config.
* For the browser based authentification on a machine without GUI support you may be able to use a console based web browser in another console or ssh session but I haven't personally tested this.
* ~~Alternatively configure the auth server in the config file to listen outside of localhost and open the machine on another browser.~~ It seems google doesn't allow this either... **I do not recommend exposing the auth server to the internet or to untrusted local networks!**