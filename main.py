
import csv

print("Program starting...")

# -----------------------
# UC1 - Load ticket data
# -----------------------
def load_ticket_data(filename):
    """
    Loads ticket data from a CSV file.
    Returns a list of dictionaries (one per row).
    """
    ticket_data = []

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                ticket_data.append(row)

        print(f"Loaded {len(ticket_data)} rows from {filename}")
        return ticket_data

    except FileNotFoundError:
        print("Error: CSV file not found.")
        return []

    except Exception:
        print(f"An unexpected error occurred while reading the file: {e}")
        return []  


# -----------------------
# UC2 - Extract categories
# -----------------------

def get_categories(ticket_data):
    """
    Extracts and returns a sorted list of unique ticket categories.
    Works even if the CSV header is 'Category' or 'Category '.
    """
    categories = set()

    for row in ticket_data:
        category = (row.get("Category") or row.get("Category ") or "").strip()
        if category:
            categories.add(category)

    return sorted(categories)
# -----------------------
# UC3 - Show top-ups for a category
# -----------------------
def get_topups_for_category(ticket_data, category):
    topups = set()
    category = category.strip()

    for row in ticket_data:
        row_category = row.get("Category ", "").strip()
        if row_category == category:
            topup = row.get("TopUp", "").strip()
            if topup:
                topups.add(topup)

    return sorted(topups)

# -----------------------
# UC4 - Show details for a chosen top-up
# -----------------------
def get_topup_details(ticket_data, category, topup_name):
    """
    Returns the first matching row (dictionary) for a given category + topup.
    If not found, returns None.
    """
    for row in ticket_data:
        row_category = (row.get("Category") or row.get("Category ") or "").strip()
        row_topup = (row.get("TopUp") or "").strip()

        if row_category == category.strip() and row_topup == topup_name.strip():
            return row

    return None


# -----------------------
# UC5 - Purchases
# -----------------------

def get_value(row, key):
    """Safely get a cleaned string value from a row dict for both 'key' and 'key '."""
    return (row.get(key) or row.get(key + " ") or "").strip()


def ask_int(prompt, min_val, max_val):
    """Ask for an integer in range [min_val, max_val]. Keeps prompting until valid."""
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            n = int(s)
            if min_val <= n <= max_val:
                return n
        print(f"Please enter a number between {min_val} and {max_val}.")


def ask_yes_no(prompt):
    """Ask a yes/no question. Returns True for yes, False for no."""
    while True:
        s = input(prompt).strip().lower()
        if s in ("y", "yes"):
            return True
        if s in ("n", "no"):
            return False
        print("Please type y or n.")

def purchase_flow(ticket_data):
    """
    UC5: lets user choose a category and top-up, confirms purchase,
    and returns a purchase record dict (or None if cancelled).
    """

    categories = get_categories(ticket_data)
    if not categories:
        print("No categories available.")
        return None

    print("\nChoose a category:")
    for i, c in enumerate(categories, start=1):
        print(f"{i}. {c}")

    cat_choice = ask_int("Enter category number: ", 1, len(categories))
    selected_category = categories[cat_choice - 1]

    topups = get_topups_for_category(ticket_data, selected_category)
    if not topups:
        print("No top-ups found for that category.")
        return None

    print(f"\nChoose a TopUp for {selected_category}:")
    for i, t in enumerate(topups, start=1):
        print(f"{i}. {t}")

    top_choice = ask_int("Enter top-up number: ", 1, len(topups))
    selected_topup = topups[top_choice - 1]

    details = get_topup_details(ticket_data, selected_category, selected_topup)
    if details is None:
        print("Could not find details for that selection.")
        return None

    price = (details.get("Price") or details.get("Price ") or "").strip()

    print(f"\nYou selected: {selected_category} -> {selected_topup}")
    print(f"Price: {price}")

    if not ask_yes_no("Confirm purchase? (y/n): "):
        print("Purchase cancelled.")
        return None

    purchase = {
        "Category": selected_category,
        "TopUp": selected_topup,
        "Price": price
    }

    print(" Ticket purchase successful.")
    return purchase   

# -----------------------
# UC6 - Save purchases to a file
# -----------------------
def save_purchases(purchases, filename="purchases.csv"):
    """
    Saves the list of purchase dictionaries to a CSV file.
    """
    if not purchases:
        print("No purchases to save.")
        return

    fieldnames = ["Category", "TopUp", "Price"]

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for p in purchases:
                writer.writerow({
                    "Category": p.get("Category", ""),
                    "TopUp": p.get("TopUp", ""),
                    "Price": p.get("Price", "")
                })

        print(f"Saved {len(purchases)} purchase(s) to {filename}")

    except Exception as e:
        print(f"Error saving purchases: {e}")

# -----------------------
# UC7 - Load purchases from a file
# -----------------------
def load_purchases(filename="purchases.csv"):
    """
    Loads purchases from a CSV file and returns a list of dictionaries.
    If the file doesn't exist yet, returns an empty list (no crash).
    """
    purchases = []

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                purchases.append({
                    "Category": (row.get("Category") or "").strip(),
                    "TopUp": (row.get("TopUp") or "").strip(),
                    "Price": (row.get("Price") or "").strip()
                })

        print(f"Loaded {len(purchases)} previous purchase(s) from {filename}")
        return purchases

    except FileNotFoundError:
       
        print("No previous purchases found (purchases.csv not created yet).")
        return []

    except Exception as e:
        print(f"Error loading purchases: {e}")
        return []

# -----------------------
# Program execution
# -----------------------
tickets = load_ticket_data("tickets.csv")

categories = get_categories(tickets)

print("Available Ticket Categories:")

for category in categories:
    print("-", category)

print("Total categories:", len(categories))

selected_category = "Adult" 

topups = get_topups_for_category(tickets, selected_category)

print(f"Available TopUps for {selected_category}:")
for topup in topups:
    print("-", topup)

# -----------------------
# UC4 test: choose first top-up from the list
# -----------------------
if topups:
    selected_topup = topups[0]
    details = get_topup_details(tickets, selected_category, selected_topup)

    print(f"\nTopUp details for {selected_topup} ({selected_category}):")
    if details is not None:
        price = (details.get("Price") or details.get("Price ") or "").strip()
        print("Price:", price)
    else:
        print("No details found for that selection.")
else:
    print("No top-ups found to show details.")

# -----------------------
# UC5/UC7 Program execution
# -----------------------

purchases = load_purchases("purchases.csv") #UC7

while True:
    p = purchase_flow(tickets)
    if p is not None:
        purchases.append(p)

    if not ask_yes_no("\nBuy another ticket? (y/n): "):
        break

print("\nPurchases made this session:")
for p in purchases:
    print(p)

save_purchases(purchases) #UC6




    

