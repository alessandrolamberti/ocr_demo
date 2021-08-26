class Page:

    def __init__(self, name):
        self.name = name

    def dispatch(self):
        raise NotImplementedError


class Pages_View:

    def __init__(self):
        self.pages = []

    def get_pages_name(self):
        names = []

        for page in self.pages:
            names.append(page.name)

        return names

    def get_page_by_name(self, name):
        selected_page = None

        for page in self.pages:
            if page.name == name:
                selected_page = page
                break

        return selected_page

    def add_page(self, page):
        self.pages.append(page)