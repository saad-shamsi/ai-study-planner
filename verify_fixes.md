# Verification Guide

## 1. Notification Tab

- **Action**: Open Dashboard -> Click "Notifications" in sidebar.
- **Expectation**:
  - Should verify "0 notifications" issue is resolved (if you have data).
  - You should see a **List** of notifications (read/unread).
  - You should see **Delete (Trash)** and **Mark Read (Check)** buttons.
  - Clicking "Trash" should remove any item immediately.

## 2. Dark Theme Fix

- **Action**: Go to "Home" tab.
- **Expectation**:
  - "Quick Actions", "Stats", and "Garden" cards should now be **Dark Blue/Grey**.
  - No more bright white squares clashing with the background.

## 3. Streak Logic

- **Action**: Logout and Login again.
- **Expectation**:
  - If you logged in yesterday, you should see a Windows Toast: **"🔥 Streak Maintained!"**.
  - If this is your first time today, streak should increment by 1.
  - Check the "Streak" card on Home view to see the number go up.
