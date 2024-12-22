import heapq
from collections import Counter

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

def rle_decode(encoded_string):
    decoded_string = ""
    i = 0
    while i < len(encoded_string):
        char = encoded_string[i]
        i += 1
        count = ""
        while i < len(encoded_string) and encoded_string[i].isdigit():
            count += encoded_string[i]
            i += 1
        decoded_string += char * int(count)
    return decoded_string

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

def huffman_decompress(encoded_text, huffman_dict):
    reverse_dict = {code: char for char, code in huffman_dict.items()}
    decoded_text = ""
    temp_code = ""
    for bit in encoded_text:
        temp_code += bit
        if temp_code in reverse_dict:
            decoded_text += reverse_dict[temp_code]
            temp_code = ""
    return decoded_text

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

def lzw_decompress(compressed_data):
    dictionary = {i: chr(i) for i in range(128)}
    dict_size = 128
    current_code = compressed_data.pop(0)
    pre_string = dictionary[current_code]
    decompressed_data = [pre_string]

    for code in compressed_data:
        if code in dictionary:
            current = dictionary[code]
        elif code == dict_size:
            current = pre_string + pre_string[0]
        else:
            raise ValueError("Invalid compressed data.")

        decompressed_data.append(current)
        dictionary[dict_size] = pre_string + current[0]
        dict_size += 1
        pre_string = current

    return "".join(decompressed_data)

# Main
def main():
    input_file = input("Enter the input text file path: ").strip('"')
    with open(input_file, 'r') as file:
        text = file.read()

    print("Choose the compression algorithm:")
    print("1. Run-Length Encoding (RLE)")
    print("2. Huffman Coding")
    print("3. LZW Coding")
    choice = int(input("Enter your choice (1/2/3): "))

    if choice == 1:
        encoded_text = rle_encode(text)
        print(f"Encoded Text: {encoded_text}")
        decoded_text = rle_decode(encoded_text)
        print(f"Decoded Text: {decoded_text}")
    elif choice == 2:
        encoded_text, huffman_dict = huffman_compress(text)
        print(f"Encoded Text: {encoded_text}")
        print(f"Huffman Codes: {huffman_dict}")
        decoded_text = huffman_decompress(encoded_text, huffman_dict)
        print(f"Decoded Text: {decoded_text}")
    elif choice == 3:
        compressed = lzw_compress(text)
        print(f"Compressed Data: {compressed}")
        decompressed = lzw_decompress(compressed)
        print(f"Decompressed Text: {decompressed}")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
