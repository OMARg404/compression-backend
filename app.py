from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for handling CORS errors
import heapq
from collections import Counter

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Run-Length Encoding (RLE)
def rle_encode(input_string):
    if not input_string:
        return ""
    encoded_string = ""
    count = 1
    prev_char = input_string[0]
    for char in input_string[1:]:
        if char == prev_char:
            count += 1
        else:
            encoded_string += prev_char + str(count)
            prev_char = char
            count = 1
    encoded_string += prev_char + str(count)
    return encoded_string

# Huffman Coding
def huffman_compress(text):
    frequency = Counter(text)
    heap = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_codes = sorted(heap[0][1:], key=lambda p: (len(p[-1]), p))
    huffman_dict = {char: code for char, code in huffman_codes}
    encoded_text = "".join(huffman_dict[char] for char in text)
    return encoded_text, huffman_dict

# LZW Coding
def lzw_compress(input_string):
    dictionary = {chr(i): i for i in range(128)}
    dict_size = 128
    current_string = ""
    compressed_data = []

    for char in input_string:
        combined_string = current_string + char
        if combined_string in dictionary:
            current_string = combined_string
        else:
            compressed_data.append(dictionary[current_string])
            dictionary[combined_string] = dict_size
            dict_size += 1
            current_string = char

    if current_string:
        compressed_data.append(dictionary[current_string])

    return compressed_data

# Compression API endpoint
@app.route('/compress', methods=['POST'])
def compress():
    try:
        algorithm = request.form.get('algorithm', '').lower()
        file = request.files.get('file')
        text = request.form.get('text', '')

        if file:
            text = file.read().decode('utf-8')  # Read the file content

        if not text:
            return jsonify({'error': 'Text or file content is required for compression'}), 400

        if algorithm == 'rle':
            encoded_text = rle_encode(text)
            return jsonify({'encoded_text': encoded_text})
        elif algorithm == 'huffman':
            encoded_text, huffman_dict = huffman_compress(text)
            return jsonify({'encoded_text': encoded_text, 'huffman_dict': huffman_dict})
        elif algorithm == 'lzw':
            compressed = lzw_compress(text)
            return jsonify({'compressed_data': compressed})
        else:
            return jsonify({'error': 'Invalid algorithm provided'}), 400
    except Exception as e:
        print(f"Error during compression: {e}")  # Log error for debugging
        return jsonify({'error': f'An error occurred during compression: {str(e)}'}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
