"""Core RSS feed watcher logic"""

import feedparser
import json
import os
from datetime import datetime

class RSSWatcher:
    """RSS Feed Watcher"""
    
    def __init__(self, config):
        self.config = config
        self.state_file = config['state_file']
        self.seen_items = self._load_state()
    
    def _load_state(self):
        """Load previously seen items"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return set(json.load(f))
            except:
                return set()
        return set()
    
    def _save_state(self):
        """Save seen items to state file"""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(list(self.seen_items), f)
    
    def check_feeds(self):
        """Check all feeds for new items"""
        new_items = []
        
        for feed_url in self.config['feeds']:
            if not feed_url.strip():
                continue
                
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                item_id = entry.get('id', entry.get('link', ''))
                
                if item_id and item_id not in self.seen_items:
                    new_items.append({
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', '')
                    })
                    self.seen_items.add(item_id)
        
        if new_items:
            self._save_state()
        
        return new_items
