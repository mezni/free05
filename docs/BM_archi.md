[ FRONTEND LAYER ]
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
     [ User App ]          [ Admin Portal ]       [ Partner Portal ]
   (React / Leaflet)       (React / Tailwind)     (React / Tailwind)
          │                       │                       │
          │ (REST + JWT)          │ (REST + JWT)          │ (REST + JWT)
          └───────────────────────┼───────────────────────┘
                                  ▼
                          [ API GATEWAY LAYER ]
                         [ Envoy / Nginx Proxy ]
                           (Rate Limit & Route)
                                  │
                  ┌───────────────┴───────────────┐
                  │ (Stateless JWKS Token Check)  │ (Async Clickstream)
                  ▼                               ▼
       =======================================================
       ||                  RABBITMQ BROKER                  ||
       =======================================================
          │                  │                    │
          │ (Sync gRPC)      │ (Clickstream Log)  │ (Data Sync Events)
          ▼                  ▼                    ▼
   [ CORE BACKEND ]   [ ANALYTICS WORKER ]  [ GEOSPATIAL SERVICE ]
   [ Admin Service ]  [ Clickstream Ingest] [   Locate Service   ]
     (Rust / Axum)       (Rust Consumer)       (Rust / Axum)
          │                                       │
          ▼                                       ▼
     [ STATE ]                                [ STATE ]
    [ App DB ]                              [ PostGIS DB ]
    (Postgres)                              (Postgres + PostGIS)
          ▲                                       
          │ (Sync HTTP/gRPC Administration)       
          ▼                                       
  [ Keycloak Server ] ──────────────────────► [ Keycloak DB ]
   (Quarkus / IAM)                              (Postgres)


Layer-by-Layer Architectural Specifications
1. Frontend Layer (React Ecosystem)

    Tech Stack: React, Tailwind CSS, TanStack Query (for smart data caching/polling), React Leaflet (to interact with map data).

    Auth Handling: The apps perform a standard OpenID Connect (OIDC) Authorization Code Flow directly against Keycloak to obtain a Access/Refresh token pair. The frontend attaches this JWT to the Authorization: Bearer <token> header for all backend requests.

2. Traffic Control & Security Layer (API Gateway)

    Tech Stack: Nginx or Envoy Proxy.

    Responsibilities: Edge rate limiting, TLS termination, and centralized path routing.

    Stateless Auth Verification: The gateway fetches Keycloak's public keys via its JWKS (/protocol/openid-connect/certs) endpoint at boot and caches them. For every incoming request, it cryptographically verifies the JWT signature in-memory.

        Result: Request validation takes < 1ms and never bottlenecks Keycloak. Validated headers (e.g., X-User-Id, X-User-Roles) are cleanly forwarded downstream.

3. Asynchronous Backbone (RabbitMQ Broker)

Acts as the central nervous system for decoupling heavy writes and background changes. It manages two main exchanges:

    clickstream.exchange (Direct/Fanout): Frontend click events hit the Gateway, which immediately drops them here and returns a quick HTTP 202 Accepted to the client. A lightweight Clickstream Ingest Rust worker pulls these down to process or dump into long-term data lakes.

    data-sync.exchange (Topic): Solves database isolation data-drift. When an entity changes, it broadcasts an event here.

4. Microservices & Isolated Storage Layer (Rust & Postgres)
Identity & Access Management (IAM)

    Components: Keycloak Server + Keycloak DB (PostgreSQL).

    Role: Keycloak manages realms, clients, user federations, and password hashing. It stays entirely isolated in its own database to satisfy security compliance.

Admin Service

    Components: Rust Backend (Axum/Tokio) + App DB (PostgreSQL).

    Role: Handles core domain logic (managing accounts, registrations, partners, system configurations).

    Inter-service Flows: * To Keycloak: Uses synchronous HTTP/gRPC administration APIs to provision or modify users when triggered by an operator in the Admin Portal.

        To RabbitMQ: When an asset or partner is updated, it saves to App DB and fires a partner.updated event to RabbitMQ.

Locate Service

    Components: Rust Backend (Axum/Tokio) + PostGIS DB (PostgreSQL + Spatial Extensions).

    Role: Handles high-throughput vehicle/driver tracking, coordinate storage, geofencing, and proximity calculations.

    Inter-service Flows: It consumes the partner.updated event from RabbitMQ to automatically sync internal metadata tables in its PostGIS DB without ever querying the Admin Service directly.

🚀 Key Architectural Advantages of This Design

    Impenetrable Fault Isolation: If the Locate Service or its specialized spatial DB experiences a massive query strain or crashes, users can still securely log in, open portals, and manage their admin operations without interruption.

    No Distributed Database Deadlocks: By forcing the Admin and Locate databases to talk through asynchronous RabbitMQ events instead of shared tables or synchronous locks, you eliminate database-level dependencies.

    Blazing Fast Performance: Rust's async runtime (Tokio) handles incoming Gateway routes seamlessly. Because auth checks are entirely stateless (via local JWKS caching), your internal network latency remains incredibly close to bare metal.   
