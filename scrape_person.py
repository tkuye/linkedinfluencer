"""
CLI tool to scrape a linkedin influencer's profile by their username and create a csv with all their posts. 
"""

from argparse import ArgumentParser
from playwright.sync_api import sync_playwright

def main():
    """
    Main function
    """
    parser = ArgumentParser(description='Scrape a linkedin influencer\'s profile by their username and create a csv with all their posts.')
    
    parser.add_argument('--output', help='The output file name')
    parser.add_argument('input_file', help='The name of the input file, should have your linkedin login credentials and the name of the personality you want to clone.')
    args = parser.parse_args()

    if args.output:
        scrape_person(args.input_file, args.output)
    else:
        scrape_person(args.input_file)
    

def scrape_person(input_file:str, output:str ="output.csv"):
    """
    Scrapes the data from a linkedin personality and saves it to a csv file.
    Args:
        input_file (str): The name of the input file, should have your linkedin login credentials and the name of the personality you want to clone.
        output (str): What you would like the output file to be called.

    Raises:
        Exception: If no username, password or personality found in input file.  
    """
    login = dict()
    with open(input_file, 'r') as f:
        for line in f.readlines():
            logins = line.split('=')
            if len(logins) == 2:
                login[logins[0]] = logins[1].strip()
            
            
    if "username" not in login:
        raise Exception("No username found in input file")
    if "password" not in login:
        raise Exception("No password found in input file")
    if "personality" not in login:
        raise Exception("No personality found in input file")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://www.linkedin.com/login/uas')
        page.fill('#username', login['username'])
        page.fill('#password', login['password'])
        page.click('.btn__primary--large from__button--floating')


if __name__ == '__main__':
    main()