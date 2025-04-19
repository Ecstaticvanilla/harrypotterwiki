import random

def generate_inconsistent_examples(consistent_data, num_to_generate=5000):
    """Generates inconsistent examples based on the provided consistent data.

    Args:
        consistent_data (list): A list of dictionaries representing consistent
                                     statements (loaded from the JSON file).
            num_to_generate (int): The number of inconsistent examples to generate.

        Returns:
            list: A list of strings, where each string is an inconsistent example.
        """
    inconsistent_examples = []
    generated_count = 0

    all_characters = set()
    all_locations = set()
    for entry in consistent_data:
        if entry.get('characters'):
            all_characters.update(entry['characters'])
        if entry.get('location'):
            all_locations.add(entry['location'])

    all_characters = list(all_characters)
    all_locations = list(all_locations)

    def create_character_swap(entry):
        """Generates an inconsistent example by swapping a character."""
        if not entry.get('characters') or len(entry['characters']) < 1:
            return None  

        original_characters = entry['characters']
        other_characters = [c for c in all_characters if c not in original_characters]
        if not other_characters:
            return None  

        inconsistent_characters = random.sample(other_characters, min(len(original_characters), len(other_characters)))
        new_entry = entry.copy()
        new_entry['characters'] = inconsistent_characters

        original_summary = entry['summary']
        new_summary = original_summary
        for i in range(len(original_characters)):
            new_summary = new_summary.replace(original_characters[i], inconsistent_characters[i], 1)  # Replace only the first occurrence

        return f"{', '.join(inconsistent_characters)} {new_summary}"

    def create_location_swap(entry):
        """Generates an inconsistent example by swapping the location."""
        if not entry.get('location'):
            return None  # Cannot swap if no location

        original_location = entry['location']
        other_locations = [loc for loc in all_locations if loc != original_location]
        if not other_locations:
            return None
        inconsistent_location = random.choice(other_locations)
        new_entry = entry.copy()
        new_entry['location'] = inconsistent_location
        return original_summary.replace(original_location, inconsistent_location)  # Keep summary same, but replace location

    def create_negation(entry):
        """Generates an inconsistent example by negating the summary (simple negation)."""
        if not entry.get('summary'):
            return None

        original_summary = entry['summary']
        negated_summary = "not " + original_summary  # Very basic negation
        if "not not" in negated_summary:
            return original_summary.replace("not not ", "")
        return negated_summary

    def create_time_shift(entry):
        """Generates an inconsistent example by changing time-related words (very basic)."""
        if not entry.get('summary'):
            return None
        time_words = ["yesterday", "today", "tomorrow", "earlier", "later", "now", "then"]
        changed = False
        new_summary = entry['summary']
        for word in time_words:
            if word in new_summary:
                new_summary = new_summary.replace(word, random.choice(time_words))
                changed = True
        if changed:
            return new_summary
        return None

    def create_verb_change(entry):
        """Generates an inconsistent example by changing a verb in the summary."""
        if not entry.get('summary'):
            return None
        verbs = ["went", "said", "flew", "stayed", "took", "gave", "saw", "heard", "knew", "thought"]
        changed = False
        new_summary = entry['summary']
        for verb in verbs:
            if verb in new_summary:
                new_summary = new_summary.replace(verb, random.choice(verbs))
                changed = True
        if changed:
            return new_summary
        return None

    def create_object_swap(entry):
        """Generates an inconsistent example by swapping a key object."""
        if not entry.get('summary'):
            return None
        objects = ["wand", "broom", "potion", "stone", "cloak", "sword", "letter", "book"]
        changed = False
        new_summary = entry['summary']
        for obj in objects:
            if obj in new_summary:
                new_summary = new_summary.replace(obj, random.choice(objects))
                changed = True
        if changed:
            return new_summary
        return None

    def create_relationship_change(entry):
        """Generates an inconsistent example by changing a relationship."""
        if not entry.get('characters') or len(entry['characters']) < 2:
            return None
        relationships = ["father", "mother", "brother", "sister", "friend", "enemy", "teacher", "student"]
        changed = False
        new_summary = entry['summary']
        for relation in relationships:
            if relation in new_summary:
                new_summary = new_summary.replace(relation, random.choice(relationships))
                changed = True
        if changed:
            return new_summary
        return None

    def create_impossible_action(entry):
        """Generates an inconsistent example by describing an impossible action."""
        if not entry.get('characters'):
            return None
        character = random.choice(entry['characters'])
        impossible_actions = [
            f"{character} flew without a broom.",
            f"{character} cast a spell without a wand.",
            f"{character} Apparated to the moon.",
            f"{character} turned into a Muggle.",
            f"{character} understood Parseltongue without being a Parselmouth.",
            f"{character} walked through a wall at Hogwarts without magic."
        ]
        return random.choice(impossible_actions)

    def create_number_change(entry):
        """Generates an inconsistent example by changing a number."""
        if not entry.get('summary'):
            return None
        numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        changed = False
        new_summary = entry['summary']
        for number in numbers:
            if number in new_summary:
                new_summary = new_summary.replace(number, random.choice(numbers))
                changed = True
        if changed:
            return new_summary
        return None
        
    rule_functions = [
        create_character_swap,
        create_location_swap,
        create_negation,
        create_time_shift,
        create_verb_change,
        create_object_swap,
        create_relationship_change,
        create_impossible_action,
        create_number_change
    ]

    while generated_count < num_to_generate:
        base_entry = random.choice(consistent_data)

        rule_function = random.choice(rule_functions)

        inconsistent_example = rule_function(base_entry)
        if inconsistent_example:  
            inconsistent_examples.append(inconsistent_example)
            generated_count += 1

    return inconsistent_examples
    