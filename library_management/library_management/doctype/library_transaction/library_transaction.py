import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
import datetime

class Librarytransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.update_quantity(-1)  # Reduce quantity by 1
            # Set the article status to "Issued"
            article = frappe.get_doc("article", self.article)
            if article.available_quantity == 0:
                article.status = "issued"
                article.save()
            
        elif self.type == "Return":   
            article = frappe.get_doc("article", self.article)   
            article.available_quantity = int(article.available_quantity) + 1  
            article.status = "available"   
            article.save()

    def after_insert(self):
        # Create a To-Do entry
        self.create_todo_entry()

    def create_todo_entry(self):
        # Fetch the article name from the transaction
        article = self.article  # Assuming article_name is a field in Library Transaction

        # Create a new ToDo entry
        todo = frappe.get_doc({
            "doctype": "ToDo",
            "description": f"{article}",
            "assigned_by": frappe.session.user,
            "reference_type": "Library transaction",
            "reference_name": self.name,  # Link to the current transaction
            "priority": "Medium",  # Optional: Set priority
            "status": "Open"  # Default status
        })
        todo.insert(ignore_permissions=True)  # Ignore permissions to allow creation
        frappe.db.commit()  # Commit the transaction

    


    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("article", self.article)
        # article cannot be issued if it is already issued
        if article.status == "issued":
            frappe.throw("Article is already issued by another member")
        # Check available quantity
        quantity_doc = frappe.get_doc("article", {"name": self.article})
        available_quantity = int(quantity_doc.available_quantity)
        if available_quantity <= 0:
            frappe.throw("No available copies for this article.")   

    def validate_return_period(self):
        """Check if the article is returned after the loan period."""
        if self.Return_date and self.Issue_date:  # Ensure both dates are set
            loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
            days_borrowed = frappe.utils.date_diff(self.Return_date, self.date)

            # Show a message if the loan period is exceeded
            if days_borrowed > loan_period:
                frappe.msgprint(
                    f"Loan period of {loan_period} days exceeded. Borrowed for {days_borrowed} days."
            )
                

    # def validate_return(self):
    #     article = frappe.get_doc("article", self.article)
    #     # article cannot be returned if it is not issued first
    #     if article.status == "available" :
    #         frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "type": "Issue", "docstatus": DocStatus.submitted()},
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # check if a valid membership exists for this library member
        valid_membership = frappe.db.exists(
            "Library membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

    def update_quantity(self,change_quantity):
        
        quantity_doc = frappe.get_doc("article", {"name": self.article})
        if not quantity_doc:
            frappe.throw(f"Quantity record for article '{self.article}' not found.")
        
        # Update current quantity and total quantity
        quantity_doc.available_quantity = int(quantity_doc.available_quantity) - 1
        
        if quantity_doc.available_quantity < 0:
            frappe.throw("Available quantity cannot be negative.")
        if quantity_doc.available_quantity < 0:
            frappe.throw("Total quantity cannot be negative.")
        
        quantity_doc.save()

        quantity_doc.save()

        frappe.logger().info(
            f"Updated Article {self.article}: available_quantity = {quantity_doc.available_quantity}"
        )

    