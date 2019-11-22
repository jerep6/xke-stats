import html
from BlogPost import BlogPost


class BlogPostBuilder:

    def __init__(self) -> None:
        self.title=None
        self.publication_date=None
        self.modified_date=None
        self.authors=None
        self.authors_to_exclude=None
        self.keywords_not_content=None

    def with_keywords_not_content(self, keywords_not_content):
        self.keywords_not_content = keywords_not_content
        return self

    def with_authors_to_exclude(self, authors_to_exclude):
        self.authors_to_exclude = authors_to_exclude
        return self

    def with_xdd_payload(self, payload: dict):
        default_author = payload['author']['username']
        authors = [author['name'] for author in payload.get('terms').get('authors', [])]

        self.title=html.unescape(payload['title'])
        self.publication_date=payload['created']
        self.modified_date=payload['created']
        self.authors=authors if len(authors) > 0 else [default_author]

        return self

    def build(self):
        return BlogPost(
            title=self.title,
            publication_date=self.publication_date,
            modified_date=self.modified_date,
            authors=self.authors,
            keywords_not_content = self.keywords_not_content,
            authors_to_exclude = self.authors_to_exclude
        )