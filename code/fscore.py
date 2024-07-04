from stringmatch import Match

llm_data = ['Kathryn Fiorella', 'Horace Owiti Onyango', 'Fonda Jane Awuor', 'Christopher Aura', 'Prof Williams', 'Justin Rowlatt', 'Michael Cohen', 'Harry Zekollari', 'Cari Corrigan', 'Veronica Tollenaar', 'Eduardo Leite', 'Cosmos Nobre', 'Giacomo Falchetta', 'Kelly Beall', 'Kathryn Fiorella', 'Horace Owiti Onyango', 'Fonda Jane Awuor', 'Christopher Aura']
my_data = ['Prof Paul Williams', 'UN Climate Science Body', 'Researchers ', 'a study of 26 carbon offset projects across six countries', 'A 2022 report', 'Scientists', 'Cari Corrigan ', 'Veronica Tollenaar', 'Harry Zekollari', 'Eduardo Leite', 'Hugo Chavez', 'Carlos Nobre', 'scientists', 'Giacomo Falchetta', 'Colin Polsky, Ph.D.', 'Adam Stover', 'the authors', 'Kathryn Fiorella', 'Ranaivo Rasolofoson', 'Horace Owiti Onyango', 'Fonda Jane Awuor', 'Christopher Aura', 'Kenya Marine', 'Fisheries Research Institute.']

match = Match()

tp = fp = fn = 0

for llmExpert in llm_data:
    for expert in my_data:
        if match.match(expert,llmExpert) == True:
            tp += 1
        if llmExpert not in my_data:
            fp += 1
        if expert not in llm_data:
            fn += 1
print(tp,fp,fn)

def fscore(tp,fp,fn):
    f1 = (2 * tp) / ((2 * tp) + fp + fn)
    print(f1)

fscore(tp,fp,fn)
