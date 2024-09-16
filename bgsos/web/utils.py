import random


def generate_random_name():
    # Adjectives
    adjectives = [
        "Adventurous", "Brave", "Calm", "Delightful", "Energetic", "Fearless", "Gentle", "Happy",
        "Inquisitive", "Joyful", "Kind", "Lively", "Merry", "Noble", "Optimistic", "Passionate",
        "Quirky", "Radiant", "Serene", "Thoughtful", "Unique", "Vibrant", "Witty", "Zealous",
        "Affectionate", "Brilliant", "Charming", "Daring", "Eager", "Friendly", "Gracious",
        "Humble", "Imaginative", "Jovial", "Keen", "Luminous", "Magnificent", "Nurturing",
        "Optimistic", "Playful", "Quiet", "Resilient", "Spirited", "Tenacious", "Upbeat",
        "Versatile", "Warm", "Xenial", "Youthful", "Zany", "Artistic", "Blissful", "Creative",
        "Determined", "Empathetic", "Fierce", "Generous", "Hopeful", "Inspiring", "Joyful",
        "Knowledgeable", "Loving", "Motivated", "Nostalgic", "Open-minded", "Persistent",
        "Quick-witted", "Resourceful", "Strong", "Talented", "Understanding", "Valiant",
        "Wise", "Zestful", "Ambitious", "Bold", "Confident", "Diligent", "Enthusiastic",
        "Fearless", "Grateful", "Honest", "Innovative", "Jubilant", "Kindhearted", "Logical",
        "Mindful", "Noble", "Optimistic", "Patient", "Quiet", "Reliable", "Sincere", "Trustworthy",
        "Uplifted", "Vigorous", "Wise", "Youthful", "Zesty", "Honey"
    ]

    # Colors
    colors = [
        "Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Black", "White", "Gray",
        "Brown", "Violet", "Indigo", "Turquoise", "Cyan", "Magenta", "Maroon", "Navy", "Gold",
        "Silver", "Bronze", "Emerald", "Jade", "Ruby", "Sapphire", "Amber", "Crimson", "Scarlet",
        "Lavender", "Peach", "Apricot", "Olive", "Teal", "Coral", "Ivory", "Chartreuse", "Fuchsia",
        "Amethyst", "Turquoise", "Obsidian", "Onyx", "Garnet", "Topaz", "Aquamarine", "Cerulean",
        "Periwinkle", "Vermilion", "Blush", "Caramel", "Chocolate", "Tan", "Khaki", "Mustard",
        "Burgundy", "Salmon", "Eggshell", "Pearl", "Sand", "Cherry", "Raspberry", "Mulberry",
        "Plum", "Cobalt", "Zinc", "Alabaster", "Ivory", "Charcoal", "Copper", "Honey", "Vanilla",
        "Mint", "Lemon", "Lime", "Tangerine", "Azure", "Mauve", "Ochre", "Sage"
    ]

    # Party Vibes
    party_vibes = [
        "Acid", "Groovy", "Funky", "Electric", "Disco", "Retro", "Neon", "Psychedelic",
        "Rave", "Wild", "Flashy", "Vibrant", "Zesty", "Festive", "Hypnotic", "Kooky"
    ]

    # Combine all adjectives
    adjectives.extend(colors)
    adjectives.extend(party_vibes)

    # Nouns
    nouns = [
        "Bear", "Eagle", "Lion", "Wolf", "Tiger", "Falcon", "Hawk", "Fox", "Panther", "Leopard",
        "Cheetah", "Jaguar", "Elephant", "Giraffe", "Zebra", "Horse", "Buffalo", "Rhino",
        "Hippo", "Monkey", "Chimpanzee", "Gorilla", "Orangutan", "Kangaroo", "Koala", "Panda",
        "Penguin", "Dolphin", "Whale", "Shark", "Octopus", "Turtle", "Frog", "Lizard", "Snake",
        "Crocodile", "Alligator", "Swan", "Peacock", "Parrot", "Owl", "Rabbit", "Squirrel",
        "Hedgehog", "Deer", "Moose", "Elk", "Caribou", "Bison", "Raccoon", "Otter", "Beaver",
        "Badger", "Porcupine", "Skunk", "Ferret", "Mongoose", "Meerkat", "Armadillo", "Sloth",
        "Antelope", "Gazelle", "Impala", "Wildebeest", "Gnu", "Okapi", "Yak", "Llama",
        "Alpaca", "Camel", "Dromedary", "Donkey", "Mule", "Horse", "Zebra", "Giraffe",
        "Elephant", "Hippo", "Rhino", "Tapir", "Pig", "Boar", "Warthog", "Hog", "Sheep",
        "Goat", "Lamb", "Ewe", "Ram", "Ox", "Bull", "Cow", "Calf", "Bison", "Buffalo",
        "Camel", "Dromedary", "Llama", "Alpaca", "Deer", "Moose", "Elk", "Caribou", "Reindeer",
        "Antelope", "Gazelle", "Impala", "Wildebeest", "Gnu", "Okapi", "Kudu", "Springbok",
        "Dik-dik", "Sitatunga", "Waterbuck", "Bushbuck", "Bongo", "Nyala", "Hartebeest",
        "Tsessebe", "Topi", "Bontebok", "Damaliscus", "Hirola", "Sable", "Roan", "Rhebok",
        "Chamois", "Ibex", "Goral", "Serow", "Takin", "Muskox", "Chinchilla", "Guinea Pig",
        # Additional nouns
        "Warrior", "Guardian", "Champion", "Hero", "Viking", "Samurai", "Knight", "Ranger",
        "Paladin", "Ninja", "Monk", "Mage", "Wizard", "Sorcerer", "Druid", "Rogue", "Hunter",
        "Barbarian", "Bard", "Cleric", "Shaman", "Seeker", "Sage", "Alchemist", "Scholar",
        "Swordsman", "Archer", "Spearman", "Cavalier", "Commander", "Scout", "Healer",
        "Protector", "Defender", "Avenger", "Conqueror", "Crusader", "Warden", "Sentinel",
        "Watcher", "Adventurer", "Explorer", "Pioneer", "Pathfinder", "Trailblazer", "Navigator",
        "Pilot", "Sailor", "Captain", "Mariner", "Buccaneer", "Pirate", "Corsair", "Raider",
        "Berserker", "Battler", "Fighter", "Gunner", "Sniper", "Lancer", "Gladiator", "Wrestler",
        # Party Vibes
        "Junkie", "Raver", "Reveler", "Partier", "Dancer", "Groover", "Rockstar", "DJ",
        "Performer", "Entertainer", "MC", "Beatboxer", "Juggler", "Magician", "Jester"
    ]

    # Ensure list has enough items for combinations
    nouns.extend([f"Animal{i}" for i in range(len(nouns), 203)])

    # Randomly select a color/emotion and an animal
    first_name = random.choice(adjectives)
    last_name = random.choice(nouns)

    print('hello', first_name, last_name)

    return first_name, last_name
