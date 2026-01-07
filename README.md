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
    * Click **'My Wallet'** 
    * Click **'Add Funds to Wallet'** 
3.  **Ticket Purchase:**
    * Click **'Buy New Ticket'** 
    * Select `Station A` as Start and `Station B` as End.
    * Click **'Purchase Ticket'** (Cost: ₹10.00). The balance is deducted, and a new ticket is created with **Status: Active**.
4.  **Ticket History:**
    * The user is redirected to the Ticket History. The newly purchased ticket will be visible along with its unique **Ticket ID**. **Copy this Ticket ID for Scanner testing.**

### **B. Scanner Experience **

1.  **Log in**. The user is redirected to the home dashboard.
2.  **Access Scanner:** Click **'Scanner Interface'** 
3.  **Entry Scan:**
    * Paste the **Ticket ID**.
    * Click **'Process Scan'**. The system will report "Entry Granted" and update the ticket status to **'In Use'**.
4.  **Exit Scan:**
    * Paste the **SAME Ticket ID**.
    * Click **'Process Scan'**. The system will report "Exit Recorded" and update the ticket status to **'Used'**.
5.  **Offline Purchase:**
    * Click **'Go to Offline Cash Purchase'**.
    * Select `Station A` to `Station B` and click **'Issue Cash Ticket'**. A ticket is created and immediately marked as **USED**.

---

## 4. Administrative Control 

Log into the Admin Panel with `admin`/`password123`.

* **METROLINE:** Stations (`Station A`, `Station B`) and Lines (`Blue Line`) are configurable here.
* **TICKETS:** All generated tickets and user wallets can be reviewed and managed.
* **AUTHENTICATION:** Users (`scanner`, `passenger`) and Groups (`Scanners`, `Passengers`) are verified here.
