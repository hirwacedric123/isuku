# Pre-Implementation Analysis and Conclusions

Source analyzed: `Research Methodoloy.pdf`  
Implementation stack to be used: `Django + HTML + CSS + Bootstrap`

## 1) Problem and Scope Analysis

### 1.1 Core Problem (Locked)
Kigali's current waste collection workflow is mostly static and manual, causing:
- fuel/time waste from fixed routes that visit low-need areas,
- missed or delayed collections in high-density zones,
- weak communication between residents and contractors,
- limited analytics for City/REMA strategic decision-making.

### 1.2 Project Objective (Locked)
Build a web platform that enables:
- real-time schedule visibility for citizens,
- geo-tagged waste reporting,
- contractor operational response and routing support,
- administrative oversight with exportable performance data.

### 1.3 Actors and Operating Boundary (Locked)
- **Citizen**: consume schedules, submit incidents, track resolution.
- **Contractor/Logistics Manager**: view incidents map, generate routes, resolve reports.
- **Municipal Admin**: manage master data, monitor KPIs, export reports.

Pilot geography remains limited to:
- Remera,
- Kimisagara,
- Kinyinya.

### 1.4 Scope Matrix
- **In Scope (MVP)**
  - Role-based authentication and authorization
  - Sector/cell-based schedule display
  - Geo-tagged report submission with optional image
  - Contractor incident map and route suggestion
  - Status lifecycle: Pending -> In Progress -> Resolved
  - Notifications for updates/delays
  - Admin metrics and CSV export

- **Out of Scope (MVP)**
  - Physical IoT bin sensors
  - Computer vision / AI waste classification
  - Native mobile apps (web only)
  - Full enterprise ERP integration

### Phase 1 Conclusion
The MVP scope is feasible and should be strictly limited to software-only, browser-based workflows to avoid timeline risk and feature creep.

---

## 2) Requirement Baseline (Django-Ready)

### 2.1 Functional Requirements -> Implementable Features

#### Citizen Features
- Register/login/logout and profile with location (district/sector/cell).
- View upcoming collection schedule for assigned area.
- Submit waste incident:
  - required: title/type, GPS coordinates, description,
  - optional: photo upload.
- Track report status and receive update notifications.

#### Contractor Features
- Secure contractor login and role-restricted dashboard.
- View open reports on map and list with filters.
- Generate recommended route from open incidents.
- Assign route to vehicle/driver and update completion state.
- Mark incidents resolved with timestamp and optional note/photo.

#### Admin Features
- Manage master data (locations, schedules, contractors, vehicles).
- View operational KPIs by sector and timeframe.
- Export operational datasets (CSV first, PDF optional).

### 2.2 Non-Functional Requirements -> Acceptance Criteria

- **Security**
  - Django auth with hashed passwords.
  - CSRF enabled for forms; role guards on all protected views.
  - Input validation for report payloads and uploads.
  - Baseline OWASP checks (XSS/SQLi prevention by framework defaults + safe coding).

- **Performance**
  - Main pages render within acceptable mobile network thresholds.
  - Report submission should complete quickly under normal load.
  - Route suggestion should return within practical dispatcher tolerance for MVP.

- **Usability**
  - Mobile-first Bootstrap layouts for all actor dashboards.
  - Clear status labels and minimal click depth for key actions.

- **Localization**
  - English-first implementation with i18n structure ready for Kinyarwanda.

- **Scalability**
  - PostgreSQL-backed design with index-ready data model and caching opportunities.

### 2.3 Stack Alignment Conclusion
The document references React/Node in design examples, but required behavior can be preserved in Django using:
- Django templates + Bootstrap for UI,
- Django views/services for business logic,
- PostgreSQL data layer,
- optional JS where needed (geolocation/maps interactivity).

### Phase 2 Conclusion
All required behavior is fully representable in Django without architectural compromise.

---

## 3) System and Data Analysis (Architecture Freeze)

## 3.1 Django App Boundaries (Frozen for MVP)
- `accounts`: users, roles, authentication, permissions.
- `locations`: district/sector/cell reference data.
- `schedules`: collection schedules and exceptions.
- `reports`: citizen incident reporting and lifecycle.
- `routing`: route generation, assignments, stop ordering.
- `notifications`: in-app/email/SMS dispatch logs.
- `analytics`: KPI aggregation and exports.

### 3.2 Conceptual Data Model (Frozen for MVP)
- **User**
  - id, names, phone/email, password_hash, role, location_fk, is_active, created_at
- **Location hierarchy**
  - district -> sector -> cell
- **CollectionSchedule**
  - id, location_fk, weekday, time_window, collector_fk, active
- **WasteReport**
  - id, citizen_fk, location_fk, lat, lng, category, description, photo, status, timestamps
- **Vehicle**
  - id, contractor_fk, plate_number, capacity, active
- **RoutePlan**
  - id, contractor_fk, vehicle_fk, date, status, estimated_distance, created_by
- **RouteStop**
  - id, route_fk, report_fk, sequence, eta
- **NotificationLog**
  - id, user_fk, channel, message, delivery_status, sent_at

### 3.3 Data Flow (Frozen for MVP)
1. Citizen submits report with geolocation.
2. Report stored as open incident and appears in contractor queue/map.
3. Contractor generates route and dispatches vehicle.
4. Contractor updates stops/reports as resolved.
5. User receives resolution update.
6. Admin dashboards consume historical and real-time metrics.

### 3.4 GIS Strategy Decision
- **Primary choice**: PostgreSQL + PostGIS.
- **Fallback**: PostgreSQL with decimal `lat/lng` and app-level distance calculations.

Decision rule:
- If hosting supports PostGIS smoothly in setup window, use it.
- Otherwise start with `lat/lng` fallback and keep model migration path to PostGIS.

### Phase 3 Conclusion
Architecture and data boundaries are stable enough to begin implementation once risk gates are accepted.

---

## 4) Feasibility and Risk Gate

### 4.1 Feasibility Summary
- **Technical**: feasible with Django ecosystem and mapped requirements.
- **Operational**: aligned with city/contractor/citizen interaction model.
- **Economic (academic context)**: feasible if paid APIs are minimized and open-source map tooling is preferred.
- **Schedule**: feasible only if MVP is protected from scope expansion.

### 4.2 Risk Register and Mitigation
- **Connectivity variability**
  - Mitigation: lightweight pages, compressed images, retries and clear offline/error states.
- **Map API cost/rate limits**
  - Mitigation: start with OpenStreetMap/Leaflet; isolate provider adapters.
- **Low-quality/false citizen reports**
  - Mitigation: required geotag, category validation, report moderation flags, reputation checks later.
- **Notification failures**
  - Mitigation: queue + retry + delivery log; keep in-app notifications as baseline fallback.
- **Route complexity beyond MVP**
  - Mitigation: start with nearest-neighbor heuristic and track future optimization backlog.
- **Timeline pressure**
  - Mitigation: freeze MVP; defer non-critical features.

### 4.3 Definition of Ready (Go/No-Go Checklist)
Implementation should start only if all are true:
- Scope matrix approved.
- Requirement baseline approved by team.
- Data model and app boundaries approved.
- GIS path selected (primary/fallback).
- Test scenarios drafted for all 3 actor roles.
- Environments prepared (dev DB, media storage strategy, secrets handling).

### Phase 4 Conclusion
Project is **Go** for MVP implementation if readiness checklist is satisfied before coding sprint starts.

---

## 5) Implementation Readiness Roadmap (Phased)

### Sprint 0: Setup and Foundations
- Project bootstrap, app scaffolding, environment configs.
- User model with roles and permission policy.
- Location master data and admin setup.

### Sprint 1: Citizen Core
- Schedule viewing by location.
- Incident submission with geolocation and optional image.
- Citizen report tracking page.

### Sprint 2: Contractor Operations
- Open incidents list/map.
- Route suggestion and route assignment.
- Resolve workflow and completion updates.

### Sprint 3: Admin and Reporting
- KPI dashboard (response times, resolution rates, volumes).
- CSV export and sector-level breakdowns.
- Data quality checks.

### Sprint 4: Hardening and UAT
- Security pass, performance tuning, UX fixes.
- Pilot UAT in target sectors.
- Final release candidate and handover docs.

## Testing Strategy (Predefined)
- **Unit tests**: models, validators, route service, permission checks.
- **Integration tests**: report-to-resolution flow and notification flow.
- **UAT scripts**:
  - Citizen submits report and tracks closure.
  - Contractor generates and executes route.
  - Admin exports period report.

## Success Metrics (Initial)
- Median report response time.
- Resolution rate within defined time window.
- Schedule adherence by sector.
- Number of citizen reports submitted and closed.

## Final Conclusion
The analysis confirms the project should proceed as a software-only Django MVP with strict phase control. The strongest delivery strategy is to lock scope early, implement role-based workflows first, keep GIS/routing practical, and use measurable service KPIs to prove impact during pilot rollout.
