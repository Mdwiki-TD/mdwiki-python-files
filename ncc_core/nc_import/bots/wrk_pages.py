import wikitextparser as wtp
from nc_import.bots.import_files import import_file
from newapi import printe
from newapi.wiki_page import MainPage
"""
page      = MainPage(title, 'ar', family='wikipedia')
exists    = page.exists()
text      = page.get_text()
save_page = page.save(newtext='', summary='', nocreate=1, minor='')
"""


class PageWork:

    def __init__(self, code, title):
        self.code = code
        self.title = title
        self.temps = []
        self.page = MainPage(self.title, self.code, family="wikipedia")
        self.text = self.page.get_text()
        self.new_text = self.text

    def start(self):
        # ---
        if not self.page.exists():
            print(f"self.page {self.page} not exists!")
            return
        # ---
        self.get_temps()
        self.work_on_temps()
        self.save()

    def get_temps(self):
        # ---
        parsed = wtp.parse(self.text)
        # ---
        for temp in parsed.templates:
            # ---
            name = str(temp.normal_name()).strip().lower().replace("_", " ")
            # ---
            if name == "nc":
                self.temps.append(temp)
        # ---
        printe.output(f"{len(self.temps)} temps")

    def work_one_temp(self, temp):
        # args = temp.arguments
        # ---
        text = temp.string
        # ---
        file_name = ""
        caption = ""
        # ---
        if temp.get_arg("1"):
            file_name = temp.get_arg("1").value
        # ---
        if temp.get_arg("2"):
            caption = temp.get_arg("2").value
        # ---
        printe.output(f"<<purple>> File:<<default>> {file_name}")
        printe.output(f"<<purple>> caption:<<default>> {caption}")
        # ---
        done = import_file(file_name, self.code)
        # ---
        if done:
            new_temp = f"[[File:{file_name}|thumb|{caption}]]"
            return new_temp
        # ---
        return text

    def work_on_temps(self):
        # ---
        for temp in self.temps:
            string = temp.string
            # ---
            # {{NC|file name from NC Commons|caption}}
            temp_new_text = self.work_one_temp(temp)
            # ---
            if temp_new_text != string:
                self.new_text = self.new_text.replace(string, temp_new_text)

    def save(self):
        if self.new_text != self.text:
            self.page.save(newtext=self.new_text, summary="bot: fix NC")


def work_on_pages(code, pages):
    for numb, page_title in enumerate(pages, 1):
        print(f"{numb=}: {page_title=}:")
        bot = PageWork(code, page_title)
        bot.start()
