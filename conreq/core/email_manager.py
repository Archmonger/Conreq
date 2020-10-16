"""Conreq Email Manager: Sends emails to someone using a template. For example, when the user's request completes downloading."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from conreq.core import log

# TODO: Obtain template from the database on init


class EmailManager:
    """Sends emails to recepients.
    >>> Kwargs:
        sender_name: String name of the sender.
        sender_email: String email address of the sender.
        sender_password: String password for the sender.
        smtp_server_url: String address to the SMTP server (ex. smtp.gmail.com).
        smtp_server_port: String port number of the SMTP server.
    """

    def __init__(self, **kwargs):
        # Creating a logger (for log files)
        self.__logger = log.get_logger("Content Discovery")
        log.configure(self.__logger, log.WARNING)

        # Personal email login information
        try:
            # TODO: Obtain these values from the database on init
            self.__sender_name = kwargs["sender_name"]
            self.__sender_email = kwargs["sender_email"]
            self.__sender_password = kwargs["sender_password"]
            self.__smtp_server_url = kwargs["smtp_server_url"]
            self.__smtp_server_port = kwargs["smtp_server_port"]
            self.__smtp_server = None

            # Set up the email server and login
            self.__configure_encrypted_smtp()
        except:
            log.handler(
                "Failed to initialize the email manager!",
                log.ERROR,
                self.__logger,
            )

    def send_email(self, receiver_email, template, **kwargs):
        """Customizes an email template and sends the email to a recepient.

        Args:
            receiver_email: String email address of the receiver.
            template: String of a HTML template to send.

        Kwargs:
            Any values to be substituted into the template. For example...
            A kwargs value of content_type="movie" will substitute the string "{content_type}" with "movie"
        """
        try:
            # Set up the email subject, to, and from fields.
            email = MIMEMultipart("alternative")
            email["Subject"] = kwargs["content_name"] + " is available!"
            email["From"] = f'"{self.__sender_name}" <{self.__sender_email}>'
            email["To"] = receiver_email

            # Replacing {keywords} in the template with their respective values
            customized_template = template
            for key, value in kwargs.items():
                customized_template = customized_template.replace(
                    "{" + str(key) + "}", value
                )

            # Attach the message
            msg = MIMEText(customized_template, "html")
            email.attach(msg)

            # Send the email
            self.__smtp_server.sendmail(email["From"], email["To"], email.as_string())
        except:
            log.handler("Failed to send email!", log.ERROR, self.__logger)

    def __configure_encrypted_smtp(self):
        try:
            # Configure the email server
            self.__smtp_server = smtplib.SMTP(
                self.__smtp_server_url, self.__smtp_server_port
            )
            # Identify ourselves to the server
            self.__smtp_server.ehlo()
            # Secure our email with TLS encryption
            self.__smtp_server.starttls()
            # Re-identify as an encrypted connection
            self.__smtp_server.ehlo()
            # Log in to the SMTP server
            self.__smtp_server.login(self.__sender_email, self.__sender_password)
        except:
            log.handler(
                "Failed to configure encryped connection!",
                log.ERROR,
                self.__logger,
            )


# Test driver code
if __name__ == "__main__":

    email_manager = EmailManager(
        sender_name="My Name",
        sender_email="example@gmail.com",
        sender_password="password",
        smtp_server_url="smtp.gmail.com",
        smtp_server_port="587",
    )
    email_manager.send_email(
        "receiver@gmail.com",
        open("template_1.html", "r").read(),
        content_name="Avengers: End Game",
        content_type="movie",
        content_description="After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos' actions and restore order to the universe once and for all, no matter what consequences may be in store.",
        server_name="PlexyFlix",
        server_message="Come check it out on our website!",
        poster_img_url="https://image.tmdb.org/t/p/w600_and_h900_bestv2/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        watch_now_href="#",
        server_href="#",
        notifications_href="#",
        unsubscribe_href="#",
    )
