import frappe

def update_foundation_cost(doc, method):
    """Update the Foundation cost in the Project's Budget Table when Timesheet is submitted."""
    if not doc.project or not doc.custom_total_cost:
        return

    # Get the Project
    project = frappe.get_doc("Project", doc.project)

    # Try finding the Foundation entry
    updated = False
    for item in project.get("budget_table", []):
        if item.expense_type and item.expense_type.lower() == "foundation":
            item.amount = (item.amount or 0) + doc.custom_total_cost
            updated = True
            break

    # If not found, add a new entry
    if not updated:
        project.append("budget_table", {
            "expense_type": "Foundation",
            "amount": doc.custom_total_cost,
            "remarks": "Added from Timesheet"
        })

    project.save()
