# Requirement Prioritization (MoSCoW Framework)
## Library Management System using Scrum Agile Methodology

---

## 1. The MoSCoW Prioritization Framework

In Scrum and Agile software delivery, **MoSCoW Prioritization** is an established methodology for categorizing project requirements based on criticality to ensure that essential business value is delivered within constrained iteration timeboxes.

```text
+-----------------------------------------------------------------------------------------+
|                              MoSCoW REQUIREMENT PYRAMID                                 |
+-----------------------------------------------------------------------------------------+
|  🔴 MUST HAVE   : Non-negotiable core functionality (Authentication, Issue, Return)     |
|  🟠 SHOULD HAVE : Critical enhancements with acceptable workarounds (History, Renew)    |
|  🟢 COULD HAVE  : Nice-to-have capabilities (Admin Metrics, Aesthetic Themes)          |
|  ⚪ WON'T HAVE  : Deferred to post-academic iterations (Payment Gateways, RFID Sensors) |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Requirement Classification & Point Distribution

| MoSCoW Category | Story Points | Percentage | Core Deliverables Included | Rationale |
|---|---|---|---|---|
| 🔴 **Must Have** | 35 pts | 68.6% | `US-01`, `US-02`, `US-03`, `US-04`, `US-05`, `US-06`, `US-08`, `US-10`, `US-12` | Without secure authentication, catalog search, atomic book issues, and returns, the system cannot function as an academic library. |
| 🟠 **Should Have** | 8 pts | 15.7% | `US-07`, `US-09` | Loan history and self-service renewals significantly enhance member experience, though manual librarian queries could serve as a temporary fallback. |
| 🟢 **Could Have** | 3 pts | 5.9% | `US-11` | Aggregated executive administrative dashboards and audit logs provide operational visibility but do not halt circulation. |
| ⚪ **Won't Have** | 0 pts (Deferred) | 0.0% | Online Stripe/Razorpay payment gateway, physical RFID antenna readers, automated SMS gateway. | Out of scope for academic single-node PBL demonstration; deferred to future iterations. |

**Total Estimated Backlog:** 51 Story Points (Delivered across Sprints 1 to 5).

---

## 3. Story-by-Story Prioritization Matrix

| Story ID | Story Title | MoSCoW Status | Story Points | Sprint | Priority Badge |
|---|---|---|---|---|---|
| `US-01` | Member Registration & Credential Hashing | Must Have | 3 | Sprint 1 | 🔴 High |
| `US-02` | Role-Based Authentication & Session Management | Must Have | 3 | Sprint 1 | 🔴 High |
| `US-03` | Book Catalog Management & Shelf Tracking | Must Have | 5 | Sprint 2 | 🔴 High |
| `US-04` | Advanced Book Search & Category Filtering | Must Have | 3 | Sprint 2 | 🔴 High |
| `US-05` | Real-time Book Availability & Copy Inspection | Must Have | 3 | Sprint 2 | 🔴 High |
| `US-06` | Atomic Book Issue & Concurrency Control | Must Have | 8 | Sprint 3 | 🔴 High |
| `US-07` | Member Loan History & Due Date Overview | Should Have | 3 | Sprint 3 | 🟠 Medium |
| `US-08` | Book Return & Automated Inventory Recovery | Must Have | 5 | Sprint 3 | 🔴 High |
| `US-09` | Self-Service Book Renewal & Reservation Queue | Should Have | 5 | Sprint 4 | 🟠 Medium |
| `US-10` | Automated Overdue Fine Calculation & Settlement | Must Have | 5 | Sprint 4 | 🔴 High |
| `US-11` | Centralized Librarian & Admin Inventory Audit | Could Have | 3 | Sprint 5 | 🟢 Low |
| `US-12` | Built-in Scrum Backlog, Sprint & Terminal Kanban Engine | Must Have | 8 | Sprint 5 | 🔴 High |

---

## 4. Priority Traceability across Artifacts

Priorities remain strictly harmonized across all project artifacts:
1. **Product Backlog:** Ordered strictly with Must Have items in Sprints 1–3, followed by Should Have and Could Have items in Sprints 4–5.
2. **Kanban Board:** Color-coded badges (Red = High, Amber = Medium, Green = Low).
3. **GitHub Issues:** Labeled with corresponding labels (`priority: high`, `priority: medium`, `priority: low`).
4. **Automated Test Suite:** Every Must Have user story has dedicated unit and integration tests with zero skipped assertions.
