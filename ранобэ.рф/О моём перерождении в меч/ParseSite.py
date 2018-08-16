from lxml import html

from selenium import webdriver

from time import sleep


def clean(text: str):
    # strings = ['?', "|", '.  Слава Королю  Ранобэ.рф', '\"', " Слава Королю Ранобэ.рф", '  Слава Королю  Ранобэ.рф']
    # result = (text.replace(i, "") for i in strings)
    # result = str()
    # for i in strings:
    #     print(i)
    #     result = text.replace(i, '')
    #     continue
    return text \
        .replace('?', '') \
        .replace("|", '') \
        .replace('.  О моем перерождении в меч  Ранобэ.рф', '') \
        .replace('\"', '') \
        .replace(" О моем перерождении в меч  Ранобэ.рф", '') \
        .replace('  О моем перерождении в меч Ранобэ.рф', '') \
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
        self.iterator = 1
        self.browser = web_driver
        self.timeout = timeout

    def start(self):
        self.parse_page()
        self.parse_links()

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

            sleep(0.2)
            self.browser.get(link)
            if len(self.browser.title) <= 15:
                sleep(0.3)
            if len(self.browser.title) <= 15:
                sleep(0.3)

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
        part = open('src/html/{}.html'.format(clean(self.browser.title)), 'w', encoding="utf-8")
        for i in self.__text_list:
            part.write(i)
        part.close()
        self.iterator += 1

    def parse_html(self):
        pass


if __name__ == '__main__':
    main = ParseSite()
    main.start()
