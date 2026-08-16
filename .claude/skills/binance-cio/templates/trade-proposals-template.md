# הצעות עסקה — [YYYY-MM-DD] [שעה UTC]

> כותב: אלון (binance-cio) | קוראת: מרים (binance-risk-manager)
> נדרס בכל ריצה. הצעה בלי כל השדות — מוחזרת.

## P-YYYY-MM-DD-01 — [ביצוע מיידי / פקודה נחה בבורסה]
- **symbol:** BTCUSDT
- **side:** BUY
- **type:** LIMIT | MARKET | OCO | STOP_LOSS_LIMIT | TAKE_PROFIT_LIMIT
- **notional_usdt:** [מספר; מרים רשאית להקטין]
- **price:** [מחיר לימיט]
- **stop:** [חובה בקנייה]
- **take_profit:** [יעד]
- **תיק:** Core / Satellite
- **תזה:** [שני משפטים: על סמך איזה דוח, ומה נקודת הפסילה]

## T-YYYY-MM-DD-01 — [טריגר מותנה ל-watcher]
- **symbol:** ETHUSDT
- **condition:** price <= [מחיר]  (אופרטורים: <=, >=, <, >)
- **order:** {type, side, notional_usdt, price, stop, take_profit}
- **TTL:** [שעות, עד trigger_ttl_hours_max מ-limits.json]
- **תזה:** [שני משפטים]
- **למה טריגר ולא פקודה נחה:** [חובה לנמק — ברירת המחדל היא פקודה נחה בבורסה]
