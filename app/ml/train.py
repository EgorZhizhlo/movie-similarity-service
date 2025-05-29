from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)


def fine_tune():
    dataset = load_dataset('imdb', split='train[:2000]')
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    model = AutoModelForSequenceClassification.from_pretrained(
        'distilbert-base-uncased', num_labels=2
    )

    def preprocess(batch):
        tokens = tokenizer(
            batch['text'], truncation=True,
            padding='max_length', max_length=256
        )
        tokens['labels'] = batch['label']
        return tokens

    ds = dataset.map(preprocess, batched=True)
    args = TrainingArguments(
        output_dir='models/distilbert-imdb',
        num_train_epochs=2,
        per_device_train_batch_size=8,
        logging_steps=100,
        save_steps=500
    )
    trainer = Trainer(model=model, args=args, train_dataset=ds)
    trainer.train()
    trainer.save_model()
