"""Configuration loader for Anime RSS Watcher"""

import os
from dotenv import load_dotenv

def load_config():
    """Load configuration from environment"""
    load_dotenv()
    
    return {
        'feeds': os.getenv('RSS_FEEDS', '').split(','),
        'check_interval': int(os.getenv('CHECK_INTERVAL', 300)),
        'notifications_enabled': os.getenv('NOTIFICATIONS_ENABLED', 'false').lower() == 'true',
        'state_file': os.getenv('STATE_FILE', 'src/data/last_state.json')
    }
