import nltk
from collections import Counter

# Download NLTK resources (run this line only once)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def get_most_common_noun_with_count(text):
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Tag each word with its part of speech
    tagged_words = nltk.pos_tag(words)
    
    # Filter out words that are not nouns
    nouns = [word for word, pos in tagged_words if pos.startswith('NN')]
    
    # Count the occurrences of each noun
    noun_counts = Counter(nouns)
    
    # Find the most common noun
    most_common_noun, count = noun_counts.most_common(1)[0] if noun_counts else (None, 0)
    
    return most_common_noun, count