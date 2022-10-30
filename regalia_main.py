# Main operation of Regalia tool

# How should inputs be utilized?
#     1. What exchanges should be looked at?
#     2. What assets/tickers should be looked at?
#
# Idea 1: User sets up input configuration
# Idea 2: Configuration is set in a file in the repository and the user is expected to customize it appropriately

from constants import ALL_EXCHANGES


def validate_config(user_preference_config):
    """Ensures a configuration is acceptable."""
    exchanges = user_preference_config.get('exchanges')
    assets = user_preference_config.get('assets')
    for exchange in exchanges:
        if exchange not in ALL_EXCHANGES:
            return False

    for asset in assets:
        if len(asset) < 2 or len(asset) > 10:
            return False

    return True
