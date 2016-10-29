"""
Usage:
    google_explorer.py --dork=<arg> --browser=<arg> [--exploit_parser=<arg>]
                                                    [--language=<arg>]
                                                    [--location=<arg>]
                                                    [--last_update=<arg>]
                                                    [--google_domain=<arg>]

    google_explorer.py --help
    google_explorer.py --version

Options:
    -h --help                                Open help menu
    -v --version                             Show version

Required options:
    --dork='google dork'                     your favorite g00gle dork :)
    --browser='browser'                      chrome
                                             chromium


Optional options:
    --language='page language'               Portuguese
                                             English
                                             Arabic
                                             Romanian
                                             ...
                                             ...

    --location='server location'             Brazil
                                             Mauritania
                                             Tunisia
                                             Marroco
                                             Japan
                                             ...
                                             ...

    --last_update='page last update'         anytime
                                             past 24 hours
                                             past week
                                             past month
                                             past year

    --google_domain='google domain'          google domain to use on search.
                                             Ex: google.co.uk


"""

import os
import sys
import time

from docopt import docopt, DocoptExit
from lxml import html as lh

from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


filter_names = ['language', 'location', 'last_update', 'google_domain']


class GoogleScanner:

    @staticmethod
    def banner():
        os.system('clear')
        print("\n")
        print(" █████╗ ███╗   ██╗ █████╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗██████╗ ")
        print("██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗")
        print("███████║██╔██╗ ██║███████║██████╔╝██║     ██║   ██║██║  ██║█████╗  ██████╔╝")
        print("██╔══██║██║╚██╗██║██╔══██║██╔══██╗██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗")
        print("██║  ██║██║ ╚████║██║  ██║██║  ██║╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║")
        print("╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝")
        print("\t  g00gle maSS ExPLOReR - anarcoder at protonmail.com\n")

    def __init__(self, dork, browser, filters):
        self.dork = dork
        self.browser = browser
        self.filters = filters
        self.driver = self.validate_browser()

    def validate_browser(self):
        browser = self.browser
        browser_path = ''

        browsers_names = ['chrome', 'chromium']

        if browser not in browsers_names:
            print('[###] No option for this browser [###]\n')
            print('Your current options are: \n')
            for b in browsers_names:
                print('- ' + b)
            print("\nIf you dont have any of them sorry for you =)..\n")
            sys.exit(1)

        if browser == 'chromium':
            browser_path = '/usr/bin/chromium'

        if browser == 'chrome':
            browser_path = '/usr/bin/google-chrome-stable'

        opts = Options()
        opts.binary_location = browser_path
        driver = webdriver.Chrome(chrome_options=opts)
        driver.wait = WebDriverWait(driver, 20)
        return driver

    def go_to_advanced_search_page(self):
        tools_button = "//*[@id='ab_opt_icon']"
        advanced_search_option = "//*[@id='ab_as' and "\
                                 "@href[contains(.,'/advanced_search')]]"
        driver = self.driver
        driver.wait.until(EC.presence_of_element_located((
            By.XPATH, tools_button))).click()
        time.sleep(1)
        driver.wait.until(EC.presence_of_element_located((
            By.XPATH, advanced_search_option))).click()

    def wait_for_presence(self, xpath):
        return self.driver.wait.until(EC.presence_of_element_located((
            By.XPATH, xpath)))

    def wait_for_clickable(self, xpath):
        self.wait_for_presence(xpath)
        return self.driver.wait.until(EC.element_to_be_clickable((
            By.XPATH, xpath)))

    def validate_and_select_option(self, option, options, option_button,
                                   argument_name):
        if option not in options:
            print("\n[###] No option for this argument... [###]\n")
            print("[*] The argument --" + argument_name +
                  " dont contains option: " + option)
            print("[*] Your current options are: \n")
            for op in options:
                print(op)
            sys.exit(1)

        for _ in range(options.index(option) + 1):
            self.wait_for_presence(option_button).send_keys(Keys.ARROW_DOWN)

        self.wait_for_presence(option_button).send_keys(Keys.RETURN)

    def apply_filters(self):
        f = self.filters
        self.go_to_advanced_search_page()

        if f['language']:
            language_options_xpath = "//ul[@id='lr_menu']/li/div/text()"
            language_button = "//*[@id='lr_button']"
            arg = 'language'
            content = self.driver.page_source
            options = lh.fromstring(content)
            language_options = [op for op in options.xpath(
                language_options_xpath)]
            self.validate_and_select_option(f['language'], language_options,
                                            language_button, arg)

        if f['location']:
            location_options_xpath = "//ul[@id='cr_menu']/li/div/text()"
            location_button = "//*[@id='cr_button']"
            arg = 'location'
            content = self.driver.page_source
            options = lh.fromstring(content)
            location_options = [op for op in options.xpath(
                location_options_xpath)]
            self.validate_and_select_option(f['location'], location_options,
                                            location_button, arg)

        if f['last_update']:
            last_update_options_xpath = "//ul[@id='as_qdr_menu']/li/div/text()"
            last_update_button = "//*[@id='as_qdr_button']"
            arg = 'last_update'
            content = self.driver.page_source
            options = lh.fromstring(content)
            last_update_options = [op for op in options.xpath(
                last_update_options_xpath)]
            self.validate_and_select_option(f['last_update'],
                                            last_update_options,
                                            last_update_button, arg)

        # Making the search
        search_button = '//input[@type="submit"]'
        self.wait_for_clickable(search_button).click()

    def check_page_loaded(self):
        driver = self.driver
        navigation_bar_xpath = "//*[@id='foot']"
        try:
            driver.wait.until(EC.presence_of_element_located((
                By.XPATH, navigation_bar_xpath)))
            captcha = 'xxx'
            return captcha
        except:
            captcha = None
            return captcha
            pass

    def write_results_to_file(self, results, filename):
        with open(filename, 'a') as f:
            for res in results:
                f.write(res + '\n')

    def result_parser(self):
        driver = self.driver

        print('[+] Starting parse search engine..')
        print('[+] Take a look at the screen to wait the captcha shows,'
              ' and type it')
        print('[+] The default time to wait you type the captcha is 20s')

        # Wait until captcha is checked
        check_page = self.check_page_loaded()
        while check_page is None:
            check_page = self.check_page_loaded()

        # Html parser and check if have a next page on pagination
        try:
            driver.wait.until(EC.presence_of_element_located((
                By.ID, "pnnext")))
            next_page = driver.find_element_by_id("pnnext")
        except:
            next_page = 'xxx'
            pass

        while next_page is not None:
            print('parsing links from page..')
            links_xpath = ".//*[@id='rso']//h3/a[@onmousedown and @href]/@href"
            content = self.driver.page_source
            options = lh.fromstring(content)
            results = [link for link in options.xpath(links_xpath)]

            self.write_results_to_file(results, 'google_results.txt')

            try:
                next_page = driver.find_element_by_id("pnnext")
                next_page.click()
                time.sleep(2)
                driver.wait.until(EC.presence_of_element_located((
                    By.XPATH, ".//*[@id='nav']")))
            except:
                break

        driver.close()

    def check_google_domain(self, google_domain):
        google_url = 'http://www.google.com.br'
        google_domains_list = open('google_domains.txt').read().splitlines()

        url_parsed = urlparse(google_domain)

        if 'www' in url_parsed.path or 'www' in url_parsed.netloc:
            print('\n[####] Please just put google domain in --google_domain'
                  'argument Ex: --google_domain="google.co.uk" [####]')
            print('Your option was: {0}'.format(google_domain))
            sys.exit(1)

        if url_parsed.path in google_domains_list:
            return 'http://www.' + url_parsed.path
        else:
            print('\n[+] Your current option was not find in google'
                  ' domains list: {0}'.format(google_domain))
            print('[+] Setting brazillian google as default =)))')
            return google_url

    def start_search(self):
        self.banner()

        driver = self.driver
        f = self.filters
        dork = self.dork

        # Checking google domain to search
        google_url = 'http://www.google.com.br'
        if f['google_domain']:
            google_url = self.check_google_domain(f['google_domain'])

        # Making the search
        driver.get(google_url)
        search_bar = driver.find_element_by_name("q")
        search_bar.send_keys(dork)
        search_bar.send_keys(Keys.RETURN)
        try:
            driver.wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[@id='nav']")))
        except:
            sys.exit(1)

        # Apply filters in arguments if necessary
        filters = dict((key, value) for key, value in f.items())
        if any(x is not None for x in filters.values()):
            self.apply_filters()

        self.result_parser()
        time.sleep(5)


def main():
    try:
        arguments = docopt(__doc__, version="anarc0der Google Explorer - 2016")
        dork = arguments['--dork']
        browser = arguments['--browser']
        filters = {name: arguments['--%s' % name] for name in filter_names}

    except DocoptExit as e:
        GoogleScanner.banner()
        os.system('python google_explorer.py --help')
        sys.exit(1)

    myScan = GoogleScanner(dork, browser, filters)
    myScan.start_search()


if __name__ == '__main__':
    main()
