class Article:
    def __init__(self, text, source, date_published):
        self.text = text
        self.source = source
        self.date_published = date_published
        self.expert_references = []

    def add_expert_reference(self, expert):
        self.expert_references.append(expert)

    def write_file(self, filename):
        with open(filename, 'w') as f:
            f.write("Text:\n" + self.text + "\n")
            f.write("Source: " + self.source + "\n")
            f.write("Date Published: " + self.date_published + "\n")
            f.write("Expert References:\n")
            for ref in self.expert_references:
                f.write(f"Name: {ref['name']}, Affiliation: {ref['Affiliation']}\n")

# Create an instance of Article
test_article = Article(
    text="INTRODUCTION\n... (content truncated)",
    source="/mnt-curn-llm/meeting-notes/Papers.md",
    date_published="Publication date"
)

# Add expert references

test_article.add_expert_reference({"name":
"Y.W.K., D.B.A., and Y.-G.P.", 
"Affiliation": "Roles: Carried out the experiment, analyzed the data, and wrote the manuscript."})

test_article.add_expert_reference({"name":
"C.S.K. and Y.-M.H.", 
"Affiliation": "Roles: Involved in all animal experiments and the related analysis."})

test_article.add_expert_reference({"name":
"E.K., D.H.L., S.-W.K., K.-H.L., and W.-Y.K.",
"Affiliation": 
"Roles: Involved in device fabrications."})

test_article.add_expert_reference({"name":
"J.-U.P., S.-Y.L., J.W.C., and H.H.J.",
"Affiliation": 
"Roles: Oversaw all of the research phases and revised the manuscript."})



# Write to a file

test_article.write_file("test_article.txt")