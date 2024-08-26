from sendcloud_email.mailBody import MailBody
from sendcloud_email.mailReceiver import MailReceiver
from sendcloud_email.validationError import ValidationError


class TemplateMail:

    def __init__(self, receiver: MailReceiver, body: MailBody, template_invoke_name: str):
        self.receiver = receiver
        self.body = body
        self.template_invoke_name = template_invoke_name

    def validate_template_mail(self):
        if not self.receiver.to and (not self.body.xsmtpapi or not self.body.xsmtpapi.to):
            raise ValidationError("to cannot be empty")

        if not self.body.xsmtpapi or not self.body.xsmtpapi.to or self.receiver.use_address_list:
            self.receiver.validate_receiver()

        if not self.receiver.use_address_list and self.body.xsmtpapi:
            self.body.xsmtpapi.validate_xsmtpapi()

        self.body.validate_mail_body()

        if not self.template_invoke_name:
            raise ValidationError("templateInvokeName cannot be empty")

    def prepare_send_template_email_params(self, params):
        self.receiver.prepare_mail_receiver_params(params)
        self.body.prepare_mail_body_params(params)
        params['templateInvokeName'] = self.template_invoke_name
