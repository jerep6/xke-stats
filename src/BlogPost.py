from dataclasses import dataclass, field
from typing import List
import re
from functools import reduce
import mylogging


logger = mylogging.get_logger()

@dataclass
class BlogPost:
    keywords_not_content: List[str]
    authors_to_exclude: List[str]

    title: str
    publication_date: str
    modified_date: str
    authors: List[str] = field(default_factory=list)

    def get_type(self):
        is_author_backlist = True in [author in self.authors for author in self.authors_to_exclude]

        matches_title_blacklist = reduce(list.__add__, [re.findall(keyword.lower(), self.title.lower()) for keyword in self.keywords_not_content])
        logger.debug(f"Search 'other' keyword for article {self.title}, matches={matches_title_blacklist}")
        is_title_blacklist = len(matches_title_blacklist) > 0

        if not is_title_blacklist and not is_author_backlist:
            logger.info(f"Article {self.title} is kept because with matches={matches_title_blacklist}")
            return "ARTICLE_CONTENT"
        else:
            return "ARTICLE_OTHER"

    def __iter__(self):
        return iter([self.publication_date, self.title, ",".join(self.authors), self.get_type()])
