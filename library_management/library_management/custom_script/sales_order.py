import frappe

def after_insert(self):
        # Create a To-Do entry
        self.create_todo_entry()

def create_todo_entry(self,args):
        # Fetch the article name from the transaction
        customer = self.customer  # Assuming article_name is a field in Library Transaction

        # Create a new ToDo entry
        todo = frappe.get_doc({
            "doctype": "ToDo",
            "description": f"{customer}",
            "assigned_by": frappe.session.user,
            "reference_type": "Sales Order",
            "reference_name": self.name,  # Link to the current transaction
            "priority": "Medium",  # Optional: Set priority
            "status": "Open",  # Default status
        })
        todo.insert(ignore_permissions=True)  # Ignore permissions to allow creation
        frappe.db.commit()  # Commit the transaction
