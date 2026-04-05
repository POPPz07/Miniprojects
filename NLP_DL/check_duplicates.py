import pandas as pd

# Check train set
train_df = pd.read_csv('data/train.csv')
print("=" * 60)
print("TRAIN SET ANALYSIS")
print("=" * 60)
print(f"Total samples: {len(train_df)}")
print(f"\nDuplicate breakdown:")
print(train_df['is_duplicate'].value_counts())
print(f"\nDuplicate ratio: {train_df['is_duplicate'].sum() / len(train_df) * 100:.1f}%")

# Check test set
test_df = pd.read_csv('data/test.csv')
print("\n" + "=" * 60)
print("TEST SET ANALYSIS")
print("=" * 60)
print(f"Total samples: {len(test_df)}")
print(f"\nDuplicate breakdown:")
print(test_df['is_duplicate'].value_counts())
print(f"\nDuplicate ratio: {test_df['is_duplicate'].sum() / len(test_df) * 100:.1f}%")
