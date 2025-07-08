# scripts/fine_tune_model.py

import os
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)

# --- Configuration ---

# Model selection from Hugging Face Hub.
# 'distilgpt2' is a smaller, faster version of GPT-2, ideal for prototyping.
MODEL_NAME = "distilgpt2"

# Paths to the datasets created in the previous step.
TRAIN_DATA_FILE = "data/train_dataset.json"
VALIDATION_DATA_FILE = "data/validation_dataset.json"

# Directory where the fine-tuned model will be saved.
OUTPUT_DIR = "models/recipe-generator-distilgpt2"

# --- Main Functions ---

def load_and_prepare_dataset(tokenizer):
    """
    Loads the datasets, formats them into a single text string per recipe,
    and tokenizes the text.
    """
    print("Loading and preparing dataset...")

    # Load the JSON files using the 'datasets' library.
    data_files = {'train': TRAIN_DATA_FILE, 'validation': VALIDATION_DATA_FILE}
    raw_datasets = load_dataset('json', data_files=data_files)

    def format_recipe(example):
        """
        Formats a single recipe example into the required string format:
        "TITLE: [Title] INGREDIENTS: [ingredient1], [ingredient2] INSTRUCTIONS: [instruction1] [instruction2]"
        """
        title = example.get('title', '')
        ingredients = ', '.join(example.get('ingredients', []))
        instructions = ' '.join(example.get('instructions', []))
        
        # We add the tokenizer's end-of-sentence token to signal the end of a recipe.
        return f"TITLE: {title} INGREDIENTS: {ingredients} INSTRUCTIONS: {instructions}{tokenizer.eos_token}"

    def tokenize_function(examples):
        """
        Tokenizes a batch of formatted recipe strings.
        """
        formatted_texts = [format_recipe(ex) for ex in examples]
        return tokenizer(formatted_texts, truncation=True, padding=False)

    # Apply the formatting and tokenization to the entire dataset.
    # The 'batched=True' argument processes multiple examples at once for efficiency.
    tokenized_datasets = raw_datasets.map(
        lambda examples: tokenize_function(examples),
        batched=True,
        remove_columns=raw_datasets["train"].column_names, # Remove old columns to keep the dataset clean
    )
    
    print("Dataset prepared and tokenized.")
    return tokenized_datasets['train'], tokenized_datasets['validation']


def main():
    """
    Main function to orchestrate the model fine-tuning process.
    """
    print(f"--- Starting Fine-Tuning Process for model: {MODEL_NAME} ---")

    # 1. Load Tokenizer
    # The tokenizer converts text into a sequence of numbers (tokens) that the model can understand.
    # We use a pre-trained tokenizer that matches our model.
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    # GPT-2 doesn't have a default padding token, so we set it to the end-of-sentence token.
    tokenizer.pad_token = tokenizer.eos_token

    # 2. Load and Prepare Datasets
    train_dataset, eval_dataset = load_and_prepare_dataset(tokenizer)

    # 3. Load Pre-trained Model
    # AutoModelForCausalLM loads a model suitable for text generation (a language model).
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    # 4. Define Training Arguments
    # TrainingArguments is a class that holds all the hyperparameters for the training process.
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,  # Number of times to iterate over the training dataset. 3 is a good starting point.
        per_device_train_batch_size=4,  # Number of examples per batch for training. Adjust based on your GPU memory.
        per_device_eval_batch_size=4,   # Number of examples per batch for evaluation.
        warmup_steps=500,               # Number of steps for the learning rate to warm up. Prevents instability at the start.
        weight_decay=0.01,              # Regularization technique to prevent overfitting.
        logging_dir='./logs',           # Directory for storing logs.
        logging_steps=10,
        evaluation_strategy="epoch",    # Run evaluation at the end of each epoch.
        save_strategy="epoch",          # Save a checkpoint at the end of each epoch.
        load_best_model_at_end=True,    # Load the best model found during training at the end.
    )

    # Data collator for language modeling. It will handle padding for us.
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # 5. Initialize Trainer
    # The Trainer class from Hugging Face abstracts away the complex training loop.
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )

    # 6. Start Fine-Tuning
    print("Starting model training...")
    trainer.train()
    print("Training finished.")

    # 7. Save the Final Model and Tokenizer
    print(f"Saving the fine-tuned model to {OUTPUT_DIR}")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Model saved successfully.")
    print(f"--- Fine-Tuning Process Complete ---")

if __name__ == "__main__":
    main()
