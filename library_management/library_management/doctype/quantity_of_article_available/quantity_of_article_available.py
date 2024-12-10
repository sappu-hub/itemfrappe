# Copyright (c) 2024, Faris Ansari and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class QuantityofArticleAvailable(Document):
# 	pass
import frappe
from frappe.model.document import Document
from library_management.library_management.doctype.article.article import article


class QuantityofArticleAvailable(Document):
    def validate(self):
        # Ensure current_quantity and new_quantity are valid numbers
        if self.current_quantity is None:
            frappe.throw("Current Quantity cannot be empty.")
        if self.new_quantity is None:
            frappe.throw("New Quantity cannot be empty.")
        
        # Calculate total_quantity
        self.total_quantity = self.current_quantity + self.new_quantity
####
         # Ensure total_quantity is updated in the linked Article
        if self.article:
            self.update_article_available_quantity()

    def update_article_available_quantity(self):
        """
        Updates the available quantity of the linked Article
        based on the total_quantity in QuantityofArticleAvailable.
        """
        # Get the corresponding Article document
        article = frappe.get_doc("article", self.article)
        
        # Set the available_quantity in the Article doctype
        article.available_quantity = self.total_quantity
        
        # Save the updated Article document
        article.save()

        frappe.logger().info(
            f"Updated available_quantity for Article {self.article} to {self.total_quantity}"
        )