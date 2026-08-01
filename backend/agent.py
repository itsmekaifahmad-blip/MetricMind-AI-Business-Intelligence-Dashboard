import pandas as pd
from semantic.metrics import metrics

# Load the dataset
df = pd.read_csv("data/sales.csv", encoding="latin1")


def ask_agent(question):
    question = question.lower()

    if "revenue" in question:
        revenue = df[metrics["Revenue"]["column"]].sum()
        return f"Total Revenue: ${revenue:,.2f}"

    elif "profit" in question:
        profit = df[metrics["Profit"]["column"]].sum()
        return f"Total Profit: ${profit:,.2f}"

    elif "orders" in question:
        orders = df[metrics["Orders"]["column"]].count()
        return f"Total Orders: {orders}"

    elif "average sales" in question:
        avg = df[metrics["Average Sales"]["column"]].mean()
        return f"Average Sales: ${avg:.2f}"

    else:
        return "Sorry, I don't understand that question."


# Test the AI Agent
if __name__ == "__main__":
    while True:
        question = input("Ask MetricMind: ")
        if question.lower() == "exit":
            break
        print(ask_agent(question))