import os, os.path

from lxml import html

from selenium import webdriver

from time import sleep

from collections import Counter


def clean(text: str):
    # strings = ['?', "|", '\"', ]
    # result = (text.replace(i, "") for i in strings)
    # result = str()
    # for i in strings:
    #     print(i)
    #     result = text.replace(i, '')
    #     continue
    return text \
        .replace('?', '') \
        .replace("|", '') \
        .replace('Ранобэ.рф', '') \
        .replace('\"', '') \
        .replace("О моём перерождении в слизь", '') \
        .replace('  ', '') \
        .replace(':', '') \
        .replace('\\', '') \
        .replace('/', '') \
        .replace('>', '') \
        .replace('<', '') \
        .replace('"', '') \
        .replace('+', '') \
        .replace('*', '') \
        .replace(' .', '')


class ParseSite:
    def __init__(self, file="src/link_pages.html", links_save="src/links.html", web_driver=webdriver.Firefox(),
                 timeout=10):
        self.file = file
        self.link_list = list()
        self.loaded_html = str()
        self.links_save = links_save
        self.__text_list = list()
        self.__html_title = str()
        self.iterator = 0
        self.browser = web_driver
        self.timeout = timeout
        self.home_directory = os.getcwd() 

    def start(self):
        self.parse_page()
        # self.parse_links()
        self.check_files()
        self.parse_files()

    def parse_page(self):
        html_src = open(self.file, 'r', encoding="utf-8")

        for i in html_src:
            self.loaded_html += i

        html_src.close()

        tree = html.fromstring(self.loaded_html)

        links = tree.xpath('//div[@class="book__item-wrapper"]/a/@href')

        links_src = open(self.links_save, 'w', encoding="utf-8")
        links.reverse()  # Для порядка

        for i in links:
            links_src.write(i + '\n')

        links_src.close()

    def parse_links(self):
        with open(self.links_save, 'r', encoding="utf-8") as links_src:
            for i in links_src:
                self.link_list.append(i[:-1])

        links_src.close()
        for link in self.link_list:

            self.browser.get(link)
            while len(self.browser.title) <= 45:
                sleep(0.2)

            self.__text_list = self.browser.page_source
            try:
                self.save_text()
            except AttributeError:
                sleep(0.5)
                self.__text_list = self.browser.page_source
                self.save_text()

            if link == self.link_list[-1]:
                self.browser.close()
                exit()

    def save_text(self):
        tree = html.fromstring(self.__text_list)
        a = clean(tree.xpath('//title')[0].text)
        print(a)
        partName = str(self.iterator)+". "+self.browser.title
        part = open(\
            'src/html/{}.html'.format(clean(partName)),\
             'w', encoding="utf-8")
        for i in self.__text_list:
            part.write(i)
        part.close()
        self.iterator += 1

    def check_files(self):
        files = os.listdir('src\\html')
        number_files = list([int(i.split('. ')[0]) for i in files])
        len_files = list(range(0, len(files)))
        uniques_list = list(set(number_files))
        check_list = list(set(len_files) - set(number_files))

        counter_list = Counter(number_files)

        non_uniqueness_list = list()
        for z in counter_list:
            if counter_list[z] > 1:
                non_uniqueness_list.append(z)
        non_uniqueness_list.sort()
        if check_list and non_uniqueness_list:
            print("Not foud:")
            for g in check_list:
                print(g)
            print('\n\nRepeating files:')
            for h in non_uniqueness_list:
                print(h)
            print("\n\n                FAIL")
        elif check_list:
            print("Not foud:")
            for g in check_list:
                print(g)
            print("\n\n                FAIL")
        elif non_uniqueness_list:
            for h in non_uniqueness_list:
                print(h)
            print("\n\n                FAIL")
        else:
            print("\n\n                OK")
        input()

    def parse_files(self):
        files = os.listdir('src\\html')
        result = open('result/parts.html', 'a', encoding="utf-8")
        result.write(\
            "<!DOCTYPE html>\n"+\
            "<html lang=\"ru\">\n"+\
            "<head>\n"+\
            "    <meta charset=\"UTF-8\">\n"+\
            "    <title>О моём превращении в слизь</title>\n"+\
            "</head>\n"+\
            "<body>\n"\
            )
        for i in files:
            html_text = ""
            text = ""
            part = open('src/html/{}'.format(i), 'r', encoding="utf-8")
            for g in part:
                html_text += g
            tree = html.fromstring(html_text)
            for z in tree.xpath('//div/p'):
                print(z.text)
                try:
                    text += "<p>" + z.text + "</p>"
                except TypeError:
                    continue
            part.close()
            result.write(text+"\n")
        result.write(\
            "\n</body>\n"+\
            "</html>")
        result.close()



if __name__ == '__main__':
    main = ParseSite()
    main.start()
