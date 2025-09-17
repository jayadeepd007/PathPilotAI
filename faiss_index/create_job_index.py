import faiss
import numpy as np

# Example: 10 job/document embeddings, each with 128 dimensions
embeddings = np.random.rand(10, 128).astype('float32')  # Replace with your actual embeddings

# Create FAISS index (L2 distance)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save index to disk
faiss.write_index(index, "d:/FILES/PathPIlotAI/faiss_index/job_index.faiss")

print("FAISS index saved to job_index.faiss")