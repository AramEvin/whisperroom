import secrets

ADJECTIVES = [
    'silent', 'hidden', 'ghost', 'dark', 'quick', 'calm', 'wild',
    'lost', 'cool', 'pale', 'swift', 'brave', 'grim', 'odd', 'shy',
    'bold', 'dim', 'keen', 'raw', 'soft',
]

NOUNS = [
    'panda', 'fox', 'wolf', 'crow', 'moth', 'lynx', 'hawk', 'frog',
    'deer', 'bear', 'owl', 'crab', 'newt', 'vole', 'ibis', 'mink',
    'toad', 'wren', 'dace', 'kite',
]


def generate_nick() -> str:
    """Generate a random anonymous nickname like 'silent_fox'."""
    import random
    adj  = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f'{adj}_{noun}'


def generate_token() -> str:
    """Generate a secure random token for session persistence."""
    return secrets.token_hex(32)
