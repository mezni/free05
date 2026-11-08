# EXPERIENCE — bss-core

**Purpose**: User flows, interaction patterns, states, accessibility, and journey specifications for the support application.

**Related Documents**:
- `PRD.md` — Product requirements and functional specifications
- `DESIGN.md` — Visual design tokens and UI styling
- `ARCHITECTURE-SPINE.md` — Technical constraints and paradigm (hexagonal/ports-and-adapters)
- `epics.md` — Epic and story breakdown for implementation
- `sprint-status.yaml` — Sprint planning and status tracking

**Last Updated**: 2026-11-08
**Status**: Draft

---
## User Personas

> The CSR is the primary operator. Customer-facing flows (browsing, tracking, viewing billing) may be self-service or assisted by a CSR; Journey 2 shows the customer-facing view of the same order lifecycle.

### Persona 1: Customer Service Representative (CSR)

**Description**: Front-line staff who manage customer accounts, process orders, handle returns, and track shipments.

**Goals**:
- Onboard new customers quickly and accurately
- Process orders without errors
- Handle returns and refunds efficiently
- Track shipments and provide delivery updates to customers
- Generate billing records and view payment history

**Pain Points**:
- Slow navigation between related records
- Unclear return eligibility criteria
- Difficulty finding customer history
- Complex billing reconciliation
- Too many steps for simple tasks

**Key Metrics**:
- Average time to onboard a customer: < 2 minutes
- Order processing error rate: < 2%
- Return processing time: < 15 minutes
- Shipment tracking accuracy: 100%

**Mental Model**:
- "I need to find the customer, then do something with their order"
- "I should be able to see the full journey from order to delivery"
- "I need clear signals when something goes wrong"

---
### Persona 2: Customer (End User)

**Description**: Individuals or businesses who purchase products through the support application.

**Goals**:
- Place orders easily and quickly
- Track shipments in real-time
- View billing history and payment details (masked for privacy)
- Initiate returns when needed
- Get clear information about delivery dates

**Pain Points**:
- Confusing order placement flow
- Unclear tracking information
- Surprise delivery dates
- Difficulty understanding return policy
- Billing statements without masked payment details

**Key Metrics**:
- Order placement time: < 3 minutes
- Tracking information clarity: 95% positive feedback
- Delivery date accuracy: 98%+
- Return initiation success: 85%+

**Mental Model**:
- "I ordered something, now I want to know where it is"
- "I need to see what I've bought before, so I don't order duplicates"
- "The price I see should be what I pay (no hidden fees)"
- "If I need to return something, the process should be straightforward"

---
### Persona 3: System Administrator

**Description**: Internal staff who manage user accounts, roles, and system configuration.

**Goals**:
- Create and manage user accounts with appropriate permissions
- Assign roles (Viewer, Operator, Manager, Administrator, User Manager)
- Audit user actions for compliance
- Monitor system health and usage *(post-MVP; no FR yet)*
- Configure system settings and preferences *(post-MVP; no FR yet)*

**Pain Points**:
- Complex role assignment without clear guidance
- Unclear permission boundaries
- Audit trail not visible or searchable
- System configuration scattered across interfaces
- User onboarding takes too long

**Key Metrics**:
- User onboarding time: < 5 minutes
- Role assignment clarity: 90%+ understand permissions
- Audit log completeness: 100% of CRUD operations
- System uptime: 99.9%+

**Mental Model**:
- "I need to control who can do what in the system"
- "Every action should be traceable to a user"
- "The interface should make permission boundaries clear"
- "Configuration should be centralized and discoverable"

---
## User Flows

### Flow 1: Customer Onboarding

**Step 1**: CSR navigates to "Customers" section
- **Trigger**: Application load or "Add Customer" CTA
- **Action**: Click "Add New Customer" button
- **Decision**: Is user authenticated with sufficient permissions?
  - Yes → Proceed to Step 2
  - No → Show authentication required modal, redirect to login

**Step 2**: Fill customer form
- **Fields**: Name, email, tier assignment (Standard/Gold/Enterprise), preferences
- **Validation**: 
  - Email format validation
  - Unique email constraint check
  - Tier must be one of: Standard, Gold, Enterprise
- **Action**: Click "Create Customer" button

**Step 3**: Confirmation
- **Success**: Show toast "Customer created successfully: CUST-001"
- **Redirect**: Navigate to customer detail page
- **Error**: Show inline validation errors, prevent form submission

**Step 4**: Customer listed
- **Display**: Customer appears in customers list with ID, name, tier
- **Next**: CSR can now search, filter, or view billing history for this customer

**Alternative Paths**:
- **Escape**: Click "Cancel" → Return to customers list without saving
- **Validation Failure**: Show error banner, keep form open with highlighted fields

---
### Flow 2: Order Creation

**Step 1**: CSR navigates to "Orders" section or customer detail page
- **Trigger**: "Create Order" from customer profile or main navigation
- **Action**: Click "Create Order" button

**Step 2**: Select products and quantities
- **Interface**: Product catalog with search, filters, category navigation
- **Fields**: Product ID/name, quantity (≥ 1), price display
- **Validation**:
  - Product must exist in catalog
  - Quantity must be ≥ 1 (per-line cap configurable if enabled)
  - Price must be positive
- **Action**: Select items, click "Add to Order"

**Step 3**: Review order summary
- **Display**: Itemized list, unit prices, quantities, line totals, order total
- **Editable**: Quantities can be adjusted, items can be removed
- **Action**: Click "Place Order" or "Remove Item"

**Step 3b**: Alternative — Remove items
- **Action**: Click "Remove" on any item line
- **Confirmation**: "Remove this item from order?" modal
- **Result**: Item removed, order total recalculated

**Step 4**: Place order
- **Action**: Click "Place Order" button
- **Confirmation**: "Order ORD-0001 created successfully. Status: Processing."
- **Redirect**: Navigate to order detail page, status: Processing

**Error Paths**:
- **Insufficient inventory**: Show error "Product temporarily unavailable", offer alternative
- **Validation failure**: Show inline errors, prevent placement
- **Authentication required**: Redirect to login if session expired

---
### Flow 3: Return Processing

**Step 1**: CSR navigates to order detail page
- **Trigger**: From orders list, select order to view details
- **Action**: Click order ID or "View" button

**Step 2**: Check return eligibility
- **Interface**: Return eligibility checker
- **Fields**: Item ID, purchase date, current date
- **Validation**: 
  - Purchase date within return window (30 days, configurable policy)
  - Item status: not used, in original packaging
  - Order status: not already cancelled/returned
- **Action**: Click "Check Eligibility"

**Step 3**: Eligibility result
- **Eligible**: Show "Item is eligible for return. Would you like to initiate?"
- **Not eligible**: Show reason "Purchase outside return window" / "Item used/damaged" / "Order cancelled"
- **Action**: Click "Initiate Return" or "Close"

**Step 4**: Initiate return
- **Fields**: Reason for return (dropdown: defective, wrong item, changed mind, etc.), quantity
- **Action**: Click "Submit Return Request"

**Step 5**: Return confirmation
- **Success**: Show "Return request submitted. RMA-001 generated. Shipping label is ready."
- **Generate**: Shipping label (available for download/print); email delivery activates once the notification service is enabled (deferred)
- **Error**: Show error, prevent submission, keep form open

**Step 6**: Return status tracking
- **Display**: Return request status (submitted, approved, rejected, completed)
- **Actions**: View RMA details, regenerate shipping label, update status
- **Timeline**: Typical 5-7 business days for processing

---
### Flow 4: Shipment Tracking

**Step 1**: Customer or CSR navigates to shipment tracking
- **Trigger**: From order detail page, "Track Shipment" button
- **Action**: Click "Track Shipment" or enter tracking number

**Step 2**: Input tracking information
- **Options**: 
  - Enter tracking number manually
  - Select from recent shipments for this order
  - Auto-detect from carrier
- **Fields**: Tracking number, carrier selection (FedEx, UPS, DHL)

**Step 3**: Retrieve tracking data
- **Action**: System fetches real-time status from carrier API
- **Loading**: Show spinner, "Fetching tracking information..."
- **Result**: Display tracking details or error message

**Step 4**: Display tracking information
- **Status indicators**: In Transit, Out for Delivery, Delivered
- **Location**: Current city/state, last update timestamp
- **Estimated delivery**: Date with +/- business days
- **Carrier**: Name and logo
- **History**: Timeline of status changes

**Error Paths**:
- **Invalid tracking**: Show error "Tracking number not found. Please verify and try again."
- **Carrier unavailable**: Show warning "Carrier API temporarily unavailable. Showing last known status."
- **No shipments**: Show "This order has not been shipped yet. Status: Processing."

---
### Flow 5: Billing and Payments

**Step 1**: CSR or customer navigates to billing section
- **Trigger**: From main navigation or order detail page
- **Action**: Click "Billing" or "Payment History"

**Step 2**: View billing records
- **Display**: List of transactions with:
  - Date
  - Type (Charge, Refund, Credit)
  - Amount (masked: "Visa ending in 4242")
  - Order reference
  - Status

**Step 3**: Filter and search
- **Fields**: Date range, transaction type, customer ID, order ID
- **Action**: Apply filters, refresh list

**Step 4**: Execute monetary credit
- **Trigger**: "Issue Refund" or "Add Credit" from billing record
- **Fields**: Amount, credit destination (balance or payment method)
- **Validation**: 
  - User has Financial Write scope
  - Amount > 0
  - Credit destination valid
  - Audit logging enabled
- **Action**: Click "Execute Credit"

**Step 5**: Credit confirmation
- **Success**: Show "Credit of $X.XX executed. Updated balance: $X.XX. Audit log entry created."
- **Error**: Show error, prevent execution, log failed attempt

**Step 6**: Audit trail
- **Display**: Audit entries for billing operations
- **Fields**: Timestamp, user ID, operation type, amount, outcome
- **Search**: Filter by date, user, operation type

---
### Flow 6: User Management (Admin)

**Step 1**: Admin navigates to "User Management" section
- **Trigger**: Main navigation, "Users" or "Admin" section
- **Authentication**: Requires `User Management` scope or `Administrator` role
- **Action**: Click "Users" section header

**Step 2**: View user list
- **Display**: Table of users with:
  - Name, email, role, status (active/inactive)
  - Last login, date created
  - Actions: Edit, Toggle Status, Delete

**Step 2b**: Search and filter
- **Fields**: Name, email, role, status toggle
- **Action**: Apply filters, refresh list

**Step 3**: Create new user
- **Action**: Click "Add User" button
- **Fields**: Name, email, role assignment (Viewer/Operator/Manager/Administrator/User Manager)
- **Validation**: Role must be one of the valid roles
- **Action**: Click "Create User"

**Step 4**: User created
- **Success**: Show toast "User created: john.doe@example.com with role: Operator"
- **Redirect**: Navigate to user detail page
- **Error**: Show validation errors, prevent creation

**Step 5**: Edit user
- **Action**: Click "Edit" on user row
- **Fields**: Same as create, modifiable
- **Action**: Click "Update User"

**Step 6**: Toggle status
- **Action**: Click "Toggle Status" button
- **Confirmation**: "Are you sure you want to deactivate this user?"
- **Result**: Status changes, audit log entry created

**Step 7**: Delete user
- **Action**: Click "Delete" on user row
- **Confirmation**: "Are you sure you want to delete this user? This action cannot be undone."
- **Result**: User removed, audit log entry created, or error if system prevents deletion

---
## Interaction Patterns

### Loading States

| Component | Spinner | Text | Duration | Action |
|-----------|---------|------|----------|--------|
| **Button click** | Spinner inside button | "Processing..." | Until response | Disable button, prevent double-click |
| **Form submission** | Full-screen spinner | "Saving..." | Until response | Show success/error toast |
| **API call** | Small spinner near element | "Loading..." | < 2 seconds | Show skeleton state |
| **Data table load** | Row hover spinner | "Loading data..." | < 3 seconds | Show empty state if no data |
| **Modal open** | Spinner in header | "Loading..." | Until data received | Show placeholder content |

### Error States

| Component | Icon | Title | Message | Action |
|-----------|------|-------|---------|--------|
| **404 Page** | `close` or `info` | "Page Not Found" | "The requested page does not exist." | "Go Home" |
| **403 Page** | `alert` | "Access Denied" | "You do not have permission to view this page." | "Return to Dashboard" |
| **Validation Error** | `alert` | "Validation Error" | "Please fix the errors below." | "Close" + inline field errors |
| **API Error** | `alert` | "Error" | "Something went wrong. Please try again." | "Retry" + error details expander |
| **Network Offline** | `wifi-off` | "No Internet" | "You appear to be offline." | "Retry" | 

### Success States

| Component | Icon | Title | Message | Action |
|-----------|------|-------|---------|--------|
| **Toast** | `check` | "Success" | "Action completed successfully." | "Dismiss" (auto-hide after 4s) |
| **Modal** | `check` | "Success" | "Your changes have been saved." | "Close" + "Continue editing" |
| **Page** | `check` | "Success" | "Your changes have been saved successfully." | "Go to Overview" | 

### Empty States

| Component | Illustration | Title | Description | Action |
|-----------|-------------|-------|-------------|--------|
| **No customers** | Illustrated empty state | "No customers yet" | "Click 'Add Customer' to get started." | "Add Customer" CTA |
| **No orders** | Illustrated empty state | "No orders yet" | "Create your first order to get started." | "Create Order" CTA |
| **No shipments** | Illustrated empty state | "No shipments yet" | "An order will generate a shipment when fulfilled." | "View Order" CTA |
| **No billing** | Illustrated empty state | "No billing records yet" | "Transactions will appear here as they are processed." | "Learn More" CTA |
| **No users** | Illustrated empty state | "No users yet" | "Add users to get started with administration." | "Add User" CTA |

### Breadcrumbs

| Component | Structure | Usage |
|-----------|-----------|-------|
| **Primary** | `Home > Section > Page` | Standard navigation context |
| **Secondary** | `Home > Section > Page > Sub-page` | Deep navigation context |
| **Tertiary** | `Home > Section > Page > Sub-page > Item` | Specific item context (e.g., order details) |

**Breadcrumb Styles**:
- Separator: `>` or chevron
- Active page: not clickable, highlighted
- Hover: underline, not clickable
- Mobile: collapse to "Back" button

### Notification Toasts

| Type | Timeout | Action | Auto-dismiss |
|------|---------|--------|------------|
| **Success** | 4 seconds | "Dismiss" button | Yes |
| **Error** | 6 seconds | "Dismiss" + "Report" link | Yes |
| **Warning** | 5 seconds | "Dismiss" + "Learn More" | Yes |
| **Info** | 5 seconds | "Dismiss" | Yes |
| **Persistent** | Never auto-dismiss | "Pin" icon, "Dismiss" | No |

**Toast Position**: `top-right` of viewport, slides in from top
**Maximum Stack**: 3 toasts visible at once
**Accessibility**: 
- ARIA role="alert" for important notifications
- Keyboard navigable (Tab to cycle, Esc to dismiss)
- Color-independent messaging (also include text)

---
## Accessibility

### Color Contrast

| Contrast Level | Minimum Ratio | Target Elements |
|----------------|---------------|-----------------|
| **AA normal text** | 4.5:1 | Body text < 18pt, non-text content |
| **AA large text** | 3:1 | Body text ≥ 18pt, heading text ≥ 14pt bold |
| **UI components** | 3:1 | Borders, inputs, icons, disabled states |
| **Error text** | 4.5:1 | Danger text against neutral backgrounds |
| **Graphical content** | 3:1 | Charts, icons, decorative elements |

**Tools for Verification**:
- Stark (Figma plugin)
- axe DevTools
- Lighthouse
- WAVE
- Manual testing with screen readers (NVDA, VoiceOver)

### Keyboard Navigation

| Key | Function | Context |
|-----|----------|---------|
| **Tab** | Move focus to next interactive element | All pages |
| **Shift + Tab** | Move focus to previous interactive element | All pages |
| **Enter** | Activate focused element (button, link, checkbox) | All pages |
| **Space** | Toggle checkbox/radio, activate button | Form elements |
| **Escape** | Close modals, dismiss toasts, exit fullscreen | Overlays, modals, toasts |
| **Arrow keys** | Navigate data tables, carousel items | Data tables, carousels |
| **Ctrl + F** | Focus search field | Pages with search |
| **Ctrl + P** | Print page | Print-capable pages |

### Screen Reader Support

| Feature | Implementation |
|---------|---------------|
| **ARIA labels** | All buttons, inputs, has clear labels |
| **Landmarks** | `header`, `nav`, `main`, `section`, `footer` | 
| **Live regions** | Toasts and errors use `role="alert"` |
| **Focus management** | Modal trap, focus return on close |
| **Heading hierarchy** | H1 on page title, H2 on section headers, H3 on sub-sections |
| **Language attribute** | `lang` attribute on `<html>` element |
| **Contrast ratios** | All colors verified per WCAG AA |

### Focus Management

| Scenario | Behavior |
|----------|----------|
| **Modal open** | Focus trapped within modal, focus returns to opener on close |
| **Toast appear** | Focus remains where it was, toast announced by screen reader |
| **Form error** | Focus moved to first error field, error announced |
| **Navigation change** | Focus moves to new page header, announcement |
| **Error state** | Focus remains, error announced live region |

---
## User Journey Maps

### Journey 1: New Customer Onboarding (CSR Perspective)

**Actors**: Customer Service Representative

**Phase 1: Discovery** (5-10 minutes)
- CSR logs into the application
- Navigates to "Customers" section
- Clicks "Add New Customer"
- Fills out customer form

**Phase 2: Onboarding** (2-3 minutes)
- Form validation runs
- Customer created successfully
- Toast confirmation shown
- CSR reviews customer detail

**Phase 3: Exploration** (3-5 minutes)
- CSR searches for the new customer
- Filters by tier
- Views billing history (empty state)
- Navigates to orders section

**Phase 4: Handoff** (2-3 minutes)
- CSR continues to next task
- May assist customer with account questions
- Logs out or moves to next customer

**Success Criteria**:
- Customer created in < 3 minutes
- No validation errors
- CSR can find customer by name/email/tier

**Failure Points**:
- Invalid email format
- Duplicate email
- Insufficient permissions
- Form timeout

---
### Journey 2: Order Placement (Customer Perspective)

**Actors**: End Customer

**Phase 1: Browsing** (5-10 minutes)
- Customer logs into the application
- Browses product catalog
- Selects products and quantities
- Adds items to order

**Phase 2: Checkout** (3-5 minutes)
- Reviews order summary
- Adjusts quantities if needed
- Clicks "Place Order"

**Phase 3: Confirmation** (1-2 minutes)
- Order created successfully
- Order ID displayed
- Status: Processing
- Email confirmation sent (if configured)

**Phase 4: Tracking** (Ongoing)
- Customer receives order confirmation
- Can track shipment via tracking number
- Receives delivery date updates
- Contact support if issues arise

**Success Criteria**:
- Order placed in < 5 minutes
- Order total calculated correctly
- Customer receives confirmation
- Order status visible in account

**Failure Points**:
- Invalid product selection
- Insufficient quantity
- Payment processing error
- Network timeout

---
### Journey 3: Return Initiation (CSR Perspective)

**Actors**: Customer Service Representative

**Phase 1: Identification** (2-3 minutes)
- CSR finds order in orders list
- Opens order detail page
- Checks return eligibility

**Phase 2: Evaluation** (2-3 minutes)
- Reviews return policy
- Considers item condition
- Verifies purchase date within window

**Phase 3: Submission** (2-3 minutes)
- Selects reason for return
- Provides quantity
- Submits return request
- Receives RMA confirmation

**Phase 4: Follow-up** (Ongoing)
- Tracks return status
- Communicates with customer
- Processes refund or rejection

**Success Criteria**:
- Return eligibility determined in < 5 minutes
- Return request submitted without errors
- RMA number generated
- Customer notified of status

**Failure Points**:
- Purchase outside return window
- Item condition doesn't qualify
- Missing order information
- System error during submission

---
## Design Principles

### 1. Empathy First
Every design decision serves a genuine user need. We start simple and evolve through feedback. The interface should make users feel understood, not lost.

### 2. Data-Informed, Not Data-Driven
Metrics inform our decisions, but creativity and human understanding drive design. Numbers tell us what's happening; design tells us why.

### 3. Start Simple, Evolve Through Feedback
The first version of any feature should be usable but minimal. We add complexity only when users need it and request it.

### 4. Consistency Across Contexts
The same patterns, colors, and interactions apply across all five contexts (Customer, Order, Shipment, Billing, User Management). This reduces cognitive load and increases learnability.

### 5. Accessibility by Default
No feature is considered complete without accessibility compliance. Contrast, keyboard navigation, and screen reader support are built in, not bolted on.

### 6. Error Prevention Over Error Recovery
Better to prevent errors than to explain them. Clear validation, confirmation modals, and disabled unavailable options reduce the chance of mistakes.

### 7. Transparent Operations
Every action should be traceable. Audit logs, status indicators, and clear error messages build trust and enable users to understand what's happening.

### 8. Performance Matters
Page load < 3 seconds, API responses < 200ms (p95), smooth interactions at 60fps. Performance is a feature, not an afterthought.

### 9. Mobile-First, Responsive
Design works on mobile devices first, then scales up to desktop. Touch targets minimum 44px, responsive breakpoints at 48rem (768px).

### 10. Speed of Implementation
Design tokens and components are implementation-ready for the FastAPI/Streamlit stack. No speculative design that can't be built in the sprint.

---
## Design-to-Development Handoff Checklist

### Visual Design
- **COLOR**: All color tokens defined, contrast verified, dark mode supported
- **FILE**: DESIGN.md reviewed and approved
- **TOKENS**: CSS custom properties extracted and committed

### Interaction Design
- **FILE**: EXPERIENCE.md reviewed and approved
- **PATTERNS**: All user flows documented and approved
- **PATTERNS**: Interaction states (loading, error, success, empty) designed

### Accessibility
- **FILE**: EXPERIENCE.md accessibility section reviewed
- **CONTRAST**: All color ratios meet WCAG AA
- **KEYBOARD**: All interactive elements keyboard navigable
- **SCREEN READER**: ARIA labels, live regions, heading hierarchy verified

### Content
- **FILE**: All copy reviewed and approved
- **TONALITY**: Consistent voice and tone across all touchpoints
- **TRANSLATION**: i18n keys identified for multi-language support

### Technical
- **FILE**: DESIGN.md and EXPERIENCE.md committed to repository
- **FASTAPI**: Streamlit integration points identified
- **CSS**: Custom properties defined, no inline styles
- **RESPONSIVE**: Breakpoints tested at mobile, tablet, desktop

### Handoff Complete When:
- [ ] DESIGN.md and EXPERIENCE.md are both final status
- [ ] All color tokens have contrast ratios verified
- [ ] All user flows have acceptance criteria
- [ ] Accessibility requirements are met
- [ ] Development team has reviewed and approved
- [ ] i18n keys identified (if multi-language support planned)
- [ ] Repository contains DESIGN.md, EXPERIENCE.md, and component library

---
## Revision History

| Date | Author | Change | Status |
|------|--------|--------|--------|
| 2026-11-08 | Sally (UX Designer) | Initial design draft | Draft |
| 2026-11-08 | Review pass | Fixed WCAG AA ratios, principle numbering, Flow 4 step numbering, carrier list (USPS removed), quantity rule, return-window/notification wording, persona scope | Draft |

---
*Document Version: 1.0*
*Last Updated: 2026-11-08*
*Status: Draft*
*Designer: Sally — UX Designer*
*Grounded in Don Norman's human-centered design and Alan Cooper's persona discipline.*
