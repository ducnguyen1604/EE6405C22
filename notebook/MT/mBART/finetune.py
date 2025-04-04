import torch
from transformers import MBartForConditionalGeneration, MBartTokenizer, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import load_dataset, concatenate_datasets
import evaluate
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# Update the data path to a proper path
data_path = "../data/"
def load_and_preprocess(lang_pair):
    dataset = load_dataset("csv", data_files={
        "train": f"{data_path}{lang_pair}_train.csv",
        "val": f"{data_path}{lang_pair}_val.csv",
        "test": f"{data_path}{lang_pair}_test.csv"
    })
    return dataset["train"], dataset["val"], dataset["test"]


lang_pairs = ["en_es", "en_it", "en_cn"]
datasets = {lp: load_and_preprocess(lp) for lp in lang_pairs}

#load mBART25, smaller model but supports our use case
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-cc25")
tokenizer = MBartTokenizer.from_pretrained("facebook/mbart-large-cc25")

# Freeze encoder + embeddings
for param in model.model.encoder.parameters():
    param.requires_grad = False
model.model.shared.weight.requires_grad = False  # Embeddings

# Verify frozen params (only decoder should be trainable)
print("Trainable parameters:")
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name)

lang_code_map = {
    "en": "en_XX",
    "es": "es_XX",
    "it": "it_IT", 
    "cn": "zh_CN"
}

def tokenize_fn(batch, src_lang, tgt_lang):
    tokenizer.src_lang = lang_code_map[src_lang]
    tokenizer.tgt_lang = lang_code_map[tgt_lang]
    
    # Remove <start> and <end> tags if present
    def clean_text(text):
        return text.replace("<start>", "").replace("<end>", "").strip()
    
    inputs = tokenizer(
        [clean_text(text) for text in batch["data"]],
        max_length=64,
        truncation=True,
        padding="max_length"
    )
    
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            [clean_text(text) for text in batch["target"]],
            max_length=64,
            truncation=True,
            padding="max_length"
        )
    # Rename/restructure the inputs dictionary
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
    output_dir="./mbart25-ecommerce",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    learning_rate=3e-5,
    weight_decay=0.01,
    gradient_accumulation_steps=4,
    fp16=True,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_steps=50,
    predict_with_generate=True,
    ignore_data_skip=True,
)

for lang_pair in lang_pairs:
    src, tgt = lang_pair.split("_")
    
    # Tokenize
    tokenized_train = datasets[lang_pair][0].map(
        lambda x: tokenize_fn(x, src, tgt),
        batched=True
    )
    tokenized_val = datasets[lang_pair][1].map(
        lambda x: tokenize_fn(x, src, tgt),
        batched=True
    )

    # Initialize Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        compute_metrics=compute_metrics,
        tokenizer=tokenizer
    )
    
    print(f"\n=== Training {lang_pair.upper()} ===")
    trainer.train()
    
    # Save checkpoint
    model.save_pretrained(f"./mbart25-ecommerce/{lang_pair}")
    tokenizer.save_pretrained(f"./mbart25-ecommerce/{lang_pair}")

def translate(text, src_lang="en", tgt_lang="es"):
    # Use the correct path format matching your saved models
    lang_pair = f"{src_lang}_{tgt_lang}"
    model_path = f"./mbart25-ecommerce/{lang_pair}/pytorch_model.bin"
    
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