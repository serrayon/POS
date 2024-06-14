import ssl
import nltk
from nltk.corpus import treebank
from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger
from nltk.tokenize import word_tokenize

# Workaround for SSL certificate issues
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download necessary NLTK resources
nltk.download('treebank')
nltk.download('punkt')

# Load the treebank corpus
corpus = treebank.tagged_sents()

# Split the data into training and testing sets
train_data = corpus[:3000]
test_data = corpus[3000:]

# Define a backoff tagger
default_tagger = nltk.DefaultTagger('NN')
unigram_tagger = UnigramTagger(train_data, backoff=default_tagger)
bigram_tagger = BigramTagger(train_data, backoff=unigram_tagger)
trigram_tagger = TrigramTagger(train_data, backoff=bigram_tagger)

# Evaluate the tagger
accuracy = trigram_tagger.evaluate(test_data)
print(f'Tagger Accuracy: {accuracy * 100:.2f}%')

# Function to tag new sentences
def pos_tag_sentence(sentence):
    tokens = word_tokenize(sentence)
    tagged_sentence = trigram_tagger.tag(tokens)
    return tagged_sentence

# Test the function
test_sentence = "The quick brown fox jumps over the lazy dog."
tagged_sentence = pos_tag_sentence(test_sentence)
print(tagged_sentence)
