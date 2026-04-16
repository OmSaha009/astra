def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    with open("data/chunks.txt", "w") as chunk_file:
        chunk_file.write(str(chunks))

    return chunks