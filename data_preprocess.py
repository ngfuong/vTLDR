import yaml

from transformers import AutoTokenizer
from vncorenlp import VnCoreNLP
from datasets import Dataset
from utils import listPaths, get_dataframe, process_data_to_model_inputs


with open("config.yaml", "r") as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)

tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base', use_fast=False)
rdrsegmenter = VnCoreNLP("./vncorenlp/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx2g')

train_paths = listPaths(configs["train"])
val_paths = listPaths(configs["val"])
test_paths = listPaths(configs["test"])

train_df = get_dataframe(train_paths).sample(frac=configs["sample_frac"])
val_df = get_dataframe(val_paths).sample(frac=configs["sample_frac"])
test_df = get_dataframe(test_paths).sample(frac=configs["sample_frac"])

train_data = Dataset.from_pandas(train_df)
val_data = Dataset.from_pandas(val_df)
test_data = Dataset.from_pandas(test_df)


def get_train_val_batch():
    train_data_batch = train_data.map(
        process_data_to_model_inputs,
        batched=True,
        batch_size=configs["batch_size"],
        remove_columns=["file", "original", "summary"],
    )

    train_data_batch.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
    )

    val_data_batch = val_data.map(
        process_data_to_model_inputs,
        batched=True,
        batch_size=configs["batch_size"],
        remove_columns=["file", "original", "summary"],
    )

    return train_data_batch, val_data_batch
