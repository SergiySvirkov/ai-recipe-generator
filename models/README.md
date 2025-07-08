Models

<!-- This directory is intended to store the trained machine learning models. -->

This directory contains the fine-tuned AI models that power the recipe generation.
Directory Structure

Each model will be saved in its own subdirectory, named after the model version. For example:

    recipe-generator-distilgpt2/: This directory holds the fine-tuned distilgpt2 model. It contains files like pytorch_model.bin (the model weights), config.json (model configuration), and files related to the tokenizer.

Important Note

This directory is included in .gitignore.

Trained models are typically large binary files and should NOT be committed to a Git repository. Instead, they should be stored in a dedicated cloud storage service, such as:

    Amazon S3

    Google Cloud Storage

    Hugging Face Model Hub (recommended for transformers models)

For local development, the scripts/fine_tune_model.py script will generate the model files in this directory. For production deployment, you will need to download the model from your chosen cloud storage.
