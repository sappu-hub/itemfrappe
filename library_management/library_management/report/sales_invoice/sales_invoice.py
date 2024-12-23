import frappe

def execute(filters=None):
    # Define columns
    columns = [
        {
            "fieldname": "invoice_number",
            "label": "Sales Invoice Number",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 200,
        },
        {
            "fieldname": "customer",
            "label": "Customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 300,
        },
        {
            "fieldname": "item",
            "label": "Item",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200,
        },
        {
            "fieldname": "invoice_date",
            "label": "Invoice Date",
            "fieldtype": "Date",
            "width": 150,
        },
        
    ]

    # Initialize conditions for SQL query
    conditions = []

    # Add condition for company filter if provided
    if filters.get("company"):
        conditions.append("si.company = %(company)s")

    # Add condition for customer filter if provided
    if filters.get("customer"):
        conditions.append("si.customer = %(customer)s")

    # Add condition for item filter if provided
    if filters.get("item"):
        conditions.append("sii.item_code = %(item)s")

    # Add condition for from_date filter if provided
    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")

    # Add condition for to_date filter if provided
    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")

    # Combine conditions into WHERE clause
    where_clause = " AND ".join(conditions) if conditions else ""

    # Fetch data from Sales Invoice doctype
    data = frappe.db.sql(
        f"""
        SELECT 
            si.name AS invoice_number, 
            si.customer AS customer,
            sii.item_code AS item,
            si.posting_date AS invoice_date
        FROM 
            `tabSales Invoice` si
        INNER JOIN 
            `tabSales Invoice Item` sii ON si.name = sii.parent
        WHERE 
            si.docstatus = 1
            {f" AND {where_clause}" if where_clause else ""}
        """,
        filters,
        as_dict=True
    )

    

    # Return columns, data, 
    return columns, data,
