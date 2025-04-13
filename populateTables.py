import sqlite3

class QuestionLoader:
    def __init__(self, db_name='quiz_bowl.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def load_questions(self, table_name, questions):
        self.cursor.executemany(f'''
            INSERT INTO {table_name} (question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', questions)
        self.connection.commit()
        print(f"Questions loaded into table '{table_name}'.")

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    loader = QuestionLoader()

    # DS 3850
    loader.load_questions('ds_3850', [
        ("What is the primary purpose of a relational database?", "Data visualization", "Storing large image files", "Organizing data into structured tables with relationships", "Encrypting communication between users", "C"),
        ("Which language is most commonly used for managing and querying relational databases?", "HTML", "Python", "SQL", "Java", "C"),
        ("What does CRUD stand for in database operations?", "Create, Read, Update, Delete", "Copy, Read, Upload, Download", "Connect, Retrieve, Use, Display", "Compile, Run, Use, Debug", "A"),
        ("Which library is used to interact with SQLite in Python?", "pandas", "sqlite3", "flask", "matplotlib", "B"),
        ("Which is NOT an advantage of Git?", "Easy collaboration", "Tracking changes", "Automatic debugging", "Reverting versions", "C"),
        ("What does an IDE like VS Code help you with?", "Hosting sites", "Writing/debugging code", "Creating presentations", "Compressing files", "B"),
        ("Which model organizes data in a tree-like structure?", "Relational", "Hierarchical", "Network", "Graph", "B"),
        ("What component handles interaction in a GUI?", "Database", "Compiler", "Event handler", "Server", "C"),
        ("What does the .py extension mean?", "Photoshop file", "Python script", "PowerPoint", "PDF", "B"),
        ("Which SQL command retrieves data?", "INSERT", "DELETE", "UPDATE", "SELECT", "D")
    ])

    # ECON 3610
    loader.load_questions('econ_3610', [
        ("What is the mean of the data set: 5, 10, 15, 20, 25?", "15", "20", "10", "25", "A"),
        ("What does the standard deviation measure?", "Center of data", "Shape of graph", "Spread of data", "Number of outliers", "C"),
        ("Probability of heads twice in two coin flips?", "1/4", "1/3", "1/2", "2/3", "A"),
        ("Which distribution models success/failure events?", "Poisson", "Binomial", "Normal", "Exponential", "B"),
        ("What is the range of a data set?", "Difference between high and low", "Number of values", "Square root of mean", "Sum of values", "A"),
        ("A p-value < 0.05 usually means?", "Accept null", "Insufficient data", "Reject null", "Inconclusive", "C"),
        ("Area under normal curve represents?", "Standard deviation", "Mean", "Probability", "Sample size", "C"),
        ("Which is not a central tendency?", "Mean", "Median", "Mode", "Range", "D"),
        ("Best graph for frequency distributions?", "Line chart", "Histogram", "Pie chart", "Scatterplot", "B"),
        ("Central Limit Theorem says?", "Always uniform", "Approaches normal", "Cannot be predicted", "Always skewed", "B")
    ])

    # MKT 4100
    loader.load_questions('mkt_4100', [
        ("Primary challenge of international marketing?", "Shipping costs", "Local hiring", "Cultural differences", "Weather", "C"),
        ("Trade agreement with U.S., Mexico, Canada?", "NAFTA", "ASEAN", "WTO", "EU", "A"),
        ("What is ethnocentrism?", "Belief in equality", "Love of foreign brands", "Cultural superiority", "Localization", "C"),
        ("What is glocalization?", "Translating ads", "Ignoring culture", "Adapting global to local", "Only local brands", "C"),
        ("What is differential pricing?", "Same price everywhere", "Dynamic updates", "Skimming", "Price by region", "D"),
        ("PEST analysis evaluates?", "Legal risks", "Market size", "Political/Econ/Social/Tech factors", "Pricing", "C"),
        ("Not part of Hofstede’s cultural dimensions?", "Power distance", "Individualism", "Marketing budget", "Uncertainty avoidance", "C"),
        ("What is localization?", "Same content globally", "Custom content for markets", "Outsourcing", "Copying brands", "B"),
        ("Global brand aims for?", "Unique names", "Central identity", "Irregular pricing", "Local ownership", "B"),
        ("What are tariffs?", "Shipping costs", "Import taxes", "Copyright penalties", "Discounts", "B")
    ])

    # MKT 4900
    loader.load_questions('mkt_4900', [
        ("What does SEO stand for?", "Search Engine Optimization", "Sales Engagement", "Smart Output", "Social Optimization", "A"),
        ("Main purpose of Google Analytics?", "Social posts", "Traffic analysis", "Email lists", "Ad design", "B"),
        ("What does CTR stand for?", "ROI", "Bounce Rate", "Click-Through Rate", "CPM", "C"),
        ("Best platform for B2B?", "Instagram", "LinkedIn", "Snapchat", "Pinterest", "B"),
        ("What is organic traffic?", "From ads", "From influencers", "From search engines", "Direct type-in", "C"),
        ("Not in marketing funnel?", "Awareness", "Consideration", "Payment Plan", "Conversion", "C"),
        ("What is A/B testing?", "Targeting two audiences", "Testing versions", "Competitor analysis", "Compliance", "B"),
        ("Best email practice?", "ALL CAPS", "Buy lists", "Use names", "Send nonstop", "C"),
        ("PPC means?", "Product Campaign", "Pay-Per-Click", "Conversion Cost", "Promotion Cost", "B"),
        ("Retargeting shows ads to?", "New visitors", "Never-seen users", "Past visitors", "Completed buyers", "C")
    ])

    # DS 3841
    loader.load_questions('ds_3841', [
        ("What does {} represent in Python?", "List", "Tuple", "Dictionary", "Set", "C"),
        ("How do you define a function?", "define", "def", "function", "init", "B"),
        ("What is output of print(2 ** 3)?", "5", "6", "8", "9", "C"),
        ("How do you write a comment?", "//", "<!-- -->", "#", "/* */", "C"),
        ("Which is immutable?", "List", "Dict", "Set", "Tuple", "D"),
        ("What does len() return?", "Last element", "Item count", "Lowercase string", "Starts loop", "B"),
        ("Output of bool(0)?", "0", "True", "False", "None", "C"),
        ("Which runs 5 times?", "range(5)", "while < 5", "range(1,6)", "All of the above", "D"),
        ("Which keyword handles exceptions?", "if", "catch", "except", "error", "C"),
        ("What does input() do?", "Display message", "Take input", "Exit program", "Define variable", "B")
    ])

    loader.close()
