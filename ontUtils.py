#links
LINK_PREDICATE="https://raw.githubusercontent.com/CapsaDragosGabriel/KnowledgeGraph/refs/heads/main/attempt.ttl"
LINK_SUBJECT="https://raw.githubusercontent.com/CapsaDragosGabriel/KnowledgeGraph/refs/heads/main/attempt.ttl"

def change_title(snake_str):
    words = snake_str.split('_')
    capitalized_words = [word.capitalize() for word in words]
    return '_'.join(capitalized_words)

def hello():
    return print("hi")