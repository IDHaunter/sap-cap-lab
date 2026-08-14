using { sap.cap.library as my } from '../db/schema';

@requires: 'authenticated-user'
service CatalogService {
    @odata.draft.enabled
    @restrict: [
        { grant: 'READ', to: ['Reader', 'Admin'] },
        { grant: ['CREATE', 'UPDATE', 'DELETE'], to: 'Admin' }
    ]
    entity Books as projection on my.Books;

    @odata.draft.enabled
    @restrict: [
        { grant: 'READ', to: ['Reader', 'Admin'] },
        { grant: ['CREATE', 'UPDATE', 'DELETE'], to: 'Admin' }
    ]
    entity Authors as projection on my.Authors;

    @requires: 'Admin'
    action submitOrder (bookId : UUID, quantity : Integer) returns String;

    @requires: ['Reader', 'Admin']
    function getDiscount(bookId : UUID) returns Decimal;
}