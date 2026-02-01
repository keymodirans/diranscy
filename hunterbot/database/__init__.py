"""
Package untuk database Hunterbot.
"""

from hunterbot.database.schema import init_database
from hunterbot.database.models import Video

__all__ = ["init_database", "Video"]
