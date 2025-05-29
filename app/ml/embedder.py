import torch
from transformers import AutoTokenizer, AutoModel


class Embedder:
    def __init__(self, model_dir: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModel.from_pretrained(model_dir)

    def encode(self, texts: list[str]) -> list[list[float]]:
        inputs = self.tokenizer(
            texts, padding=True, truncation=True, return_tensors='pt'
        )
        with torch.no_grad():
            last_hidden = self.model(**inputs).last_hidden_state
            embeddings = last_hidden[:, 0, :].cpu().tolist()
        return embeddings
