import smtplib
import asyncio
from concurrent.futures import ThreadPoolExecutor


class SmtpTools:
    def __init__(self, host: str, port: int, email: str, password: str):
        self.email = email
        self.host = host
        self.port = port
        self.password = password
        self.executor = ThreadPoolExecutor()
        self.server = self._connect()

    def _connect(self):
        server = smtplib.SMTP_SSL(host=self.host, port=self.port, timeout=10)
        server.login(self.email, self.password)
        return server

    async def send_email(self, to_email: str, code: str):
        subject = '[Web_Example_Project] Password Reset'
        message = (f'Web_Example_Project Password Reset\n\n'
                   f'Hello,\n'
                   f'We have received a request '
                   f'to reset the password for your Web_Example_Project account: {to_email}.\n\n'
                   f'Your reset password code:{code}')

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self.executor, self.server.sendmail, self.email, to_email, f"Subject: {subject}\n\n{message}")
        self.server.quit()

    def __del__(self):
        self.executor.shutdown(wait=True)