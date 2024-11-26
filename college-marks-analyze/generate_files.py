import pandas as pd
import numpy as np
import random

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# List of subjects (you can manually add or modify this list)
subjects = ["ECL", "DSM", "BEE", "CAO"]

# List of branches
branches = ["COMPS", "CSE-AIML", "CSE-DS", "EXTC"]

# Number of students
num_students = 414

# Function to generate marks
def generate_marks(mean, std_dev, min_mark=0, max_mark=100):
    mark = int(np.random.normal(mean, std_dev))
    return max(min_mark, min(mark, max_mark))

# Function to create dataset for a single subject
def create_subject_dataset(subject_name):
    data = []
    for _ in range(num_students):
        branch = random.choice(branches)

        # Generate marks
        ise1 = generate_marks(7, 1.5, 0, 10)
        ise2 = generate_marks(7, 1.5, 0, 10)
        mse = generate_marks(20, 5, 0, 30)
        ese = generate_marks(60, 15, 0, 100)

        data.append([branch, ise1, ise2, mse, ese])

    df = pd.DataFrame(data, columns=['Branch', 'ISE 1 Marks', 'ISE 2 Marks', 'MSE Marks', 'ESE Marks'])

    # Add some correlation between exams
    df['ISE 2 Marks'] = df['ISE 2 Marks'].clip(lower=df['ISE 1 Marks'] - 2, upper=df['ISE 1 Marks'] + 2)
    df['MSE Marks'] = ((df['MSE Marks'] + df['ISE 1 Marks'] * 3 + df['ISE 2 Marks'] * 3) / 3).round().astype(int)
    df['ESE Marks'] = ((df['ESE Marks'] + df['MSE Marks'] * 10/3) / 2).round().astype(int)

    # Ensure marks are within the correct range
    df['ISE 1 Marks'] = df['ISE 1 Marks'].clip(0, 10)
    df['ISE 2 Marks'] = df['ISE 2 Marks'].clip(0, 10)
    df['MSE Marks'] = df['MSE Marks'].clip(0, 30)
    df['ESE Marks'] = df['ESE Marks'].clip(0, 100)

    return df

# Generate and save datasets for each subject
for subject in subjects:
    df = create_subject_dataset(subject)
    df.to_csv(f'{subject.replace(" ", "_")}.csv', index=False)
    print(f"Dataset for {subject} has been created and saved.")

print("All datasets have been generated and saved.")