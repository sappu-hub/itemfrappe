frappe.ui.form.on('Item Price Updator', {
    refresh: function(frm) {
        // Trigger fetching of prices when the form is refreshed
        if (frm.doc.price_updates) {
            frm.doc.price_updates.forEach(row => {
                if (row.item) {
                    fetch_previous_prices(frm, row);
                }
            });
        }
    },
    price_updates_add: function(frm, cdt, cdn) {
        // Trigger fetching of prices when a new row is added
        let row = frappe.get_doc(cdt, cdn);
        if (row.item) {
            fetch_previous_prices(frm, row);
        }
    }
});

frappe.ui.form.on('Price Updates', {
    item: function(frm, cdt, cdn) {
        // Trigger fetching of prices when an item is selected in the child table
        let row = frappe.get_doc(cdt, cdn);
        if (row.item) {
            fetch_previous_prices(frm, row);
        }
    }
});

function fetch_previous_prices(frm, row) {
    frappe.call({
        method: "library_management.library_management.doctype.item_price_updator.item_price_updator.get_previous_prices",
        args: {
            item_code: row.item
        },
        callback: function(r) {
            if (r.message) {
                // Update the child table fields with the fetched prices
                frappe.model.set_value(row.doctype, row.name, "previous_standared_selling", r.message["Standard Selling"] || 0);
                frappe.model.set_value(row.doctype, row.name, "previous_wholesale_rate", r.message["Wholesale"] || 0);
            }
        }
    });
}
