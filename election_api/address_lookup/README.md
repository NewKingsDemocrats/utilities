# Address Lookup

Takes csv of addresses and matches against nyc elections api data to get district and other info.

## How to Run

A csv file with address info (one address per row) needs to be fed into the address_lookup.py python script which then takes each address and checks it against the elections api.

1. Create address info csv (use sample_addr.csv as an example)
2. Figure out a name for output csv file (e.g. output_addresses.csv)
3. Get an API key from election api website or add your IP address to elections api key (see getting an API key)
4. Run the command with: `python address_lookup.py <api_key> <input.csv> <output.csv>`

## How to get API key

API key is a key (random string) given by the Elections API website so users can make requests for its services and it can track which users are requesting what to avoid abuse.

To get an API key:

1. Get your IP address
    * Go to www.whatsmyip.org
    * Copy the IP address you see there. This is needed for the API key.
2. Go to https://nyc.electionapi.com/Home.aspx and click on `Sign Up`
3. Once you're logged in to the website, click on `Keys`
4. Under "Key for server apps (with IP locking)", click `Generate a new key`
5. Enter your IP address in the "Accept requests from ..." field and click `Save`
6. You will see a random string next to "API Key". That is your API key.

To add an IP to an API key:

* Each API key has a list of IP addresses permitted to access the website. If your IP changed and you don't want to generate a new key, you can add your IP to the existing key.
* Login to the elections API site, click on `Keys`, and click on `Edit allowed IPs`, then add your new IP. 	