import sys
import io
import json
import logging

# Set the console to use UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, request, jsonify
from flask_cors import CORS
from sudachipy import tokenizer
from sudachipy import dictionary

# Setup logging to show in the terminal
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# Try different dictionary loading methods
try:
    # Method 1: Default dictionary creation
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.A
    logger.info("Successfully created dictionary using default method")
except Exception as e:
    logger.error(f"Error creating dictionary: {e}")
    tokenizer_obj = None

@app.route("/tokenize", methods=["POST"])
def tokenize_text():
    # Ensure request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    # Log raw body to check incoming encoding
    raw_data = request.get_data(as_text=True)
    logger.debug("Raw data received: %s", raw_data)

    # Get text with error handling
    data = request.get_json()
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Comprehensive debugging
    logger.debug("Received text: %s", repr(text))
    logger.debug("Text length: %d", len(text))
    logger.debug("Text bytes: %s", text.encode('utf-8'))

    try:
        # Try multiple tokenization modes
        modes = [
            tokenizer.Tokenizer.SplitMode.A,
            tokenizer.Tokenizer.SplitMode.B,
            tokenizer.Tokenizer.SplitMode.C
        ]
        
        all_token_results = {}
        
        for split_mode in modes:
            try:
                tokens = tokenizer_obj.tokenize(text, split_mode)
                
                # Detailed token information
                token_info = [
                    {
                        "surface": token.surface(),
                        "base_form": token.dictionary_form(),
                        "part_of_speech": token.part_of_speech(),
                        "reading": token.reading_form() if hasattr(token, 'reading_form') else 'N/A',
                        "details": {
                            "dictionary_id": token.dictionary_id(),
                            "length": len(token.surface())
                        }
                    }
                    for token in tokens
                ]
                
                all_token_results[str(split_mode)] = token_info
                
                # Print tokens to console for debugging
                logger.debug(f"\nTokens for mode {split_mode}:")
                for token in tokens:
                    logger.debug(f"Surface: {token.surface()}")
                    logger.debug(f"Dictionary Form: {token.dictionary_form()}")
                    logger.debug(f"Part of Speech: {token.part_of_speech()}")
                    logger.debug("---")
            
            except Exception as mode_error:
                logger.error(f"Error in mode {split_mode}: {mode_error}")
                all_token_results[str(split_mode)] = []
        
        return jsonify(all_token_results)
    
    except Exception as e:
        logger.error(f"Tokenization Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e), 
            "type": type(e).__name__,
            "text": repr(text)
        }), 500

if __name__ == "__main__":
    # Additional system information
    logger.info("System Encoding: %s", sys.getdefaultencoding())
    logger.info("Filesystem Encoding: %s", sys.getfilesystemencoding())
    
    app.run(debug=True, host='0.0.0.0')
