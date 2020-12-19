import csv
import torch
import os
import numpy as np

from transformers import RobertaTokenizer, RobertaForSequenceClassification
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler


MODEL_SAVE_DIRECTORY = "./save-model"
DATA_FOLDER = "../data"
PRED_PATH = "../predictions"

if not os.path.exists(MODEL_SAVE_DIRECTORY):
    raise Exception(f"Please save the model in {MODEL_SAVE_DIRECTORY}")

if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"There are {torch.cuda.device_count()} GPU(s) available")
    print(f"Using {torch.cuda.get_device_name(0)}")
else:
    device = torch.device("cpu")

tokenizer = RobertaTokenizer.from_pretrained(MODEL_SAVE_DIRECTORY)
model = RobertaForSequenceClassification.from_pretrained(MODEL_SAVE_DIRECTORY)

raw_test_data = []
with open(os.path.join(DATA_FOLDER, "test.tsv")) as f:
    reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
    next(reader, None)

    for row in reader:
        _row = [int(row[0]), row[1]]
        raw_test_data.append(_row)


sentences = [row[1] for row in raw_test_data]
input_ids = []
attention_masks = []

# For every sentence...
for sent in sentences:
    # `encode_plus` will:
    #   (1) Tokenize the sentence.
    #   (2) Prepend the `[CLS]` token to the start.
    #   (3) Append the `[SEP]` token to the end.
    #   (4) Map tokens to their IDs.
    #   (5) Pad or truncate the sentence to `max_length`
    #   (6) Create attention masks for [PAD] tokens.
    encoded_dict = tokenizer.encode_plus(
        sent,                      # Sentence to encode.
        add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
        max_length=128,           # Pad & truncate all sentences.
        pad_to_max_length=True,
        return_attention_mask=True,   # Construct attn. masks.
        return_tensors='pt',     # Return pytorch tensors.
    )

    # Add the encoded sentence to the list.
    input_ids.append(encoded_dict['input_ids'])

    # And its attention mask (simply differentiates padding from non-padding).
    attention_masks.append(encoded_dict['attention_mask'])

# Convert the lists into tensors.
input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)

# Set the batch size.
batch_size = 32

# Create the DataLoader.
prediction_data = TensorDataset(input_ids, attention_masks)
prediction_sampler = SequentialSampler(prediction_data)
prediction_dataloader = DataLoader(
    prediction_data, sampler=prediction_sampler, batch_size=batch_size)

print('Predicting labels for {:,} test sentences...'.format(len(input_ids)))

# Put model in evaluation mode
model.eval()

# Tracking variables
predictions = []

# Predict
for batch in prediction_dataloader:
    # Add batch to GPU
    batch = tuple(t.to(device) for t in batch)

    # Unpack the inputs from our dataloader
    b_input_ids, b_input_mask = batch

    # Telling the model not to compute or store gradients, saving memory and
    # speeding up prediction
    with torch.no_grad():
        # Forward pass, calculate logit predictions
        outputs = model(b_input_ids, token_type_ids=None,
                        attention_mask=b_input_mask)

    logits = outputs[0]

    # Move logits and labels to CPU
    logits = logits.detach().cpu().numpy()

    # Store predictions and true labels
    predictions.append(logits)

flat_predictions = np.concatenate(predictions, axis=0)
flat_predictions = np.argmax(flat_predictions, axis=1).flatten()

results = []
for i, tweet in enumerate(raw_test_data):
    t = {
        'id': raw_test_data[i][0],
        'label': flat_predictions[i]
    }
    results.append(t)

f = open(os.path.join(PRED_PATH, "T2.csv"), "w")

fieldnames = ["id", "hateful"]
writer = csv.writer(f, )
writer.writerow(fieldnames)

for tweet in results:
    row = [tweet['id'], tweet['label']]
    writer.writerow(row)
