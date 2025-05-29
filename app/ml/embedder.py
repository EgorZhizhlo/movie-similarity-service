import torch
from transformers import AutoTokenizer, AutoModel


class Embedder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tokenizer = AutoTokenizer.from_pretrained(
                "distilbert-base-uncased")
            cls._instance.model = AutoModel.from_pretrained(
                "distilbert-base-uncased")
            cls._instance.model.eval()
        return cls._instance

    def encode(self, texts: list[str]) -> list[list[float]]:
        inputs = self.tokenizer(
            texts,
            truncation=True,
            padding="longest",
            return_tensors="pt",
            max_length=256,
        )
        with torch.no_grad():
            last_hidden = self.model(**inputs).last_hidden_state
        return last_hidden[:, 0, :].cpu().tolist()


embedder = Embedder()
