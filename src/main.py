#!/usr/bin/env python3
"""Anime RSS Watcher - Main Entry Point"""

import time
import sys
from config import load_config
from core import RSSWatcher
from notify import send_notification

def main():
    """Main application loop"""
    try:
        config = load_config()
        watcher = RSSWatcher(config)
        
        print("Anime RSS Watcher started...")
        print(f"Monitoring {len(config['feeds'])} feed(s)")
        
        while True:
            new_items = watcher.check_feeds()
            
            for item in new_items:
                print(f"New: {item['title']}")
                if config.get('notifications_enabled', False):
                    send_notification(item['title'], item['link'])
            
            time.sleep(config.get('check_interval', 300))
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
