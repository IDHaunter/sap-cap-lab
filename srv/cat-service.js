const cds = require('@sap/cds')

module.exports = cds.service.impl(async function() {
    const { Books } = this.entities

    /**
     * AFTER hook: Logic executed after data is read from the database.
     * We dynamically modify the title for books with low stock.
     */
    this.after('READ', 'Books', (each) => {
        if (each.stock < 7) {
            each.title += ' -- LOW STOCK!'
        }
    })

    /**
     * ON hook: Implementation of the 'submitOrder' action.
     * Decreases book stock if enough is available.
     */
    this.on('submitOrder', async (req) => {
        const { bookId, quantity } = req.data

        // Validate that quantity is a positive number
        if (quantity <= 0) return req.error(400, 'Order quantity must be greater than zero')

        // Atomic update: decrease stock only if it's greater than or equal to requested quantity
        const updatedRows = await UPDATE(Books)
            .set({ stock: { '-=': quantity } })
            .where({ ID: bookId, and: { stock: { '>=': quantity } } })

        // If no rows were updated, it means book doesn't exist or not enough stock
        if (updatedRows === 0) {
            return req.error(409, 'Insufficient stock or book not found')
        }

        return `Success! Order for ${quantity} items has been placed.`
    })

    /**
     * FUNCTION:
     * Calculates the discount percentage based on book price.
     *
     * < 20     -> 0%
     * < 50     -> 5%
     * < 100    -> 10%
     * < 200    -> 15%
     * >= 200   -> 20%
     */
    this.on('getDiscount', async (req) => {

        const { bookId } = req.data

        const book = await SELECT.one
            .from(Books)
            .where({ ID: bookId })

        if (!book) {
            return req.error(404, 'Book not found')
        }

        const price = Number(book.price)

        if (price < 20) {
            return 0
        }

        if (price < 50) {
            return 5
        }

        if (price < 100) {
            return 10
        }

        if (price < 200) {
            return 15
        }

        return 20
    })
})