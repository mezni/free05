Here is the official Project Constitution (Project Charter) for your EV Charging Discovery Platform MVP, formatted using the strict Spec-Kit methodology. This document serves as the absolute source of truth for the project's authority, boundaries, and delivery constraints.
📜 Project Constitution: Project Everest / AInDrahim

Document Ref: SK-PC-2026-REV2

Date: May 20, 2026

Status: Approved
1. Project Purpose & Intent
1.1 Executive Summary

The goal of this project is to build an independent, highly performant, on-premises, internet-facing Electric Vehicle (EV) Charging Discovery Platform MVP within an aggressive 1-month development cycle. The platform connects EV drivers with local charging stations while giving station operators (Partners) and system administrators a way to manage their infrastructure.
1.2 Core Business Drivers

    Rapid Market Entry: Building a production-ready discovery asset within 30 days.

    On-Premises Autonomy: Deploying fully self-contained infrastructure without relying on expensive, recurring cloud services or external managed APIs.

    Decoupled Analytics: Capturing user behavior metrics early without degrading the core API performance used for charger lookups.

2. Project Scope Boundary
2.1 In-Scope Functional Areas

    Driver Discovery (Mobile): A cross-platform React Native app featuring anonymous map-based station searches, connector lookups, authenticated driver profile management, station favorites, and user reviews.

    Dynamic Customization: A boot configuration API that lets admins update app themes, logos, and search defaults instantly over-the-air.

    Asynchronous Telemetry Ingestion: A high-throughput tracking pipeline that catches mobile interaction clickstreams, queues them via a message broker, and writes them to a dedicated analytics database.

    Partner Operator Tenant Portal (Web): A stateless React SPA allowing business partners to manage their stations, configure hardware connectors, and manually override charger availability statuses.

    Super Admin Workspace (Web): Global administrative views to manage corporate tenants, invite operators via secure email flows, and update application configuration profiles.

2.2 Explicit Out-of-Scope Exclusions

    ⚠️ MVP Constraints: To meet the 1-month delivery timeline, the following features are completely excluded from this phase of development:

        Live hardware integrations via OCPP (Open Charge Point Protocol).

        Real-time charging state or session tracking.

        User billing, payment processing gateways, and smart grid energy management.

        Live WebSocket connections (the system relies on explicit HTTP REST interfaces and poll requests).

3. High-Level Technical Architecture Spec

The project uses a reliable, decoupled on-premises architecture designed to handle traffic spikes smoothly.

[Mobile App / Web Admin] ──► [Nginx Edge Ingress] 
                                    │
                                    ▼
                          [Rust Actix-web API]
                                    │
             ┌──────────────────────┴──────────────────────┐
             ▼ (Pooled SQLx Core Engine)                   ▼ (AMQP Fast Publish)
  [PostgreSQL + PostGIS]                              [RabbitMQ Broker]
  (Operational Data Store)                                 │
                                                           ▼ (Async Worker Loop)
                                                      [MongoDB Node]
                                                     (Analytics Document Store)

    API Runtime Engine: Rust (Actix-web + SQLx) for memory safety and fast query processing.

    Storage Tiering: PostgreSQL with PostGIS for spatial queries, completely separated from MongoDB, which handles raw BSON clickstream documents.

    Broker Boundary: RabbitMQ acts as a safety buffer for telemetry traffic, isolating analytics writes from the driver discovery API paths.

    Perimeter Security: Nginx handles edge access control and rate-limiting, while Keycloak handles user identity verification and secures the administrative Web SPA using a server-side Backend-for-Frontend (BFF) cookie architecture.

4. Milestone Schedule & Timeline

Given the strict 1-month timeline, the project follows a fast-paced development plan:

[Week 1: Core Infra] ──► [Week 2: Backend & DB] ──► [Week 3: Frontend & Mobile] ──► [Week 4: QA & Launch]

📅 Milestone Breakdown

    Milestone 1 (End of Week 1): Core Infrastructure Validation

    Docker Compose files, Nginx reverse proxy routes, Keycloak authentication realms, and database instances fully up and running on the target host environment.

    Milestone 2 (End of Week 2): Core Backend API Completion

    Rust Actix-web services ready with compile-time verified SQLx spatial lookup queries, working RabbitMQ message publishers, and background data consumers writing to MongoDB.

    Milestone 3 (End of Week 3): Frontend Integration Delivery

    React Web Admin dashboards and the React Native Mobile Client layouts fully connected to the API endpoints.

    Milestone 4 (End of Week 4): Security Hardening, Testing, and Sign-Off

    Verification of edge rate-limits, database data persistence across reboots, and official launch of the MVP.

5. Risks, Assumptions, and Project Dependencies
5.1 Project Assumptions

    Single Host Deployment: The entire system will run within a single physical or virtual on-premises Linux host environment during this phase.

    Static Status Handling: Since there is no live OCPP hardware integration, station operators will manually maintain charger availability statuses using their web dashboard.

5.2 Key Risks & Mitigation Plans

    Risk: Scope Creep Over 30 Days. Adding "nice-to-have" features like real-time notifications or payment drafts could cause schedule delays.

        Mitigation: Strict adherence to this constitution. Any feature request involving automated hardware updates or payments will be deferred to Phase 2.

    Risk: Analytics Surges Affecting Driver Discovery. High volumes of tracking logs from mobile devices could overwhelm database connections.

        Mitigation: The asynchronous architecture is locked in. Core discovery queries run on PostgreSQL, while telemetry instantly hands off to RabbitMQ to decouple processing.

6. Authority and Governance Roles

    Lead Software Architect / Full Stack Engineer (Mohamed Ali Mezni): Holds absolute authority over codebase patterns, database schemas, framework selections, and infrastructural adjustments.

    Project Sponsor / Product Owner: Responsible for reviewing weekly milestone updates and validating that features align with business expectations before launch.