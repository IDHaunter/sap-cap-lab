using { sap.cap.library as my } from '../db/schema';

service CatalogService {
    entity Books as projection on my.Books;
    entity Authors as projection on my.Authors;

    // Define a custom action to handle book orders
    action submitOrder (bookId : UUID, quantity : Integer) returns String;
}

// ------------------------------------------------------------------
// UI Annotations - This tells Fiori how to render the UI
// ------------------------------------------------------------------

annotate CatalogService.Books with @(
    UI: {
        // SelectionFields are the filter bar fields at the top
        SelectionFields: [ title ],
        
        // LineItem defines the columns in the main table
        LineItem: [
            { Value: ID, Label: 'Book ID' },
            { Value: title, Label: 'Title' },
            { Value: stock, Label: 'Current Stock' },
            { Value: author.name, Label: 'Author' } // Navigation to Author entity!
        ],
        
        // HeaderInfo defines the title of the page
        HeaderInfo: {
            TypeName: 'Book',
            TypeNamePlural: 'Books',
            Title: { Value: title }
        }
    }
);