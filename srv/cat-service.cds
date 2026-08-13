using { sap.cap.library as my } from '../db/schema';

service CatalogService {
    @odata.draft.enabled
    entity Books as projection on my.Books;

    entity Authors as projection on my.Authors;

    action submitOrder (bookId : UUID, quantity : Integer) returns String;

    function getDiscount(bookId : UUID) returns Decimal;
}