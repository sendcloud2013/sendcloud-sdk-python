#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sendcloud_email.commonMail import CommonMail
from sendcloud_email.email import SendCloud
from sendcloud_email.mailBody import MailBody, Filter, TrackingFilter, Settings, UnsubscribeSettings, FilterSettings, \
    XSMTPAPI
from sendcloud_email.mailReceiver import MailReceiver
from sendcloud_email.templateMail import TemplateMail
from sendcloud_email.textContent import TextContent

# Initialize the SendCloud client with your API user and API key
api_user = 'YOUR_API_USER'
api_key = 'YOUR_API_KEY'
send_cloud = SendCloud(api_user, api_key)

# Create a MailReceiver object with the recipient's email address
receiver = MailReceiver(
    to="recipient@example.com",
    use_address_list=False
)

# Create a MailBody object with the email's metadata
mail_body = MailBody(
    from_email="SendCloud@SendCloud.com",
    subject="Email from SendCloud SDK",
    content_summary="Summary of the email content",
    from_name="SendCloud",
    reply_to="noreply@sendcloud.com",
    headers={"X-Custom-Header": "Value"},
    resp_email_id=False,
    use_notification=True
)

# Create a TextContent object with the HTML content of the email
text_content = TextContent(html="<p>This is an HTML email.</p>")

# Create a TemplateMail object for sending template-based emails
template_mail = TemplateMail(
    receiver=receiver,
    body=mail_body,
    template_invoke_name="test_template_active"
)


# Send a template-based email
def send_template_email():
    result = send_cloud.send_template_email(template_mail)
    print(result.message)


# Create a CommonMail object for sending regular emails
common_mail = CommonMail(
    receiver=receiver,
    body=mail_body,
    content=text_content
)


# Send a regular email
def send_common_email():
    result = send_cloud.send_common_email(common_mail)
    print(result.message)


# Create an XSMTPAPI object for advanced features like variable substitution
to_emails = ["user1@example.com", "user2@example.com"]
names = ["Name001", "Name002"]
moneys = ["0199", "0299"]
sub_values = {
    "%name%": names,
    "%amount%": moneys
}
filters = Filter(
    subscription_tracking=TrackingFilter(settings=FilterSettings(enable="1")),
    open_tracking=TrackingFilter(settings=FilterSettings(enable="1")),
    click_tracking=TrackingFilter(settings=FilterSettings(enable="1"))
)
settings = Settings(unsubscribe=UnsubscribeSettings(page_id=[1, 2]))
xsmtpapi = XSMTPAPI(
    to=to_emails,
    sub=sub_values,
    filters=filters,
    settings=settings
)

# Update the CommonMail object to use XSMTPAPI for variable substitution
common_mail.body.xsmtpapi = xsmtpapi


# Send a common email with variables substituted in the content
def send_common_email_with_vars():
    result = send_cloud.send_common_email(common_mail)
    print(result.message)


if __name__ == "__main__":
    send_template_email()
    send_common_email()
    send_common_email_with_vars()
