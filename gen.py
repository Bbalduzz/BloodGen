from playwright.sync_api import sync_playwright
import requests
from random import choices
from time import sleep
from rich.console import Console
from rich.table import Table
import os
import warnings
import zipfile
from src.names import generate_name
from src.gmailnator import GmailNator

# Constants
BASE_URL = 'https://bloodhunt.com/en-us/create-account'
warnings.filterwarnings("ignore", category=DeprecationWarning)

class BloodGen():
    def __init__(self):
        self.console           = Console()
        self.gmailnator        = GmailNator()
        self.update_extension()
        self.email             = self.gmailnator.generate()
        self.name              = generate_name()
        self.password          = ''.join(choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8))

    def download_and_unzip(self, url, extract_to='.', zip_name='temp'):
        response = requests.get(url)
        zip_file_name = f'{zip_name}.zip'
        with open(zip_file_name, 'wb') as file:
            file.write(response.content) 
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_file_name)

    def update_extension(self):
        with self.console.status("[bold green]Updating Extension...") as status:
            releases = requests.get("https://api.github.com/repos/Wikidepia/hektCaptcha-extension/releases").json()
            for release in releases:
                if release["target_commitish"] == "recaptcha":
                    tag_name = release["tag_name"]
                    self.download_and_unzip(url=release["assets"][0]["browser_download_url"], extract_to="solver", zip_name=tag_name)
            self.console.print(":heavy_check_mark: Extension Updated")
            self.console.print(f"   └── [bold green]version: [bold yellow]{tag_name}")
            self.path_to_extension = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solver")

    def fill_form(self, page):
        with self.console.status("[bold green]Filling Form...") as status:
            page.wait_for_selector('xpath=//*[@id="username"]')
            page.fill('xpath=//*[@id="username"]', self.name)
            page.fill('xpath=//*[@id="email"]', self.email)
            page.fill('xpath=//*[@id="password"]', self.password)
            page.fill('xpath=//*[@id="password-confirm"]', self.password)
            page.click('xpath=//*[@id="account"]/div[1]/div[12]/div[1]/div/div')
            page.click('xpath=//*[@id="choices--day-item-choice-2"]')
            page.click('xpath=//*[@id="account"]/div[1]/div[12]/div[2]/div/div')
            page.click('xpath=//*[@id="choices--month-item-choice-2"]')
            page.click('xpath=//*[@id="account"]/div[1]/div[12]/div[3]/div/div')
            page.click('xpath=//*[@id="choices--year-item-choice-25"]')
            page.click('xpath=//*[@id="account"]/div[1]/div[13]/div[1]')
            page.click('xpath=//*[@id="account"]/div[1]/div[14]/div[1]')
            page.click('xpath=//*[@id="block-lonelyfish-content"]/div/section/div/div/div[7]/button')
            self.console.print(":heavy_check_mark: [bold]Form[/bold] Filled")
            self.console.print(f"   ├── [bold green]username: [bold yellow]{self.name}")
            self.console.print(f"   ├── [bold green]email: [bold yellow]{self.email}")
            self.console.print(f"   └── [bold green]password: [bold yellow]{self.password}")

    def wait_for_verification_code(self):
        with self.console.status("[bold green]Waiting for verification code...") as status:
            not_received = True
            while not_received:
                inbox = self.gmailnator.inbox(self.email)
                if inbox != []:
                    not_received = False
            msg_id = [data['messageID'] for data in inbox if data['messageID'] != 'ADSVPN'][0]
            verification_code = self.gmailnator.get_message(msg_id, self.email)
            self.console.print(":heavy_check_mark: [bold]Verification code[/bold] received")
            self.console.print(f"   └── [bold green]code: [bold yellow]{verification_code}")

            return verification_code

    def submit_verification_code(self, page, verification_code):
        with self.console.status("[bold green]Submitting verification code...") as status:
            for n, c in enumerate(verification_code): 
                page.fill(f'#number{n+1}', c)
            page.click('xpath=//*[@id="block-lonelyfish-content"]/div/section/div/div/div[7]/button')
            self.console.print(":heavy_check_mark: Verification code submitted")

    def recaptcha_detection(self, page):
        if captcha := page.locator("//iframe[@title='reCAPTCHA']"):
            with self.console.status("[bold green]Solving reCaptcha...") as status:
                sleep(5)
                self.console.print(":heavy_check_mark: reCaptcha solved")
                self.console.print(f"   └── [bold green]name: [bold yellow]{captcha.get_attribute('name')}")

    def run(self, playwright):
        user_dir = 'bloodgen_user'
        if not os.path.exists(user_dir): os.makedirs(user_dir)
        context = playwright.chromium.launch_persistent_context(
            user_dir,
            headless=False,
            args=[
                f"--disable-extensions-except={self.path_to_extension}",
                f"--load-extension={self.path_to_extension}",
            ],
        )
        context.add_cookies([{"name": "agegate", "value": "1", "domain": "bloodhunt.com", "path": "/"}])
        page = context.new_page()
        page.goto(BASE_URL)
        self.fill_form(page)
        self.recaptcha_detection(page)
        verification_code = self.wait_for_verification_code()
        self.submit_verification_code(page, verification_code)
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")
        table.add_row(self.email, self.name, self.password)
        self.console.print(table)
        
    def create(self):
        with sync_playwright() as playwright:
            self.run(playwright)

if __name__ == "__main__":
    g = BloodGen()
    g.create()
