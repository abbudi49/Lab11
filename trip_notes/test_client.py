from chromadb import Client
try:
    c = Client()
    print('Client() OK')
except Exception as e:
    print('Client() failed', type(e).__name__, e)

try:
    c2 = Client(persist_directory='chroma_db')
    print("Client(persist_directory=...) OK")
except Exception as e:
    print('Client(persist_directory) failed', type(e).__name__, e)

try:
    c3 = Client(path='chroma_db')
    print("Client(path=...) OK")
except Exception as e:
    print('Client(path) failed', type(e).__name__, e)
