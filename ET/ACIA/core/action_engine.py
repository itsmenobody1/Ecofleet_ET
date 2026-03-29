"""
action_engine.py — Simulates enterprise API execution pipelines for autonomous agents.
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, Any

from config.settings import ACTION_LOG_PATH, CURRENCY_SYMBOL
from workflows.action_logs import append_action_log


def execute_action(finding: Dict[str, Any], approved_by: str = "System User", dry_run: bool = False) -> Dict[str, Any]:
    """
    Executes the corrective action for a finding.
    Returns simulated API Request Payloads to demonstrate real-world execution capacity.
    """
    ftype = finding.get("type", "unknown")
    dispatch = {
        "price_overrun":            _action_renegotiate_vendor,
        "duplicate_vendor_pricing": _action_consolidate_vendor,
        "idle_server":              _action_shutdown_server,
        "unused_licenses":          _action_reclaim_licenses,
        "sla_breach_risk":          _action_escalate_ticket,
        "duplicate_invoice":        _action_flag_finance,
    }
    handler = dispatch.get(ftype, _action_generic)
    result = handler(finding)
    
    result["approved_by"] = approved_by
    result["executed_at"] = datetime.now().isoformat()
    result["annual_savings"] = finding.get("annual_impact", 0)

    if not dry_run:
        append_action_log(result)
    return result


# ── Simulated API Execution Handlers ──────────────────────────────────────────

def _action_renegotiate_vendor(f: Dict) -> Dict:
    payload = {
        "endpoint": "https://api.ariba.com/v2/rfq/renegotiate",
        "method": "POST",
        "headers": {"Authorization": "Bearer ARIBA_TOKEN_**"},
        "body": {
            "vendor_id": f.get("vendor"),
            "item_name": f.get("item"),
            "target_price": f.get("market_price", 0),
            "justification": "Automated AI Price Variance Detection"
        }
    }
    return {
        "action": "vendor_renegotiation_api_triggered",
        "description": f"📧 Transmitting automated RFQ negotiation payload to SAP Ariba for {f.get('vendor')}.",
        "icon": "💸", "category": "Procurement",
        "payload": json.dumps(payload, indent=2)
    }


def _action_consolidate_vendor(f: Dict) -> Dict:
    payload = {
        "endpoint": "https://api.coupa.com/api/suppliers/consolidate",
        "method": "PUT",
        "body": {
            "item_sku": f.get("item"),
            "affected_vendors": f.get("vendors", []),
            "target_vendor": f.get("vendors", [""])[0],
            "action": "soft_block_duplicates"
        }
    }
    return {
        "action": "vendor_consolidation_webhook",
        "description": f"📋 Pushing vendor soft-block to Coupa procurement system for {f.get('item')}.",
        "icon": "📋", "category": "Procurement",
        "payload": json.dumps(payload, indent=2)
    }


def _action_shutdown_server(f: Dict) -> Dict:
    payload = {
        "aws_service": "ec2",
        "action": "StopInstances",
        "parameters": {
            "InstanceIds": [f.get("server", "i-unknown")],
            "Force": False,
            "DryRun": False
        },
        "iam_role": "arn:aws:iam::123456789:role/ACIA-Autonomous-Execution"
    }
    return {
        "action": "aws_ec2_stop_initiated",
        "description": f"🖥️ Authenticated AWS Session. Invoking EC2 StopInstances on {f.get('server')}.",
        "icon": "☁️", "category": "Cloud Infrastructure",
        "payload": json.dumps(payload, indent=2)
    }


def _action_reclaim_licenses(f: Dict) -> Dict:
    payload = {
        "endpoint": f"https://dev-123.okta.com/api/v1/apps/{f.get('tool')}/users",
        "method": "DELETE",
        "parameters": {
            "inactive_days": 30,
            "batch_size": f.get("unused_seats", 0)
        },
        "workflow": "ACIA_License_Reclamation_Cron"
    }
    return {
        "action": "okta_license_reclamation",
        "description": f"🔑 Triggering Okta API to deprovision {f.get('unused_seats', 0)} inactive seats for {f.get('tool')}.",
        "icon": "🔑", "category": "SaaS",
        "payload": json.dumps(payload, indent=2)
    }


def _action_escalate_ticket(f: Dict) -> Dict:
    payload = {
        "endpoint": "https://yourdomain.atlassian.net/rest/api/3/issue/escalate",
        "method": "POST",
        "body": {
            "issue_id": f.get("ticket_id"),
            "new_priority": "Highest",
            "assignee": "escalations-tier3@company.com",
            "comment": f"⚠️ Automated ACIA Escalation: SLA breaches in {f.get('remaining_minutes', 0)} mins."
        }
    }
    return {
        "action": "jira_ticket_escalated",
        "description": f"🚨 Jira API hit: Ticket {f.get('ticket_id')} escalated to Tier 3 engineering.",
        "icon": "🚨", "category": "SLA",
        "payload": json.dumps(payload, indent=2)
    }


def _action_flag_finance(f: Dict) -> Dict:
    payload = {
        "endpoint": "https://api.netsuite.com/rest/vendorbill/hold",
        "method": "POST",
        "body": {
            "invoice_number": f.get("invoice_number"),
            "vendor": f.get("vendor"),
            "reason": f"Duplicate payment vector detected ({f.get('occurrences', 2)}x occurrences).",
            "hold_fund_amount": f.get("total_paid", 0)
        }
    }
    return {
        "action": "netsuite_payment_hold",
        "description": f"💰 NetSuite API invoked: Payment hold placed on invoice {f.get('invoice_number')}.",
        "icon": "💰", "category": "Finance",
        "payload": json.dumps(payload, indent=2)
    }


def _action_generic(f: Dict) -> Dict:
    payload = {"status": "alert_only", "finding_type": f.get("type")}
    return {
        "action": "generic_alert",
        "description": f"⚠️ Generating generic internal task for {f.get('type')}",
        "icon": "⚠️", "category": "General",
        "payload": json.dumps(payload, indent=2)
    }
