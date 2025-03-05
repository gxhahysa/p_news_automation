import feedparser
import time


class FeedFetcher:
    def __init__(self, url):
        self.url = url
        self.feed = None

    def fetch_feed(self, retries=3, delay=2):
        """Fetch and parse the RSS feed with retries."""
        for attempt in range(retries):
            print(f"Attempt {attempt + 1} to fetch feed...")
            self.feed = feedparser.parse(self.url)

            if self.feed.entries:
                print("Feed fetched successfully!")
                return True

            print(f"Failed to fetch feed. Retrying in {delay} seconds...")
            time.sleep(delay)

        print("No entries found or feed is empty after retries.")
        return False

    def ensure_feed_fetched(self):
        """Ensure the feed is fetched before accessing it."""
        if not self.feed or not self.feed.entries:
            print("Feed has not been fetched. Retrying...")
            return self.fetch_feed()
        return True

    def get_first_entry(self):
        """Get the first entry from the feed."""
        if not self.ensure_feed_fetched():
            return None

        first_entry = self.feed.entries[0]
        return {
            "title": first_entry.title,
            "link": first_entry.link,
            "published": first_entry.published,
            "description": first_entry.summary
        }

    def get_first_entry_title(self):
        """Get the title of the first entry."""
        if not self.ensure_feed_fetched():
            return None
        return self.feed.entries[0].title

    def get_first_entry_description(self):
        """Get the description of the first entry."""
        if not self.ensure_feed_fetched():
            return None
        return self.feed.entries[0].summary

    def print_first_entry(self):
        """Print details of the first entry."""
        if not self.ensure_feed_fetched():
            print("Failed to fetch the feed.")
            return

        entry = self.get_first_entry()
        if entry:
            print(f"Feed Title: {self.feed.feed.title}")
            print(f"Feed Link: {self.feed.feed.link}")
            print(f"\nFirst Entry Title: {entry['title']}")
            print(f"Link: {entry['link']}")
            print(f"Published: {entry['published']}")
            print(f"Description: {entry['description']}")
        else:
            print("No entries found.")
