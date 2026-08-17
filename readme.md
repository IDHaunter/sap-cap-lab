# SAP CAP Library Lab Project

This project is a comprehensive laboratory implementation of the **SAP Cloud
Application Programming Model (CAP)**. It demonstrates a full-stack application
including a data model, business logic services, two SAP Fiori frontend
applications, an approuter, and a Python RAG (Retrieval-Augmented Generation)
microservice.

## Project Overview

The application implements a Book Catalog system where users can browse books
and authors, view stock levels, and edit parameters. The project is built with
the SAP CAP framework and deployed as a Multi-Target Application (MTA) to SAP
BTP Cloud Foundry. It is composed of the following main parts:

- **Database layer** (`db/`) – CDS data models and seed data.
- **Service layer** (`srv/`) – OData service definition, UI annotations and
  custom business logic.
- **Frontend layer** (`app/`) – two SAP Fiori applications (`bookslist`,
  `authorslist`) and an approuter (`router`).
- **Python RAG service** (`srv-py-rag/`) – a FastAPI microservice exposing a
  RAG-based API.
- **Deployment** (`mta.yaml`, `xs-security.json`) – MTA descriptor and XSUAA
  security configuration.

The production database is **SAP HANA** (via HDI containers). For local
development, **Postgresql** is used.

## Project Structure

.
├── app/                                    # Frontend applications (Fiori apps + approuter)
│     ├── bookslist/                        # SAP Fiori app – Books List / Object Page
│     │     ├── webapp/                     # Web application assets
│     │     │     ├── Component.js          # App component (sap.fe.core.AppComponent)
│     │     │     ├── index.html            # Entry point / bootstrap
│     │     │     ├── manifest.json         # Application descriptor (routing, data sources)
│     │     │     ├── annotations/          # OData annotation XML
│     │     │     │     └── annotation.xml
│     │     │     ├── ext/                  # Extension code
│     │     │     │     └── controller/
│     │     │     │          └── ObjectPageExt.js   # "View Author" navigation extension
│     │     │     └── i18n/                 # Internationalization resources
│     │     │          └── i18n.properties
│     │     ├── ui5.yaml                    # UI5 build / middleware configuration
│     │     ├── xs-app.json                 # HTML5 app router config (BTP HTML5 repo)
│     │     └── package.json                # Dependencies for bookslist
│     │
│     ├── authorslist/                      # SAP Fiori app – Authors List / Object Page
│     │     ├── webapp/                     # Web application assets
│     │     │     ├── Component.js
│     │     │     ├── index.html
│     │     │     ├── manifest.json
│     │     │     ├── annotations/
│     │     │     │     └── annotation.xml
│     │     │     └── i18n/
│     │     │          └── i18n.properties
│     │     ├── ui5.yaml
│     │     ├── xs-app.json
│     │     └── package.json                # Dependencies for authorslist
│     │
│     └── router/                           # SAP approuter (routes to srv-api, rag-api, HTML5)
│          ├── xs-app.json                  # Approuter route definitions
│          ├── index.js                     # Approuter entry point
│          └── package.json                 # Dependencies (@sap/approuter)
│
├── db/                                     # Database layer (CAP CDS models)
│     ├── schema.cds                        # Data model definitions (Books, Authors entities)
│     └── data/                             # Seed data (CSV files)
│          ├── sap.cap.library-Books.csv
│          └── sap.cap.library-Authors.csv
│
├── srv/                                    # Service layer (OData services)
│     ├── cat-service.cds                   # Service definition (CatalogService, entities, actions)
│     ├── cat-service-ui.cds               # UI annotations for the service
│     └── cat-service.js                   # Custom business logic for the service
│
├── srv-py-rag/                             # Python RAG microservice (FastAPI)
│     ├── app/
│     │     ├── app.py                      # FastAPI application entry point
│     │     ├── settings.py                 # App settings (paths, mode, logging)
│     │     ├── settings_tools.py           # Settings / config parser helpers
│     │     ├── middleware.py               # Authorization middleware
│     │     ├── routes/
│     │     │     ├── root.py               # Root HTML info endpoint
│     │     │     ├── logs.py               # Log file retrieval endpoint (admin)
│     │     │     └── common/
│     │     │          ├── responses.py     # Response / error message builders
│     │     │          └── error_handlers.py    # Global FastAPI error handlers
│     │     ├── utils/
│     │     │     ├── module_logger.py      # Date-rotating logger implementation
│     │     │     └── env_vars.py          # Environment variable helpers
│     │     ├── themes/
│     │     │     └── color_palette.py      # UI theming (light/dark palettes)
│     │     └── static/                    # Static assets (e.g. logo.png)
│     ├── settings.ini                      # Local / prod server configuration
│     └── requirements.txt                  # Python dependencies (fastapi, uvicorn)
│
├── mta.yaml                               # MTA descriptor (modules & resources)
├── xs-security.json                       # XSUAA scopes / role templates
├── package.json                           # Root project dependencies and scripts
├── package-lock.json                      # Root dependency lock file
├── readme.md                              # Project documentation (this file)
└── how_to_sap_cap.txt                     # Guide on using SAP CAP
```

## Deployment Components (from mta.yaml)

| Module | Type | Path | Description |
| --- | --- | --- | --- |
| `sap-cap-lab-srv` | nodejs | `gen/srv` | CAP service (Node.js), requires XSUAA and HANA |
| `sap-cap-lab-db-deployer` | hdb | `gen/db` | Database schema deployer |
| `sap-cap-lab` | approuter.nodejs | `app/router` | Approuter, routes to `srv-api`, `rag-api` and HTML5 repo |
| `sap-cap-lab-app-deployer` | com.sap.application.content | `gen` | Deploys HTML5 apps to the repo |
| `sapcaplabauthorslist` | html5 | `app/authorslist` | Authors List Fiori app |
| `sapcaplabbookslist` | html5 | `app/bookslist` | Books List Fiori app |
| `sap-cap-lab-py-rag` | python | `srv-py-rag` | FastAPI RAG service (`uvicorn app.app:app`) |

Managed resources: `sap-cap-lab-auth` (XSUAA), `sap-cap-lab-db` (HANA HDI),
`sap-cap-lab-html5-repo-host` / `sap-cap-lab-html5-runtime` (HTML5 apps repo),
`sap-cap-lab-destination` (destination service).

## Start locally

**Terminal 1 (CAP backend, root folder):**
```
cds watch
```

**Terminal 2 (Books List Fiori app):**
```
cd ./app/bookslist
npm start
```

**Terminal 3 (Authors List Fiori app):**
```
cd ./app/authorslist
npm start
```

The Fiori apps proxy OData calls to `http://localhost:4004` (see each app's
`ui5.yaml`).

**Python RAG service (optional):**
```
cd ./srv-py-rag
uvicorn app.app:app --host 127.0.0.1 --port 5000
```

## Deployment in BTP

**Terminal 1 (root folder):**
```
npx cds build --production
mbt build
cf deploy ./mta_archives/sap-cap-lab_1.0.0.mtar
```

## Technology & Versions

- **SAP CAP Framework** – core application model
- **Node.js 22** – service and approuter runtime
- **Python 3.12 / FastAPI** – RAG microservice (`srv-py-rag`)
- **SAP HANA** (production) / **Postgresql** (development) – database
- **SAP Fiori / SAPUI5** – frontend applications

## Additional Resources

- `how_to_sap_cap.txt` – step-by-step guide on using SAP CAP.
- `mta.yaml` – the authoritative description of MTA modules and resources.
- `xs-security.json` – XSUAA scopes and role templates (`Admin`, `Reader`).