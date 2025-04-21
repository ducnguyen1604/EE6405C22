import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import load_dataset, concatenate_datasets
import evaluate
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class CustomSeq2SeqTrainer(Seq2SeqTrainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_lang = None
        
    def set_target_lang(self, target_lang):
        self.target_lang = target_lang
        
    def generate(self, *args, **kwargs):
        if self.target_lang is not None:
            kwargs['forced_bos_token_id'] = self.tokenizer.lang_code_to_id[lang_code_map[self.target_lang]]
        return super().generate(*args, **kwargs)

# Update the data path to a proper path
data_path = "../data/"

def load_and_preprocess(lang_pair):
    dataset = load_dataset("csv", data_files={
        "train": f"{data_path}{lang_pair}_train.csv",
        "val": f"{data_path}{lang_pair}_val.csv",
        "test": f"{data_path}{lang_pair}_test.csv"
    })
    # Add language information to the dataset
    src_lang, tgt_lang = lang_pair.split("_")
    for split in ["train", "val", "test"]:
        dataset[split] = dataset[split].add_column("source_lang", [src_lang] * len(dataset[split]))
        dataset[split] = dataset[split].add_column("target_lang", [tgt_lang] * len(dataset[split]))
    return dataset["train"], dataset["val"], dataset["test"]

# Load all language pairs
lang_pairs = ["en_es", "en_it", "en_cn"]
all_datasets = {lp: load_and_preprocess(lp) for lp in lang_pairs}

# Concatenate all training and validation datasets
train_datasets = []
val_datasets = []
for lang_pair in lang_pairs:
    train_datasets.append(all_datasets[lang_pair][0])
    val_datasets.append(all_datasets[lang_pair][1])

# Combine all datasets
combined_train = concatenate_datasets(train_datasets)
combined_val = concatenate_datasets(val_datasets)

# Load mBART50
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

# Freeze encoder + embeddings
'''
for param in model.model.encoder.parameters():
    param.requires_grad = False
model.model.shared.weight.requires_grad = False  # Embeddings

# Verify frozen params (only decoder should be trainable)
print("Trainable parameters:")
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name)
'''

lang_code_map = {
    "en": "en_XX",
    "es": "es_XX",
    "it": "it_IT", 
    "cn": "zh_CN"
}

def tokenize_fn(batch):
    # Extract language pair from the dataset
    src_lang = batch["source_lang"][0]
    tgt_lang = batch["target_lang"][0]
    
    tokenizer.src_lang = lang_code_map[src_lang]
    tokenizer.tgt_lang = lang_code_map[tgt_lang]

    # Tokenize source
    inputs = tokenizer(
        batch["source_text"],
        max_length=64,
        truncation=True,
        padding="max_length"
    )
    
    # Tokenize target with special handling for padding
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            batch["target_text"],
            max_length=64,
            truncation=True,
            padding="max_length"
        )
        # Replace padding token ID with -100 for loss computation
        labels["input_ids"] = [
            [token if token != tokenizer.pad_token_id else -100 for token in label]
            for label in labels["input_ids"]
        ]
    
    inputs = {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "labels": labels["input_ids"]
    }
    return inputs

bleu = evaluate.load("bleu")

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    return bleu.compute(
        predictions=decoded_preds,
        references=[[label] for label in decoded_labels]
    )

training_args = Seq2SeqTrainingArguments(
    output_dir="./mbart50-ecommerce",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=4,
    num_train_epochs=5,
    learning_rate=1e-5,
    weight_decay=0.01,
    gradient_accumulation_steps=2,
    fp16=True,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_steps=50,
    predict_with_generate=True,
    ignore_data_skip=True,
    # Generation parameters
    generation_max_length=64,
    generation_num_beams=4,
    warmup_ratio=0.1,
    lr_scheduler_type="cosine"
)

# Tokenize the combined datasets
tokenized_train = combined_train.map(
    tokenize_fn,
    batched=True
)
tokenized_val = combined_val.map(
    tokenize_fn,
    batched=True
)

# Initialize Trainer
trainer = CustomSeq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    compute_metrics=compute_metrics,
    tokenizer=tokenizer
)

print("\n=== Training Multilingual Model ===")
trainer.train()

# Save the final model
model.save_pretrained("./mbart50-ecommerce/final")
tokenizer.save_pretrained("./mbart50-ecommerce/final")

def translate(text, src_lang="en", tgt_lang="es"):
    # Use the correct path format matching your saved models
    lang_pair = f"{src_lang}_{tgt_lang}"
    model_path = f"./mbart50-ecommerce/{lang_pair}/pytorch_model.bin"
    
    # Check if file exists before loading
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model for {lang_pair} not found at {model_path}")
        
    # Load state dict with proper error handling
    try:
        state_dict = torch.load(model_path, map_location=model.device)
        model.load_state_dict(state_dict)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
        
    tokenizer.src_lang = lang_code_map[src_lang]
    
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id[lang_code_map[tgt_lang]]
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)