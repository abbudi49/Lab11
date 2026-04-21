import importlib
try:
    chromadb = importlib.import_module('chromadb')
    print('chromadb', chromadb.__version__)
    from chromadb import Client
    import inspect
    print('Client sig:', inspect.signature(Client))
    # Try instantiation variants
    variants = [dict(), {'persist_directory':'./chroma_db'}, {'path':'./chroma_db'}, {'settings':None}]
    for v in variants:
        try:
            print('trying', v)
            c = Client(**v)
            print('OK with', v)
            del c
            break
        except Exception as e:
            print('failed', v, type(e).__name__, e)
except Exception as e:
    print('import error', type(e).__name__, e)
