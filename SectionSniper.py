from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import Config
import json
from pprint import pprint
from typing import Dict, List

import requests

# Get all terms: https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?dataType=json&offset=1&max=500
from requests import Response
def request_terms() -> List[Dict[str, str]]:
    """Performs a GET request for all terms in TAMU history"""
    url = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?dataType=json&offset=1&max=500"
    response: Response = requests.get(url)
    return json.loads(response.content)


def request_sections(dept: str, course_num: str, cookies):
    url = f"https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subjectcoursecombo={dept+course_num}&txt_term=201931&pageOffset=0&pageMaxSize=500&sortColumn=subjectDescription&sortDirection=asc"
    response = requests.get(url, cookies=cookies)
    return(json.loads(response.content))


def post_term(term_code: str):
    """Makes a POST request to set the desired term for consequent requests. Returns cookies"""
    url = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/term/search?mode=courseSearch"
    body = {
        "dataType": "json",
        "term": term_code
    }
    response: Response = requests.post(url, data=body)
    return response.cookies


def search(dept: str, course_num: str, sec: str):
    terms = request_terms()
    term_code = terms[0]["code"]
    term_cookies = post_term(term_code)
    database = request_sections(dept,course_num,term_cookies)
    pprint(database)


class Display(Widget):

    def init(self):
        print("initialize")


    def update(self, dt):
        pass

    def button_pressed(self):
        print("Department: ", self.ids.department.text)
        print("Course #: ", self.ids.course_num.text)
        print("Section #: ", self.ids.sec_num.text)
        search(self.ids.department.text, self.ids.course_num.text, self.ids.sec_num.text)



class SectionSniperApp(App):
    def build(self):
        display = Display()
        display.init()
        Clock.schedule_interval(display.update, 1.0)
        return display


if __name__ == '__main__':
    Config.set('graphics', 'width', '320')
    Config.set('graphics', 'height', '480')
    SectionSniperApp().run()