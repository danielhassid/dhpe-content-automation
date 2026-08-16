# פסק דין סיכונים — [YYYY-MM-DD] [שעה UTC]

> כותבת: מרים (binance-risk-manager) | קורא: איתן (binance-trade-executor)
> תוקף אישור: verdict_freshness_hours מ-limits.json. נדרס בכל ריצה.

## P-YYYY-MM-DD-01: APPROVED
- **גודל סופי:** [notional_usdt — שווה או קטן מההצעה]
- **בדיקות שעברו:** 1-8 ✓
- **הערה לאיתן:** [אם יש; למשל "פקודה נחה בבורסה, לא watcher"]
- **חותמת זמן:** [ISO]

## P-YYYY-MM-DD-02: VETO
- **סעיף:** [מספר הסעיף מסדר הבדיקה + המגבלה המדויקת מ-limits.json]
- **נימוק:** [משפט אחד]
- **חותמת זמן:** [ISO]

## T-YYYY-MM-DD-01: APPROVED (טריגר)
- **גודל סופי:** [notional_usdt]
- **TTL:** [שעות] — expires_at: [ISO]
- **סטטוס חתימה:** נחתם דרך sign_trigger.py ✓
- **חותמת זמן:** [ISO]

## הצעות שינוי ל-limits.json (לדניאל — לא עריכה עצמית)
- [אין / הצעה + נימוק]
