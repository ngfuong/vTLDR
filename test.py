import torch.cuda
import yaml
import os
from utils import get_data_batch, tokenizer, rouge

from transformers import EncoderDecoderModel
import pickle


with open('./config.yaml') as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)

os.makedirs(configs['output_dir']+'/pretrained/', exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
test_data = get_data_batch(path=configs["test"], test=True)

model = EncoderDecoderModel.from_pretrained(configs['output_dir']+'/pretrained/')
model.to(device)


# map data correctly
def generate_summary(batch):
    # Tokenizer will automatically set [BOS] <text> [EOS]
    inputs = tokenizer(batch["original"], padding="max_length", truncation=True, max_length=256, return_tensors="pt")
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)

    outputs = model.generate(input_ids,
                             attention_mask=attention_mask,
                             max_length = configs['decoder_max_length'],
                             early_stopping= configs['early_stopping'],
                             num_beams= configs['num_beams'],
                             no_repeat_ngram_size= configs['no_repeat_ngram_size'])

    # all special tokens including will be removed
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    batch["pred"] = output_str
    return batch


results = test_data.map(
    generate_summary,
    batched=True,
    batch_size=configs["batch_size"],
    remove_columns=["original"]
)

rouge_output = rouge.compute(predictions=results["pred"],
                             references= results["summary"],
                             rouge_types=["rouge1", "rouge2", "rougeL"])

os.makedirs('./testing/', exist_ok=True)
with open('./testing/prediction.pkl', 'wb') as f:
    pickle.dump(results["pred"], f, protocol=pickle.HIGHEST_PROTOCOL)
with open('./testing/reference.pkl', 'wb') as f:
    pickle.dump(results["summary"], f, protocol=pickle.HIGHEST_PROTOCOL)
with open('./testing/rouge.txt', 'w+') as f:
    for key,value in rouge_output.items():
        f.write(key.upper())
        f.write(' : ')
        f.write(repr(value.mid))
        f.write('\n')
