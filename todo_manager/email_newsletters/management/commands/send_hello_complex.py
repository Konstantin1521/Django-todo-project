from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class Command(BaseCommand):
    help = 'Send exmaple hello email'

    def handle(self, *args, **options):
        self.stdout.write('Send complex email')

        name = "Arata"
        subject = f"Welcome {name}"
        sender = "admin@admin.com"
        recipient = "arata@exmaple.com"
        context = {"name": name}

        text_content = render_to_string(
            "email_newsletters/welcome_message.txt",
            context=context,
        )

        html_content = render_to_string(
            "email_newsletters/welcome_message.html",
            context=context
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=sender,
            to=[recipient],
            headers={"List-Unsubscribe": "<mailto:<EMAIL>>"},
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        self.stdout.write(self.style.SUCCESS('OK'))