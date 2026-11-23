from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from .models import Payment


@dataclass
class SandboxPaymentResult:
    reference: str
    status: str
    provider_response: dict


class SandboxPaymentGateway:
    """Sandbox payment gateway used for safe local and CI flows."""

    def charge(self, *, amount, payment_method: str) -> SandboxPaymentResult:
        reference = f"txn_{uuid4().hex[:18]}"
        return SandboxPaymentResult(
            reference=reference,
            status=Payment.Status.SUCCEEDED,
            provider_response={
                "amount": str(amount),
                "payment_method": payment_method,
                "provider": "sandbox",
            },
        )
