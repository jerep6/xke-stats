import boto3
import json
import mylogging
from typing import List
import csv
import io
from BlogPost import BlogPost
from BlogPostBuilder import BlogPostBuilder

logger = mylogging.get_logger()


class FactoryBlogPost:
    instance = None

    def __init__(self) -> None:
        self.keywords_to_exclude = self.__read_file_content_as_list("title.exclude.txt")
        self.authors_to_exclude = self.__read_file_content_as_list("author.exclude.txt")

    @staticmethod
    def get_instance():
        if FactoryBlogPost.instance is None:
            return FactoryBlogPost()
        else:
            return FactoryBlogPost.instance

    def __read_file_content_as_list(self, file_path):
        from pathlib import Path
        return Path(file_path).read_text().split("\n")

    def get_blog_post_builder(self) -> BlogPostBuilder:
        return BlogPostBuilder() \
            .with_authors_to_exclude(self.authors_to_exclude) \
            .with_keywords_not_content(self.keywords_to_exclude)


class BlogPostUtils:

    def __init__(self, s3_client) -> None:
        self.s3_client = s3_client
        self.file_titles_to_exclude = "title.exclude.txt"
        self.file_authors_to_exclude = "author.exclude.txt"

    def get_post_of_month(self, year: int, month: int) -> List[BlogPost]:
        logger.info(f"Get posts for year={year} and month={month}")
        key = f"{prefix}/{year:02}-{month:02}.json"

        params = {
            "Bucket": bucket_name,
            "Key": key
        }
        logger.debug("Get blog json file with params %s", params)
        content = self.s3_client.get_object(**params)['Body'].read().decode('utf-8')

        posts = json.loads(content)
        return [FactoryBlogPost.get_instance().get_blog_post_builder().with_xdd_payload(post).build() for post in posts]

    def get_post_of_year(self, year: int) -> List[BlogPost]:
        year_posts = []

        for n in range(1, 13):
            month_posts = self.get_post_of_month(year, n)
            year_posts.extend(month_posts)

        return year_posts

    def generate_csv(self, articles: List[BlogPost]):
        output = io.StringIO()
        writer = csv.writer(output, delimiter=';')
        for row in articles:
            writer.writerow(list(row))

        return output.getvalue()

if __name__ == "__main__":
    bucket_name = "xdd-datalake-dev.xebia.fr"
    prefix = "raw/blog-posts/2019/11/18"

    s3_client = boto3.client('s3')

    blog_post_utils = BlogPostUtils(s3_client)

    all_posts: List[BlogPost] = blog_post_utils.get_post_of_year(2018)

    # print("\n".join([ article.title for article in articles_de_fond]))
    print(blog_post_utils.generate_csv(all_posts))
