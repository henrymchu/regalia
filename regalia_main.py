# Main operation of Regalia tool

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
