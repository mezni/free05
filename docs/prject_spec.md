Here is the definitive master summary of your EV Charging Discovery Platform MVP. This consolidated breakdown integrates your complete technical stack decisions, structural pipelines, and behavioral analysis data engines into a production-ready architectural spec.
📋 Project Identity & Scope

This platform is a high-performance, on-premises, internet-facing EV Charging Discovery Platform MVP. Its explicit architectural goal is to offer zero-friction, high-velocity charger discovery for drivers, paired with robust multi-tenant control dashboards for station owners (Partners) and Super Admins.

To keep the MVP lightweight and highly maintainable, it bypasses live hardware tracking protocols (like OCPP) and real-time charging/billing sessions, relying instead on manual administrative overrides for charger status updates.
🛠️ Complete Technical Stack

    Core Backend API: Rust powered by Actix-web and SQLx for exceptional memory safety, zero-cost abstractions, and compile-time verified database operations.

    Operational Database: PostgreSQL + PostGIS for high-performance geospatial data queries and native spatial point indexing.

    Analytical Database Tier: MongoDB for flexible, un-schemed storage of semi-structured user interaction logs.

    Asynchronous Message Broker: RabbitMQ serving as the asynchronous ingestion boundary for telemetry data streams.

    Identity & Access Management: Keycloak configured for multi-tenant realm handling and social provider authentication federation.

    Frontend Interfaces:

        Drivers: A cross-platform React Native Mobile App focusing on map exploration and discovery.

        Administrators & Partners: A stateless React Single Page Application (SPA) Web Admin dashboard.

    Perimeter Proxy & Ingress: Nginx acting as a centralized reverse proxy, handling TLS termination, cross-origin security configurations, static asset caching, and route-isolated rate limiting.

📐 Dual-Database Data Model & Segregation

To prevent volatile, high-frequency user actions from interfering with core transactional workflows, the system implements two decoupled data storage zones:
Tier	Database Engine	Primary Entities / Responsibilities	Storage Pattern
Operational Tier	PostgreSQL + PostGIS	Stations, Connectors, Partners, Registered Drivers, Saved Favorites, Station Reviews, Invitations, App Configurations.	Rigid Relational Schemas + Spatial Geometries (SRID 4326) with GIST indexes.
Analytical Tier	MongoDB	Clickstream behavioral events, screen transitions, tap coordinates, search keywords.	Loose, un-schemed BSON documents to accept dynamic, evolving event tracking attributes.
⚙️ Core Runtime Pipelines
1. Real-Time Spatial Discovery (Driver Core)

When an anonymous guest or authenticated driver opens the map view in the React Native client:

    The app issues an optimized request to /api/v1/public/stations containing coordinates (lat/lng) and search radius bounds.

    The request hits Nginx, passes a dedicated public rate limiter, and transfers to the Actix-web worker.

    Actix-web pulls a connection from its read-only SQLx pool and executes a native PostGIS distance evaluation bounding-box query:
    WHERE ST_DWithin(geom::geography, ST_MakePoint(lng, lat)::geography, radius_meters)

    Highly optimized location data arrays are returned as a unified JSON vector frame to the app, achieving sub-millisecond query execution times on the server.

2. Asynchronous Telemetry Ingestion (Clickstream Pipeline)

To capture user behavioral context without locking backend execution threads or impacting driver responsiveness:

    The React Native app logs taps and navigation changes inside a local client buffer, flushing payloads out in batches of 10 or upon a major screen view transition.

    Payloads are dispatched via a high-volume route to Nginx (/api/v1/public/telemetry) that is protected by an independent, high-burst rate-limiting zone.

    The Actix-web endpoint parses the array batch, fires the event frames straight to a RabbitMQ exchange (telemetry.events), and instantly throws back an HTTP 202 Accepted status code to the mobile device.

    An independent, background Rust processing loop pulls message frames asynchronously off the RabbitMQ queue, maps them to native BSON formats, and writes them cleanly into MongoDB in bulk packets, acknowledging consumption to the broker once verified.

3. Identity, Onboarding & The BFF Boundary

    The BFF Security Pattern: To safeguard administrative credentials from Cross-Site Scripting (XSS) risks, the React SPA never handles raw Keycloak access tokens. Instead, the Rust backend intercepts the authorization flow server-side and maps administrative credentials to an encrypted, secure HttpOnly, SameSite=Strict cookie bound to the browser.

    The Operator Onboarding Loop: Super Admins can invite new operators. The system logs a secure UUID token into a local invitation ledger and dispatches a verification link via an external SMTP gateway over the internet hook. When the operator registers, the backend leverages Keycloak’s Admin REST API to programmatically provision the identity record while local database references link them exclusively to their assigned partner tenant context.

    Dynamic Client Customization: At boot time, the React Native client calls a public configurations endpoint. The server responds with active administrative details (custom logos, system colors, fallback search radii) dynamically driven by entries in the database, enabling immediate over-the-air theme updates without requiring application store re-approvals.

🔒 Perimeter Isolation Architecture

The entire application topology is housed within a single, secure on-premises container network structure. All infrastructure nodes—PostgreSQL, MongoDB, Keycloak, and RabbitMQ—have no exposed ports map-bound to the host operating system. Nginx stands as the absolute perimeter entry point, securely isolating background network communication over a private internal bridge network.


