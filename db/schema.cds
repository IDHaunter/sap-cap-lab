namespace sap.cap.library;
using { cuid, managed } from '@sap/cds/common';

/**
 * An entity for storing books.
 * Uses cuid for auto-generation of IDs (like author_ID in the CSV)
 * and managed for auditing creation times.
 */
entity Books : cuid, managed {
    title  : String(255);
    stock  : Integer;
    author : Association to Authors;
}

// An entity for storing authors, with a one-to-many relationship to Books.
entity Authors : cuid, managed {
    name  : String(255);
    books : Association to many Books on books.author = $self;
}