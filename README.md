---
title: Financial Data Cleaning Env
emoji: 💼
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

## 📌 Overview

This project implements a **real-world financial data cleaning environment** using the OpenEnv specification.  
It simulates how analysts clean messy datasets in finance, enabling AI agents to learn and optimize data cleaning workflows.

---

## 🎯 Motivation

Financial datasets often contain:

- Missing values  
- Duplicate records  
- Incorrect entries (e.g., negative amounts)  
- Invalid timestamps  
- Outliers / anomalies  

Cleaning such data is a **critical and time-consuming task** in real-world analytics pipelines.

👉 This environment allows training and evaluating AI agents to **automate data cleaning intelligently**.

---

## ⚙️ Environment Design

The environment follows the OpenEnv API:

- `reset()` → Initializes dataset  
- `step(action)` → Applies transformation  
- `state()` → Returns current dataset  

### 📊 Observation Space

Each observation includes:

- Current dataset (rows as JSON)  
- Step count  
- Data quality score  

---

## 🎮 Action Space

Agents can perform the following actions:

- `remove_duplicates` → Removes duplicate rows  
- `fix_negative_amount` → Converts negative values to positive  
- `drop_missing_customer` → Removes rows with missing customer  

---

## 🧠 Reward Function

The reward is **dense and progressive**, not binary:

- ✅ Positive reward for improving data quality  
- ❌ Penalty for no improvement  
- ❌ Penalty for excessive data deletion  

This ensures agents learn **efficient and meaningful cleaning strategies**.

---

## 🏁 Tasks & Difficulty Levels

### 🟢 Easy
- Remove duplicates  
- Fix negative values  
- Handle missing fields  

### 🟡 Medium
- Includes date validation and formatting  

### 🔴 Hard
- Adds anomaly detection (e.g., unusually large transactions)  

👉 Each task is evaluated using a deterministic grader (score: 0.0 – 1.0)

---

## 🤖 Inference (Agent Execution)

The `inference.py` script:

- Uses OpenAI client for decision-making  
- Falls back to rule-based logic if API fails  
- Logs execution in required format:
