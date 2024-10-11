import re
from math import ceil


class ArticleReadTimeEngin:
    @staticmethod
    def word_count( text):
        word = re.findall(r"\w+", text)
        return len(word)

    @staticmethod
    def estimate_time_reading(article, words_per_minutes=250,
                              seconds_per_imge=10, seconds_per_tags=2):
        word_count_body = ArticleReadTimeEngin.word_count(article.body)
        word_count_title = ArticleReadTimeEngin.word_count(article.title)
        word_count_description = ArticleReadTimeEngin.word_count(article.description)

        total_word_count = word_count_body+word_count_description+word_count_title

        reading_time = total_word_count / words_per_minutes

        if article.banner_image:
            reading_time +=seconds_per_imge/60

        tag_count = article.tag.count()

        reading_time += (tag_count*seconds_per_tags) /60
        reading_time = ceil(reading_time)

        return reading_time

        