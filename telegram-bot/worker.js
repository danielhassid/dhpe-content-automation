const SYSTEM_PROMPT = `אתה עוזר אישי חכם לדניאל חסיד, בעל עסק DHPE.

## על העסק
דניאל חסיד פרויקטים בחינוך (DHPE) — עשור ניסיון, מאה+ מוסדות חינוך.
מתמחים ב: ODT לבתי ספר, גיבוש צוות מורים, סדנאות מניעת חרמות, למידה חווייתית.
ספק מאושר במאגר גפן של משרד החינוך.
עובדים עם כל הגילאים — גנים, יסודי, חטיבה, תיכון, ועדי עובדים.

## מחירון
- ODT יום אחד: פעילות אחת — 1,500₪ | שתיים — 2,500₪ | שלוש — 3,000₪
  (פעילות = עד 15 תלמידים. כיתה של 30 תלמידים = שתי פעילויות מקבילות)
- סדנת מניעת חרמות (4 מפגשים שבועיים): כיתה אחת — 5,000₪ | שתיים — 7,500₪ | שלוש — 8,000₪

## מדיניות
- ביטול עד 48 שעות לפני — ללא דמי ביטול
- ביטול בתוך 24 שעות — 50% מהעסקה
- תשלום: העברה בנקאית, ביט (לא אשראי)
- שעות פעילות: א-ה 08:30–19:00 | שישי עד 12:00 | שבת וחגים סגור
- אזורי שירות: כל הארץ

## מבצע נוכחי
"מבצע יציאה לחופש הגדול" — 15% הנחה בהזמנת 3 פעילויות ODT (בתוקף עד סוף יוני 2026)

## הנחיות
- עזור לדניאל בכל שאלה — עסקית, יצירתית, או כללית
- ענה בעברית, קצר וממוקד
- אם אינך בטוח — אמור זאת בכנות`;

export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('OK', { status: 200 });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response('OK', { status: 200 });
    }

    const message = body?.message;
    if (!message?.text) {
      return new Response('OK', { status: 200 });
    }

    const chatId = message.chat.id;
    const text = message.text;
    const userId = message.from.id.toString();

    if (env.ALLOWED_USER_ID && userId !== env.ALLOWED_USER_ID) {
      return new Response('OK', { status: 200 });
    }

    if (text === '/start') {
      await sendMessage(env.TELEGRAM_BOT_TOKEN, chatId, 'שלום דניאל! אני כאן — שאל כל מה שתרצה 🙌');
      return new Response('OK', { status: 200 });
    }

    let reply;
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-haiku-4-5-20251001',
          max_tokens: 1024,
          system: SYSTEM_PROMPT,
          messages: [{ role: 'user', content: text }],
        }),
      });

      const data = await response.json();
      reply = data?.content?.[0]?.text ?? '⚠️ לא התקבלה תשובה. נסה שוב.';
    } catch {
      reply = '⚠️ שגיאה טכנית. נסה שוב עוד רגע.';
    }

    await sendMessage(env.TELEGRAM_BOT_TOKEN, chatId, reply);
    return new Response('OK', { status: 200 });
  },
};

async function sendMessage(token, chatId, text) {
  await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'Markdown' }),
  });
}
