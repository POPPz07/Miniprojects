# 🔵 Deep Learning Pipeline (LSTM)

## Step 1: Tokenization

- Convert text → integer sequences
- Build vocabulary

## Step 2: Padding

- Pad sequences to length = 100

## Step 3: Model Architecture

Embedding Layer:
- input_dim = vocab_size
- output_dim = 128

LSTM Layer:
- units = 64

Dense Layer:
- 32 units (ReLU)

Output Layer:
- Softmax (4 classes)

## Step 4: Compilation

- Loss: categorical_crossentropy
- Optimizer: Adam
- Metrics: accuracy

## Step 5: Training

- Epochs: 5–10
- Batch size: 32

## Step 6: Outputs

- Prediction (category)
- Probability
- Accuracy
- Loss curve

## Step 7: Optional Duplicate Logic

- Compare embeddings OR
- Use similarity threshold

## Important

Show:
- Model summary
- Training graph
- Sample predictions