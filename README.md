# sendmail-gmail

A Python script that works a bit like sendmail except it uses the Gmail oauth API.

This script requires Python 3 to run

## Setup

1. Go to <https://developers.google.com/gmail/api/quickstart/python>, complete step 1 and save `credentials.json` as `.gmail_credentials.json` to the same directory as this script. Then pip install the requirements in step 2.
2. Copy the file `config.json.example` to `config.json`.
3. Set `rewrite_to` to change the `to` header to redirect all emails to a specific email address.
4. Set `console_oauth` to `false` to enable easier browser based authorisation flow. Set to `true` for console based authorisation flow if the system doesn't have have a desktop or web browser.
5. Run the script once without any arguments or input and follow the instructions in the console to complete the authorisation flow.

**Note:** The from address will always be the gmail account used to setup the script.


