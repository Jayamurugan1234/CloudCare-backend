import smtplib
import socket
from django.core.mail.backends.smtp import EmailBackend as DjangoSMTPBackend


class IPv4SMTP(smtplib.SMTP):
    """Forces IPv4 when connecting, to avoid Render's lack of outbound IPv6 routing."""
    def _get_socket(self, host, port, timeout):
        if timeout is not None and not timeout:
            raise ValueError("Non-blocking socket (timeout=0) is not supported")
        sys_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if timeout is not None:
            sys_socket.settimeout(timeout)
        sys_socket.connect((host, port))
        return sys_socket


class IPv4EmailBackend(DjangoSMTPBackend):
    """Django SMTP backend that forces IPv4 connections."""
    def open(self):
        if self.connection:
            return False
        connection_class = IPv4SMTP
        try:
            self.connection = connection_class(self.host, self.port, timeout=self.timeout)
            if self.use_tls:
                self.connection.starttls()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise