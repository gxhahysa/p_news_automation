import feedparser
from tests.config import RSS_FEEDS


class FeedFetcher:
    def __init__(self, feed_identifier):
        # If the identifier is a key in our config, use the corresponding URL
        if feed_identifier in RSS_FEEDS:
            self.url = RSS_FEEDS[feed_identifier]
        else:
            # Otherwise, assume it's a direct URL
            self.url = feed_identifier

        self.feed = None
    def fetch_feed(self):
        self.feed = feedparser.parse(self.url)

        if not self.feed.entries:
            print("No entries found or feed is empty.")
            return False

        # Sort entries by published date (newest first)
        self.feed.entries.sort(
            key=lambda entry: entry.published_parsed if hasattr(entry, "published_parsed") else 0,
            reverse=True
        )
        return True

    def get_first_entry(self):
        if not self.fetch_feed():
            return None

        first_entry = self.feed.entries[0]
        return {
            "title": first_entry.title,
            "link": first_entry.link,
            "published": first_entry.published,
            "description": first_entry.summary
        }

    def get_first_entry_title(self):
        if not self.feed or not self.feed.entries:
            print("Feed is empty or not fetched.")
            return None

        first_entry = self.feed.entries[0]
        return first_entry.title

    def get_first_entry_description(self, word_limit=10):

        if not self.feed or not self.feed.entries:
            print("Feed is empty or not fetched.")
            return None

        first_entry = self.feed.entries[0]
        description = first_entry.summary

        # Split the description into words and limit to the first 'word_limit' words
        description_words = description.split()[:word_limit]

        # Join the first 'word_limit' words back into a string
        limited_description = " ".join(description_words)

        return limited_description
