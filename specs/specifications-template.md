# Intent
Build a service that processes payments.

# Scope
In scope:
- Charge a card and return success or failure
- Validate card expiration and format
Out of scope:
- Refunds
- Chargebacks

# Constraints
- No blocking I/O
- Kotlin coroutines only
- Must run in under 200ms for valid cards

# Interfaces
- processPayment(request): Result

# Data contracts
Request:
- cardNumber: string (16 digits)
- expiryMonth: int (1-12)
- expiryYear: int (YYYY)
- amountCents: int (> 0)
Response:
- status: "success" | "error"
- errorCode?: string

# Dependencies
- Payment gateway: Stripe (mocked in tests)
- Env vars: STRIPE_API_KEY

# Behavioral rules
- Reject expired cards with errorCode "card_expired"
- Reject invalid formats with errorCode "invalid_card"
- Do not retry on gateway 4xx errors

# Examples
Input: valid card → Success
Input: expired card → Error("card_expired")
