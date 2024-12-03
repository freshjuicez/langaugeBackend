from sudachipy import tokenizer
from sudachipy import dictionary
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# Create dictionary
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.A

# Test text
text = "お寿司が食べたい。"

# Tokenize
tokens = tokenizer_obj.tokenize(text, mode)

# Print tokens
for token in tokens:
    print(f"Surface: {token.surface()}")
    print(f"Dictionary Form: {token.dictionary_form()}")
    print(f"Part of Speech: {token.part_of_speech()}")
    print("---")