Based on your architecture, here are the official Functional Specifications (what the system must do) and Non-Functional Specifications (how well the system must perform) tailored for your on-premises EV Charging Discovery Platform MVP.
📋 1. Functional Specifications
A. Driver Features (React Native Mobile App)

    Anonymous Spatial Search: Drivers must be able to view an interactive map and search for charging stations within a specific radius based on their device's GPS coordinates or a manually selected location, without being forced to log in.

    Station & Connector Details: The system must display station name, operating partner, physical address, real-time availability status, operational hours, and a granular breakdown of available connectors (e.g., Type 2, CCS2, power output in kW).

    Driver Authentication: Drivers must have the option to register and authenticate via social identity providers (Google and Facebook OAuth) orchestrated through Keycloak.

    Favorites & Personalization: Authenticated drivers must be able to save specific charging stations to a personal "Favorites" list for rapid access.

    Reviews & Ratings: Authenticated drivers must be able to submit a text review and a 1-to-5 star rating for stations they have visited.

    Over-The-Air Branding Injection: The mobile client must fetch a boot configuration API on startup to dynamically render system-wide visual styles (logos, primary/secondary colors, and fallback search ranges) managed by the Super Admin.

    Batched Interaction Telemetry: The app must track user behavioral events (map clicks, screen views, search terms), store them in a local buffer, and send them to the backend in batches of 10 events (or upon screen exit) to conserve battery and bandwidth.

B. Partner / Operator Features (React SPA Web Portal)

    Station Management: Verified partners must be able to add, modify, or delete charging stations and individual connectors under their exclusive tenant ownership.

    Manual Status Overrides: Because the MVP bypasses dynamic hardware protocols (OCPP), operators must have a manual toggle interface to immediately mark a charger's status as Available, Occupied, In Maintenance, or Offline.

    Multi-Tenant Isolation: Partner users must only see, edit, and access telemetry metrics for stations bound directly to their specific business organization.

C. Super Admin Features (React SPA Web Portal)

    Partner Onboarding & Invitation Loop: Super Admins must be able to invite new business partners by submitting their email address. The system will generate a secure, single-use UUID token and send an activation link via SMTP.

    Tenant Management: Admins must have global permissions to approve, suspend, or terminate Partner tenants and review all operational metrics across the network.

    Global Client Design Management: Admins must have a portal to upload corporate logos, update brand colors, and alter configuration constraints, updating the mobile app's appearance instantly.

⚡ 2. Non-Functional Specifications
A. Performance & Scalability

    Sub-Millisecond Spatial Resolution: The Rust Actix-web backend, leveraging pooled SQLx connections and spatial GiST indexing, must execute geographic bounding-box queries (ST_DWithin) in under 15ms under baseline loads.

    Telemetry Ingestion Offloading: The telemetry endpoint must achieve an HTTP response time of under 5ms by immediately offloading incoming data batches to RabbitMQ and returning an HTTP 202 Accepted packet to the client before any database write occurs.

    Asynchronous Processing Backpressure: The independent background worker thread must safely absorb clickstream surges by queuing events in RabbitMQ, ensuring that even if MongoDB writes slow down to 1,000 writes/sec, the public-facing API remains completely unaffected.

B. Security & Identity Assurance

    BFF Token Shielding: The system must implement a Backend-for-Frontend (BFF) pattern for the React SPA. Privileged Keycloak tokens must be handled strictly on the server-side Rust layer and mapped to the browser via encrypted, HttpOnly, SameSite=Strict, and Secure cookies to eliminate XSS-based token theft.

    Perimeter Network Isolation: The on-premises deployment must expose only ports 80 and 443 through Nginx to the host operating system. PostgreSQL, MongoDB, RabbitMQ, and Keycloak must remain completely hidden inside an isolated internal Docker bridge network.

    Granular API Rate Limiting: Nginx must enforce strict rate-limiting policies at the edge to mitigate Denial-of-Service vectors:

        Public API / Discovery: Maximum 15 requests/sec per IP, with a burst buffer of 25.

        Telemetry Ingestion: Maximum 30 requests/sec per IP, with a burst buffer of 50.

        Admin / Partner API: Maximum 5 requests/sec per IP, with a burst buffer of 10.

C. Availability & Reliability

    Telemetry Fault Tolerance: If the MongoDB analytics database goes offline for routine maintenance, RabbitMQ must safely queue message frames without dropping data. The background worker will resume consumption and process the backlog seamlessly once the MongoDB container recovers.

    Persistent Docker Storage: All analytical data, transactional records, message state queues, and Keycloak identities must utilize native Docker volumes mapped directly to local host directories to ensure data persistence across system reboots or container upgrades.

D. Maintainability & Constraints

    Schema Flexibility: Analytical payloads stored inside MongoDB must use an open BSON structure, allowing the development team to change mobile client tracking properties without modifying database schemas or running SQL migration scripts.

    Single-Machine Portability: The entire system architecture must compile, deploy, and execute on a single on-premises linux instance using standard Docker Compose command wrappers, meeting the rapid-delivery requirements of a 1-month MVP timeline.