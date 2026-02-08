import dns.resolver
import smtplib
import socket
import logging

# Настройка логирования для продакшн-вида
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def verify_email(email):
    try:
        domain = email.split('@')[1]
    except (IndexError, AttributeError):
        return "ошибка формата"

    # 1. Проверка MX-записей
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx_host = str(sorted(answers, key=lambda r: r.preference)[0].exchange).rstrip('.')
    except Exception:
        return "домен отсутствует"

    # 2. SMTP Handshake
    try:
        # Таймаут 10с важен для защиты от "подвисших" серверов
        with smtplib.SMTP(host=mx_host, timeout=10) as smtp:
            smtp.helo(socket.gethostname())
            smtp.mail('test@verify-service.com')
            code, _ = smtp.rcpt(email)

            if code == 250:
                return "домен валиден"
            return "MX-записи отсутствуют или некорректны"
    except Exception:
        return "MX-записи отсутствуют или некорректны"


if __name__ == "__main__":
    emails = ["admin@github.com", "wrong-test-mail@nonexistent.com", "test@gmail.com"]
    for email in emails:
        print(f"{email}: {verify_email(email)}")
