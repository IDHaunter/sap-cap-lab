# SAP CAP Library Lab Project

This project is a comprehensive laboratory implementation of the **SAP Cloud Application Programming Model (CAP)**. It demonstrates a full-stack application including a data model, business logic services, and a custom SAPUI5 frontend.

## Project Overview

The application implements a simple Book Catalog system where users can browse books and authors, view stock levels, edit parameters.

## Project Structure

.
├── app/                          # Frontend applications (simple UI5 testing and two sap fiori apps)
│   ├── controller/               # UI5 Controllers for logic
│   │   └── Books.controller.js
│   ├── model/                    # Data models and configurations
│   │   └── models.js
│   ├── view/                     # UI5 XML Views for the layout
│   │   └── Books.view.xml
│   ├── css/                      # Stylesheets
│   │   └── style.css
│   ├── i18n/                     # Internationalization files (translations)
│   │   └── i18n.properties
│   ├── authorslist/              # Separate app for Authors list
│   │   ├── webapp/               # Web application assets
│   │   ├── package.json          # Dependencies for authorslist
│   │   └── ... (UI5 configurations like ui5.yaml)
│   ├── bookslist/                # Separate app for Books list
│   │   ├── webapp/               # Web application assets
│   │   ├── package.json          # Dependencies for bookslist
│   │   └── ... (UI5 configurations like ui5.yaml)
│   ├── Component.js              # Main UI5 component definition
│   ├── manifest.json             # Application descriptor
│   └── index.html                # Entry point for the application
├── db/                            # Database layer (CAP CDS models)
│   ├── schema.cds                # Data model definitions (Entities)
│   └── data/                     # Seed data (CSV files)
│       ├── sap.cap.library-Books.csv
│       └── sap.cap.library-Authors.csv
├── srv/                           # Service layer (OData services)
│   ├── cat-service.cds           # Service definition (API endpoints)
│   ├── cat-service-ui.cds        # UI annotations for the service
│   └── cat-service.js            # Custom business logic for the service
├── db.sqlite                     # SQLite database file
├── package.json                  # Root project dependencies and scripts
├── readme.md                     # Project documentation
├── how_to_sap_cap.txt            # Guide on using SAP CAP
└── js_sap-cap-lab.postman_collection.json # Postman collection for API testing

## Start locally

terminal 1 (root folder):
    cds watch
terminal 2:
    cd ./app/bookslist
    npm start
terminal 3:
    cd ./app/authorslist
    npm start

## Deployment in BTP

terminal 1 (root folder):
    npx cds build --production
    mbt build
    cf deploy ./mta_archives/sap-cap-lab_1.0.0.mtar
