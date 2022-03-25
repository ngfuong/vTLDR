import torch
from vncorenlp import VnCoreNLP
from transformers import AutoTokenizer, EncoderDecoderModel


def predict(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = EncoderDecoderModel.from_pretrained('./training/checkpoint-10000')
    model.to(device)

    rdrsegmenter = VnCoreNLP('./vncorenlp/VnCoreNLP-1.1.1.jar', annotators="wseg", max_heap_size="-Xmx500m")
    text = rdrsegmenter.tokenize(text)
    text = ' '.join([' '.join(x) for x in text])

    tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base', use_fast=False)
    inputs = tokenizer(text, padding="max_length", truncation=True, max_length=256, return_tensors="pt")
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)

    outputs = model.generate(input_ids,
                             attention_mask=attention_mask,
                             max_length=256,
                             early_stopping=True,
                             num_beams=4,
                             no_repeat_ngram_size=3)
    # all special tokens including will be removed
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    return output_str[0]
