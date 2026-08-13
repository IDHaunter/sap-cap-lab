using { sap.cap.library as my } from '../db/schema';

service CatalogService {
    @odata.draft.enabled
    entity Books as projection on my.Books;

    entity Authors as projection on my.Authors;

    action submitOrder (bookId : UUID, quantity : Integer) returns String;

    function getDiscount(bookId : UUID) returns Decimal;
}

// ------------------------------------------------------------------
// UI Annotations - This tells Fiori how to render the UI
// ------------------------------------------------------------------

// Annotations for the Books entity entirely
annotate CatalogService.Books with @(
    UI: {
        SelectionFields: [ title ],

        LineItem: [
            { Value: title, Label: 'Title', ![@HTML5.CssDefaults]: { width: '50%' } },
            { Value: stock, Label: 'Current Stock', ![@HTML5.CssDefaults]: { width: '20%' } },
            { Value: author.name, Label: 'Author', ![@HTML5.CssDefaults]: { width: '30%' } }
        ],

        HeaderInfo: {
            TypeName: 'Book',
            TypeNamePlural: 'Books',
            Title: { Value: title },
            Description: { Value: author.name }
        },

        // Fields shown in the Object Page header area (below the title)
        Identification: [
            { Value: title },
            { Value: stock },
            { Value: author_ID }
        ],

        // Sections of the Object Page
        Facets: [
            {
                $Type: 'UI.ReferenceFacet',
                Label: 'Book Details',
                Target: '@UI.FieldGroup#Details'
            }
        ],

        FieldGroup#Details: {
            Data: [
                { Value: title },
                { Value: stock },
                { Value: author_ID }
            ]
        }
    }
);

// Annotations for the each field in the Books entity
annotate CatalogService.Books with {
    ID @UI.Hidden;
    title @mandatory @Common.Label: 'Title';
    stock @mandatory @Common.Label: 'Stock';

    author @Common: {
        Label: 'Author',
        Text: author.name,
        TextArrangement: #TextOnly,
        ValueListWithFixedValues: false,
        ValueList: {
            CollectionPath: 'Authors',
            Parameters: [
                { $Type: 'Common.ValueListParameterInOut', LocalDataProperty: author_ID, ValueListProperty: 'ID' },
                { $Type: 'Common.ValueListParameterDisplayOnly', ValueListProperty: 'name' }
            ]
        }
    };
};