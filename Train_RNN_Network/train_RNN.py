from __future__ import unicode_literals, print_function, division
from io import open
import glob
import os
import unicodedata
import string
import torch
import time
import math
import random
import matplotlib.pyplot as plt

data_path = "data/names/*txt"


def findFiles(data_path):
    return glob.glob(data_path)


all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)
# Build the category_lines dictionary, a list of names per language
category_lines = {}
all_categories = []


# Turn a Unicode string to plain ASCII, thanks to https://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )


# Read a file and split into lines
def readLines(filename):
    lines = open(filename, encoding='utf-8').read().strip().split('\n')
    return [unicodeToAscii(line) for line in lines]


for filename in findFiles(data_path):
    category = os.path.splitext(os.path.basename(filename))[0]
    all_categories.append(category)
    lines = readLines(filename)
    random.shuffle(lines)
    n_lines = len(lines)
    train_size = int(0.7 * n_lines)
    val_size = int(0.2 * n_lines)
    test_size = n_lines - train_size - val_size
    category_lines[category] = {
        'train': lines[:train_size],
        'val': lines[train_size:train_size+val_size],
        'test': lines[train_size+val_size:]
    }

n_categories = len(all_categories)

# Find letter index from all_letters, e.g. "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)


# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor


def randomTrainingExample(split='train'):
    category = random.choice(all_categories)
    line = random.choice(category_lines[category][split])
    category_tensor = torch.tensor([all_categories])

n_categories = len(all_categories)

# Find letter index from all_letters, e.g. "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)


# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor


def randomTrainingExample(split='train'):
    category = random.choice(all_categories)
    line = random.choice(category_lines[category][split])
    category_tensor = torch.tensor([all_categories.index(category)], dtype=torch.long)
    line_tensor = lineToTensor(line)
    return category, line, category_tensor, line_tensor


def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


class RNN(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size

        self.i2h = torch.nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = torch.nn.Linear(input_size + hidden_size, output_size)
        self.softmax = torch.nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)


def train(category_tensor, line_tensor, model):
    hidden = model.init_hidden()
    model.zero_grad()

    for i in range(line_tensor.size()[0]):
        output, hidden = model(line_tensor[i], hidden)
    loss = criterion(output, category_tensor)
    loss.backward()
    for p in model.parameters():
        p.data.add_(p.grad.data, alpha=-learning_rate)
    return output, loss.item()
    
    
    
    

print("Started")

n_hidden = 128
rnn = RNN(n_letters, n_hidden, n_categories)
best_model_path = "MODELS/model_5.pth"
if os.path.isfile(best_model_path):
    # load the saved state dictionary
    state_dict = torch.load(best_model_path)
    # assign the state dictionary to the model
    model.load_state_dict(state_dict)


n_iters = 100000
print_every = 5000
plot_every = 5000

criterion = torch.nn.NLLLoss()
learning_rate = 0.008
current_loss = 0
all_losses = []

train_data = []
val_data = []
test_data = []

start = time.time()

# Initialize the best validation loss
best_val_loss = float('inf')

for i in range(1,11):
    print(f"TRAINING LOOP {i} / 10")
    for iter in range(1, n_iters + 1):
        category, line, category_tensor, line_tensor = randomTrainingExample(split='train')
        output, loss = train(category_tensor, line_tensor, rnn)
        current_loss += loss

        if iter % print_every == 0:
            print(
                f'iterations{iter} {round(iter / n_iters * 100,0)} time:{timeSince(start)} loss: {loss} line:{line} most likely class:{output.topk(1)[1][0].item()}  correct label:{category_tensor[0]}')

        if iter % plot_every == 0:
            all_losses.append(current_loss / plot_every)
            current_loss = 0

        # Validate the model every 1000th iteration
        if iter % 1000 == 0:
            val_loss = 0
            val_correct = 0
            val_total = 0
            with torch.no_grad():
                for category in all_categories:
                    for line in category_lines[category]['val']:
                        category_tensor = torch.tensor([all_categories.index(category)], dtype=torch.long)
                        line_tensor = lineToTensor(line)
                        hidden = rnn.init_hidden()
                        for i in range(line_tensor.size()[0]):
                            output, hidden = rnn(line_tensor[i], hidden)
                        val_loss += criterion(output, category_tensor)
                        if output.topk(1)[1][0].item() == category_tensor[0]:
                            val_correct += 1
                        val_total += 1
            val_loss /= val_total
            val_accuracy = val_correct / val_total
            print(f'Validation loss: {val_loss:.4f}, Validation accuracy: {val_accuracy:.4f}')
            if val_loss < best_val_loss:
                torch.save(rnn.state_dict(), "MODELS/model_5.pth")
                best_val_loss = val_loss
    
    plt.figure()
    plt.plot(all_losses)


