using { sap.cap.library as my } from '../db/schema';

service CatalogService {
    @odata.draft.enabled
    entity Books as projection on my.Books;

    entity Authors as projection on my.Authors;

    action submitOrder (bookId : UUID, quantity : Integer) returns String;
}

// ------------------------------------------------------------------
// UI Annotations - This tells Fiori how to render the UI
// ------------------------------------------------------------------

annotate CatalogService.Books with @(
    UI: {
        SelectionFields: [ title ],

        LineItem: [
            { Value: title, Label: 'Title' },
            { Value: stock, Label: 'Current Stock' },
            { Value: author.name, Label: 'Author' }
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

annotate CatalogService.Books with {
    ID     @UI.Hidden;
    title  @mandatory;
    stock  @Common.Label: 'Stock';

    author_ID @Common: {
        Label     : 'Author',
        Text      : author.name,
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