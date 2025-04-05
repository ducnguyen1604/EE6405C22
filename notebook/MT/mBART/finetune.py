import torch
from transformers import MBartForConditionalGeneration, MBartTokenizer, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import load_dataset, concatenate_datasets
import evaluate
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# Update the data path to a proper path
data_path = REMOVED_SECRET../data/REMOVED_SECRET
def load_and_preprocess(lang_pair):
    dataset = load_dataset(REMOVED_SECRETcsvREMOVED_SECRET, data_files={
        REMOVED_SECRETtrainREMOVED_SECRET: fREMOVED_SECRET{data_path}{lang_pair}_train.csvREMOVED_SECRET,
        REMOVED_SECRETvalREMOVED_SECRET: fREMOVED_SECRET{data_path}{lang_pair}_val.csvREMOVED_SECRET,
        REMOVED_SECRETtestREMOVED_SECRET: fREMOVED_SECRET{data_path}{lang_pair}_test.csvREMOVED_SECRET
    })
    return dataset[REMOVED_SECRETtrainREMOVED_SECRET], dataset[REMOVED_SECRETvalREMOVED_SECRET], dataset[REMOVED_SECRETtestREMOVED_SECRET]


lang_pairs = [REMOVED_SECRETen_esREMOVED_SECRET, REMOVED_SECRETen_itREMOVED_SECRET, REMOVED_SECRETen_cnREMOVED_SECRET]
datasets = {lp: load_and_preprocess(lp) for lp in lang_pairs}

#load mBART25, smaller model but supports our use case
model = MBartForConditionalGeneration.from_pretrained(REMOVED_SECRETfacebook/mbart-large-cc25REMOVED_SECRET)
tokenizer = MBartTokenizer.from_pretrained(REMOVED_SECRETfacebook/mbart-large-cc25REMOVED_SECRET)

# Freeze encoder + embeddings
for param in model.model.encoder.parameters():
    param.requires_grad = False
model.model.shared.weight.requires_grad = False  # Embeddings

# Verify frozen params (only decoder should be trainable)
print(REMOVED_SECRETTrainable parameters:REMOVED_SECRET)
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name)

lang_code_map = {
    REMOVED_SECRETenREMOVED_SECRET: REMOVED_SECRETen_XXREMOVED_SECRET,
    REMOVED_SECRETesREMOVED_SECRET: REMOVED_SECRETes_XXREMOVED_SECRET,
    REMOVED_SECRETitREMOVED_SECRET: REMOVED_SECRETit_ITREMOVED_SECRET, 
    REMOVED_SECRETcnREMOVED_SECRET: REMOVED_SECRETzh_CNREMOVED_SECRET
}

def tokenize_fn(batch, src_lang, tgt_lang):
    tokenizer.src_lang = lang_code_map[src_lang]
    tokenizer.tgt_lang = lang_code_map[tgt_lang]
    
    # Remove <start> and <end> tags if present
    def clean_text(text):
        return text.replace(REMOVED_SECRET<start>REMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET).replace(REMOVED_SECRET<end>REMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET).strip()
    
    inputs = tokenizer(
        [clean_text(text) for text in batch[REMOVED_SECRETdataREMOVED_SECRET]],
        max_length=64,
        truncation=True,
        padding=REMOVED_SECRETmax_lengthREMOVED_SECRET
    )
    
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            [clean_text(text) for text in batch[REMOVED_SECRETtargetREMOVED_SECRET]],
            max_length=64,
            truncation=True,
            padding=REMOVED_SECRETmax_lengthREMOVED_SECRET
        )
    # Rename/restructure the inputs dictionary
    inputs = {
        REMOVED_SECRETinput_idsREMOVED_SECRET: inputs[REMOVED_SECRETinput_idsREMOVED_SECRET],
        REMOVED_SECRETattention_maskREMOVED_SECRET: inputs[REMOVED_SECRETattention_maskREMOVED_SECRET],
        REMOVED_SECRETlabelsREMOVED_SECRET: labels[REMOVED_SECRETinput_idsREMOVED_SECRET]
    }
    
    return inputs

bleu = evaluate.load(REMOVED_SECRETbleuREMOVED_SECRET)

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
    output_dir=REMOVED_SECRET./mbart25-ecommerceREMOVED_SECRET,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    learning_rate=3e-5,
    weight_decay=0.01,
    gradient_accumulation_steps=4,
    fp16=True,
    evaluation_strategy=REMOVED_SECRETepochREMOVED_SECRET,
    save_strategy=REMOVED_SECRETepochREMOVED_SECRET,
    logging_steps=50,
    predict_with_generate=True,
    ignore_data_skip=True,
)

for lang_pair in lang_pairs:
    src, tgt = lang_pair.split(REMOVED_SECRET_REMOVED_SECRET)
    
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
    
    print(fREMOVED_SECRET\n=== Training {lang_pair.upper()} ===REMOVED_SECRET)
    trainer.train()
    
    # Save checkpoint
    model.save_pretrained(fREMOVED_SECRET./mbart25-ecommerce/{lang_pair}REMOVED_SECRET)
    tokenizer.save_pretrained(fREMOVED_SECRET./mbart25-ecommerce/{lang_pair}REMOVED_SECRET)

def translate(text, src_lang=REMOVED_SECRETenREMOVED_SECRET, tgt_lang=REMOVED_SECRETesREMOVED_SECRET):
    # Use the correct path format matching your saved models
    lang_pair = fREMOVED_SECRET{src_lang}_{tgt_lang}REMOVED_SECRET
    model_path = fREMOVED_SECRET./mbart25-ecommerce/{lang_pair}/pytorch_model.binREMOVED_SECRET
    
    # Check if file exists before loading
    if not os.path.exists(model_path):
        raise FileNotFoundError(fREMOVED_SECRETModel for {lang_pair} not found at {model_path}REMOVED_SECRET)
        
    # Load state dict with proper error handling
    try:
        state_dict = torch.load(model_path, map_location=model.device)
        model.load_state_dict(state_dict)
    except Exception as e:
        print(fREMOVED_SECRETError loading model: {e}REMOVED_SECRET)
        return None
        
    tokenizer.src_lang = lang_code_map[src_lang]
    
    inputs = tokenizer(text, return_tensors=REMOVED_SECRETptREMOVED_SECRET).to(model.device)
    outputs = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id[lang_code_map[tgt_lang]]
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)