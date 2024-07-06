from stringmatch import Match
import pandas as pd

# Read and prepare the data
df = pd.read_excel("/Users/bryan/Work/MNT-CURN/Purdue Internship/mnt-curn-llm/Book1.xlsx")
grouped = df.groupby("URLS")["Experts"].apply(list).reset_index()

my_data = grouped['Experts'].tolist()
llm_data = [['Prof Williams'], ['Elizabeth Rayne'], ['Michael Cohen'], ['Julia Strong'], ['Harry Zekollari', 'Cari Corrigan', 'Veronica Tollenaar'], ['Eduardo Leite', 'Carlos Nobre'], ['Giacomo Falchetta'], ['Kelly Beall'], []]


# Remove NaNs from the lists
my_data = [[expert for expert in experts if pd.notna(expert)] for experts in my_data]
llm_data = [[expert for expert in experts if pd.notna(expert)] for experts in llm_data]

# Sample LLM data

# Initialize the Match object
match = Match()

# Initialize counts
tp = fp = fn = 0

# Iterate over both lists of lists
for llm_experts, my_experts in zip(llm_data, my_data):
    # Calculate true positives, false positives, and false negatives
    for llm_expert in llm_experts:
        if any(match.match(my_expert, llm_expert) for my_expert in my_experts):
            tp += 1
        else:
            fp += 1
    
    for my_expert in my_experts:
        if not any(match.match(my_expert, llm_expert) for llm_expert in llm_experts):
            fn += 1

# Function to calculate F-score
def fscore(tp, fp, fn):
    return (2 * tp) / ((2 * tp) + fp + fn)

# Calculate F-score
f1_score = fscore(tp, fp, fn)
print(f"True Positives: {tp}, False Positives: {fp}, False Negatives: {fn}")
print(f"F1 Score: {f1_score}")
print(llm_data)
print(my_data)