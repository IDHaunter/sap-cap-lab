# SAP CAP Library Lab Project

This project is a comprehensive laboratory implementation of the **SAP Cloud Application Programming Model (CAP)**. It demonstrates a full-stack application including a data model, business logic services, and a custom SAPUI5 frontend.

## Project Overview

The application implements a simple Book Catalog system where users can browse books and authors, view stock levels, and place orders.

## Project Structure

It contains these folders and files, following our recommended project layout:

File or Folder | Purpose
---------|----------
`app/` | content for UI frontends goes here
`db/` | your domain models and data go here
`srv/` | your service models and code go here
`readme.md` | this getting started guide


├── app/
│   ├── Component.js
│   ├── index.html
│   ├── manifest.json
│   │
│   ├── controller/
│   │   └── Books.controller.js
│   │
│   ├── view/
│   │   └── Books.view.xml
│   │
│   ├── model/
│   │   └── models.js
│   │
│   ├── i18n/
│   │   └── i18n.properties
│   │
│   └── css/
│       └── style.css
│
├── db/
│   ├── schema.cds
│   └── data/
│       ├── sap.cap.library-Authors.csv
│       └── sap.cap.library-Books.csv
│
├── srv/
│   ├── cat-service.cds
│   └── cat-service.js
│
├── package.json
└── package-lock.json

### UI5 initialization processs

                        Browser
                           │
                           ▼
                      index.html
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      load sap-ui-core.js       configure UI5
             │
             ▼
       SAPUI5 Runtime
             │
             ▼
     ComponentSupport
             │
             │ data-name="sap.cap.catalog" (namespace)
             ▼
    sap.cap.catalog.Component
             │
             ▼
       Component.js
             │
             │ manifest: "json"
             ▼
       manifest.json
             │
             │ rootView
             ▼
  sap.cap.catalog.view.Books
             │
             ▼
      Books.view.xml
             │
             │ controllerName
             ▼
  Books.controller.js

## Next Steps

- Open a new terminal and run \`cds watch\`
- (in VS Code simply choose _**Terminal** > Run Task > cds watch_)
- Start with your domain model, in a CDS file in \`db/\`

## Learn More

Learn more at <https://cap.cloud.sap>.

