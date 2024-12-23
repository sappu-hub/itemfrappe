
# # import frappe
# # from frappe.model.document import Document

# # class ItemPriceUpdator(Document):
# #     def validate(self):
# #         # Loop through each row in the Price Updates child table
# #         for row in self.price_updates:
# #             # Fetch the item from the child table
# #             item_code = row.item
# #             standared_selling = row.standared_selling
# #             wholesale_rate = row.wholesale_rate

# #             # Update the Standard Selling Price in Item Price
# #             if standared_selling:
# #                 self.update_item_price(item_code, "Standard Selling", standared_selling)

# #             # Update the Wholesale Rate in Item Price
# #             if wholesale_rate:
# #                 self.update_item_price(item_code, "Wholesale", wholesale_rate)

# #         frappe.msgprint("Item prices updated.")

# #     def update_item_price(self, item_code, price_list, price_value):
# #         # Check if the Item Price record exists
# #         item_price = frappe.db.exists(
# #             "Item Price",
# #             {"item_code": item_code, "price_list": price_list}
# #         )

# #         if item_price:
# #             # Update the existing Item Price record
# #             item_price_doc = frappe.get_doc("Item Price", item_price)
# #             item_price_doc.price_list_rate = price_value
# #             item_price_doc.save()
# #         else:
# #             # Create a new Item Price record if it doesn't exist
# #             frappe.get_doc({
# #                 "doctype": "Item Price",
# #                 "item_code": item_code,
# #                 "price_list": price_list,
# #                 "price_list_rate": price_value
# #             }).insert()


# import frappe
# from frappe.model.document import Document

# class ItemPriceUpdator(Document):
#     def validate(self):
#         # Loop through each row in the Price Updates child table
#         for row in self.price_updates:
#             # Fetch the item from the child table
#             item_code = row.item

#             # Fetch and display the previously updated prices
#             row.previous_standared_selling = self.get_previous_price(item_code, "Standard Selling")
#             row.previous_wholesale_rate = self.get_previous_price(item_code, "Wholesale")

#             standared_selling = row.standared_selling
#             wholesale_rate = row.wholesale_rate

#             # Update the Standard Selling Price in Item Price
#             if standared_selling:
#                 self.update_item_price(item_code, "Standard Selling", standared_selling)

#             # Update the Wholesale Rate in Item Price
#             if wholesale_rate:
#                 self.update_item_price(item_code, "Wholesale", wholesale_rate)

#         frappe.msgprint("Item prices updated.")

#     def get_previous_price(self, item_code, price_list):
#         # Fetch the existing price for the item and price list
#         item_price = frappe.db.get_value(
#             "Item Price",
#             {"item_code": item_code, "price_list": price_list},
#             "price_list_rate"
#         )
#         return item_price or 0  # Return 0 if no previous price exists

#     def update_item_price(self, item_code, price_list, price_value):
#         # Check if the Item Price record exists
#         item_price = frappe.db.exists(
#             "Item Price",
#             {"item_code": item_code, "price_list": price_list}
#         )

#         if item_price:
#             # Update the existing Item Price record
#             item_price_doc = frappe.get_doc("Item Price", item_price)
#             item_price_doc.price_list_rate = price_value
#             item_price_doc.save()
#         else:
#             # Create a new Item Price record if it doesn't exist
#             frappe.get_doc({
#                 "doctype": "Item Price",
#                 "item_code": item_code,
#                 "price_list": price_list,
#                 "price_list_rate": price_value
#             }).insert()
import frappe
from frappe.model.document import Document

class ItemPriceUpdator(Document):
    def validate(self):
        """
        Validate the document before saving.
        Updates item prices and fetches previous prices to display in the child table.
        """
        # Loop through each row in the Price Updates child table
        for row in self.price_updates:
            # Fetch the item code from the child table
            item_code = row.item

            # Fetch previously saved prices for the item
            previous_prices = self.get_previous_prices(item_code)
            
            # Display the previously saved prices in the child table
            row.previous_standared_selling = previous_prices.get("Standard Selling", 0)
            row.previous_wholesale_rate = previous_prices.get("Wholesale", 0)

            # Update the Standard Selling Price in Item Price
            if row.standared_selling:
                self.update_item_price(item_code, "Standard Selling", row.standared_selling)

            # Update the Wholesale Rate in Item Price
            if row.wholesale_rate:
                self.update_item_price(item_code, "Wholesale", row.wholesale_rate)

        frappe.msgprint("Item prices updated.")

    @staticmethod
    @frappe.whitelist()
    def get_previous_prices(item_code):
        """
        Fetch previously saved prices for the given item.
        Returns a dictionary with price list rates for Standard Selling and Wholesale.
        """
        if not item_code:
            return {}

        # Query the Item Price table to fetch prices
        item_prices = frappe.get_all(
            "Item Price",
            filters={"item_code": item_code},
            fields=["price_list", "price_list_rate"]
        )

        # Initialize the response
        prices = {
            "Standard Selling": 0,
            "Wholesale": 0
        }

        # Populate prices from fetched records
        for price in item_prices:
            if price["price_list"] in prices:
                prices[price["price_list"]] = price["price_list_rate"]

        return prices

    def update_item_price(self, item_code, price_list, price_value):
        """
        Update or create the Item Price record.
        """
        # Check if the Item Price record exists
        item_price = frappe.db.exists(
            "Item Price",
            {"item_code": item_code, "price_list": price_list}
        )

        if item_price:
            # Update the existing Item Price record
            item_price_doc = frappe.get_doc("Item Price", item_price)
            item_price_doc.price_list_rate = price_value
            item_price_doc.save()
        else:
            # Create a new Item Price record if it doesn't exist
            frappe.get_doc({
                "doctype": "Item Price",
                "item_code": item_code,
                "price_list": price_list,
                "price_list_rate": price_value
            }).insert()
