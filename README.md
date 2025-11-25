# Metro Ticketing System (Django Project Submission)

This project implements a fully functional, role-based ticketing system for a metro railway, featuring passenger wallets, ticket scanning, and administrative controls.

---

## 1. Project Setup and Dependencies

This guide assumes a system with Python 3 and Pip installed.

1.  **Create and Activate Virtual Environment:**
    

2.  **Install Dependencies:**
    

3.  **Run Migrations (Database Setup):**
   

4.  **Start the Server:**
    

---

## 2. Testing Credentials and Roles

All user roles required for testing have been pre-created and configured by the administrator.

| Role | Username | Password | Base URL for Testing |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `password123` | `http://127.0.0.1:8000/admin/` |
| **Scanner Staff** | `scanner` | `scanner123` | `http://127.0.0.1:8000/login/` |
| **Passenger** | `passenger` | `pass123` | `http://127.0.0.1:8000/login/` |

---

## 3. Core Functionality Walkthrough

### **A. Passenger Experience (Role: `passenger`)**

1.  **Log in** using `passenger`/`pass123`. The user is redirected to the home dashboard (`/`).
2.  **Wallet Management:**
    * Click **'My Wallet'** or navigate to `/tickets/wallet/`.
    * Click **'Add Funds to Wallet'** and add `100.00` to the account.
3.  **Ticket Purchase:**
    * Click **'Buy New Ticket'** or navigate to `/tickets/buy/`.
    * Select `Station A` as Start and `Station B` as End.
    * Click **'Purchase Ticket'** (Cost: ₹10.00). The balance is deducted, and a new ticket is created with **Status: Active**.
4.  **Ticket History:**
    * The user is redirected to the Ticket History (`/tickets/history/`). The newly purchased ticket will be visible along with its unique **Ticket ID** (a long hexadecimal string). **Copy this Ticket ID for Scanner testing.**

### **B. Scanner Experience (Role: `scanner`)**

1.  **Log in** using `scanner`/`scanner123`. The user is redirected to the home dashboard.
2.  **Access Scanner:** Click **'Scanner Interface'** or navigate to `/scanner/scan/`.
3.  **Entry Scan (Active -> In Use):**
    * Paste the **Ticket ID** copied from the passenger account.
    * Click **'Process Scan'**. The system will report "Entry Granted" and update the ticket status to **'In Use'**.
4.  **Exit Scan (In Use -> Used):**
    * Paste the **SAME Ticket ID**.
    * Click **'Process Scan'**. The system will report "Exit Recorded" and update the ticket status to **'Used'**.
5.  **Offline Purchase:**
    * Click **'Go to Offline Cash Purchase'** or navigate to `/scanner/offline_purchase/`.
    * Select `Station A` to `Station B` and click **'Issue Cash Ticket'**. A ticket is created and immediately marked as **USED**.

---

## 4. Administrative Control (Role: `admin`)

Log into the Admin Panel (`/admin/`) with `admin`/`password123`.

* **METROLINE:** Stations (`Station A`, `Station B`) and Lines (`Blue Line`) are configurable here.
* **TICKETS:** All generated tickets and user wallets can be reviewed and managed.
* **AUTHENTICATION:** Users (`scanner`, `passenger`) and Groups (`Scanners`, `Passengers`) are verified here.