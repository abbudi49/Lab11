import os

def many_time_pad_simulation():
#Plain text messages to encrypt
    messages = [
        "The secret meeting is at dawn.",
        "The target is moving tonight.",
        "Attack from the northern flank",
        "Retreat to the safehouse now.",
        "Hello Alice, this is Bob here",
        "Hello Carol, this is Eve here",
        "Password for the vault is abc",
        "Launch the payload on my mark",
        "Cancel the operation entirely",
        "Send backup to the rendezvous"
    ]
    
    #Longest Message determines the key length
    max_length = max(len(msg) for msg in messages)
    
    #Random Key Generation (same length for all)
    key = os.urandom(max_length)
    
    output_filename = "many_time_pad_output.txt"
    
    # Encryption
    with open(output_filename, "w") as f:
        f.write("=== MANY-TIME PAD SIMULATION ===\n\n")
        f.write(f"Shared Key (hex): {key.hex()}\n\n")
        f.write("-----------------------------------\n\n")
        
        for i, msg in enumerate(messages, 1):
         
            p_bytes = msg.encode('utf-8')
            
            
            c_bytes = bytes([p ^ k for p, k in zip(p_bytes, key)])
            
            f.write(f"Message {i}:\n")
            f.write(f"Plaintext (text): {msg}\n")
            f.write(f"Plaintext (hex) : {p_bytes.hex()}\n")
            f.write(f"Ciphertext (hex): {c_bytes.hex()}\n\n")

    print(f"Success! Open '{output_filename}' to view the results.")

if __name__ == "__main__":
    many_time_pad_simulation()


