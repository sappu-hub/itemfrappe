// Copyright (c) 2024, Faris Ansari and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Quantity of Article Available", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Quantity of Article Available', {
    article: function (frm) {
        if (frm.doc.article) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'article',
                    name: frm.doc.article
                },
                callback: function (response) {
                    if (response.message) {
                        let article = response.message;
                        frm.set_value('current_quantity', article.available_quantity);
                    }
                }
            });
        }
    }
});

