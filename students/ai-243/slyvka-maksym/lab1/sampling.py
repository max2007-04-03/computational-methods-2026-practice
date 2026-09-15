from providers import make_client
from utils.lab_logger import custom_logger

logger = custom_logger('lab1', overwrite=True)

client, model = make_client("local")

CREATIVE = "Назва рекомендаційного сервісу фільмів"
FACTUAL = "Рік випуску першого iPhone"

def run(prompt, n=5, **params):
    """Запускає промпт n разів і повертає список відповідей."""
    answers = []
    for _ in range(n):
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **params,
        )
        answers.append(r.choices[0].message.content.strip())
    return answers

logger.info("=== Вплив temperature на креативність ===")
for t in [0.0, 0.7, 1.5]:
    answers = run(CREATIVE, temperature=t)
    logger.info(f"temperature={t}: унікальних {len(set(answers))} з 5")
    for a in answers:
        logger.info(f"  {a}")

logger.info("=== Вплив top_p на креативність ===")
for p in [0.1, 0.5, 1.0]:
    answers = run(CREATIVE, temperature=0.7, top_p=p)
    logger.info(f"top_p={p}: унікальних {len(set(answers))} з 5")

logger.info("=== Вплив temperature на фактичні знання ===")
for t in [0.0, 1.5]:
    answers = run(FACTUAL, temperature=t)
    logger.info(f"temperature={t}: {answers}")

logger.info("=== Перевірка відтворюваності ===")
answers = run(FACTUAL, n=10, temperature=0.0)
logger.info(f"Усі відповіді однакові: {len(set(answers)) == 1}")
