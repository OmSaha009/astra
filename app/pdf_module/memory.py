chunks_store = []

def store_chunks(chunks):
    global chunks_store
    chunks_store = chunks

def get_chunks():
    return chunks_store