import json
import csv
import requests

API_KEY = ''
with open('keyfile.json') as keyfile:
    keyfile = json.loads(keyfile.read())
    API_KEY = str(keyfile['propublica_api_key'])
API_URL = 'https://api.propublica.org/congress/v1/'
MEMBER_ENDPOINT = '{congress}/{chamber}/members.json'
RECENT_BILL_ENDPOINT = '{congress}/{chamber}/bills/{type}.json'
API_HEADERS = {'X-API-Key':API_KEY}

def get_page(endpoint, **kwargs):
    """Uses the requests library to send a get request to ProPublica
    for a URL endpoint type and authenication headers.

    Keyword Arguments
    endpoint -- URL Endpoint type
    **kwargs -- Used to pass arguments to the URL string for dynamic URL creation
    """

    url = API_URL
    ### "member" is used to select the congressional members ###
    if endpoint == 'member':
        url += MEMBER_ENDPOINT.format(**kwargs)
    ### "recent_bill" is used to select the 20 most recent bills ###
    elif endpoint == 'recent_bill':
        url += RECENT_BILL_ENDPOINT.format(**kwargs)
    ### Make the request ###
    r = requests.get(url,headers=API_HEADERS)
    print(r.status_code)
    ### Return request body loaded as a JSON object ###
    return json.loads(r.text)

def print_json_file(name, txt):
    """Takes a JSON object and prints it out to a file"""
    with open(name, 'w') as out_file:
        out_file.write(json.dumps(txt))

def print_pretty_json_file(name, txt):
    """Takes a JSON object and prints it out to a file.
    Output is sorted and indented for easy viewing"""
    with open(name, 'w') as out_file:
        out_file.write(json.dumps(txt, sort_keys=True, indent=4))

def print_csv_members(name, txt):
    """Used to output a list of congressional members to a CSV file
    Output is pipe ("|") delimited and contains one header row.
    """
    with open(name, 'w', newline='') as csvfile:
        ### Initialize CSV Writer ###
        csv_writer = csv.writer(csvfile, delimiter='|',
                                quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        ### Write header line to file ###
        headers = sorted(txt['results'][0]['members'][0].keys())
        csv_writer.writerow(headers)
        ### Loop through all results given ###
        for congress in txt['results']:
            ### Loop through all members for each result ###
            for member in congress['members']:
                temp_row = []
                ### Loop through the headers in order to pull out each key ###
                for key in headers:
                    try:
                        temp_row.append(member[key])
                    ### If key doesn't exist, append an empty string ###
                    except KeyError:
                        temp_row.append('')
                csv_writer.writerow(temp_row)

def print_csv_bills(name, txt):
    """Used to output a list of bills to a CSV file
    Output is pipe ("|") delimited and contains one header row.
    Python collections are cast as a string and left unformatted.
    """
    with open(name, 'w', newline='') as csvfile:
        ### Initialize CSV Writer ###
        csv_writer = csv.writer(csvfile, delimiter='|',
                                quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        ### Write header line to file ###
        headers = sorted(txt['results'][0]['bills'][0].keys())
        csv_writer.writerow(headers)
        ### Loop through all results given ###
        for congress in txt['results']:
            ### Loop through all bills given for each result ###
            for bill in congress['bills']:
                temp_row = []
                ### Loop through the headers in order to pull out each key ###
                for key in headers:
                    try:
                        temp_row.append(str(bill[key]))
                    ### If key doesn't exist, append an empty string ###
                    except KeyError:
                        temp_row.append('')
                csv_writer.writerow(temp_row)

def get_all_members(congress):
    """Get all members of congress for a specified Congress"""
    ### First get the Senate Members ###
    mem_params = {'congress':congress,'chamber':'senate'}
    members = get_page('member', **mem_params)

    ### Then get the House Members ###
    mem_params['chamber'] = 'house'
    temp_members = get_page('member', **mem_params)
    members['results'].append(temp_members['results'][0])

    ### Print to files ###
    print_json_file('congress_' + str(congress) + '_members.json', members)
    print_pretty_json_file('congress_' + str(congress) + '_members_pretty.json', members)
    print_csv_members('congress_' + str(congress) + '_members.csv', members)

def get_recent_bills(congress):
    """Get the most recently updated 20 bills from Congress"""
    ### Get All Recent Bills ###
    bill_params = {'congress':congress,'chamber':'both','type':'updated'}
    bills = get_page('recent_bill', **bill_params)

    ### Print to files ###
    print_json_file('congress_' + str(congress) + '_recent_bills.json', bills)
    print_pretty_json_file('congress_' + str(congress) + '_recent_bills_pretty.json', bills)
    print_csv_bills('congress_' + str(congress) + '_recent_bills.csv', bills)

if __name__ == "__main__":
    get_all_members(115)
    get_recent_bills(115)