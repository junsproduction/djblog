from django import template
import re
import math

register = template.Library()

@register.filter
def reading_time(content):
    """Calculate estimated reading time for content"""
    if not content:
        return "1 min read"
    
    # Remove HTML tags and count words
    text = re.sub(r'<[^>]+>', '', str(content))
    word_count = len(text.split())
    
    # Average reading speed is 200-250 words per minute
    # We'll use 200 for a conservative estimate
    reading_time_minutes = math.ceil(word_count / 200)
    
    if reading_time_minutes < 1:
        return "1 min read"
    elif reading_time_minutes == 1:
        return "1 min read"
    else:
        return f"{reading_time_minutes} min read"

@register.filter
def word_count(content):
    """Count words in content"""
    if not content:
        return 0
    
    text = re.sub(r'<[^>]+>', '', str(content))
    return len(text.split())