import smtplib
import asyncio
from concurrent.futures import ThreadPoolExecutor


class SmtpTools:
    """
    Class for working with SMTP
    """
    def __init__(self, host: str, port: int, email: str, password: str):
        self.email = email
        self.host = host
        self.port = port
        self.password = password
        self.executor = ThreadPoolExecutor()
        self.server = None

    def _connect(self):
        server = smtplib.SMTP_SSL(host=self.host, port=self.port, timeout=10)
        server.login(self.email, self.password)
        return server

    async def send_email(self, to_email: str, code: str):
        subject = '[Fast_API_Project] Password Reset'
        message = (f'Fast_API_Project Password Reset\n\n'
                   f'Hello,\n'
                   f'We have received a request '
                   f'to reset the password for your Fast_API_Project account: {to_email}.\n\n'
                   f'Your reset password code: {code}')

        loop = asyncio.get_running_loop()
        self.server = self._connect()
        await loop.run_in_executor(self.executor, self.server.sendmail, self.email, to_email,
                                   f"Subject: {subject}\n\n{message}")
        self.server.quit()

    def close(self):
        self.executor.shutdown(wait=True)