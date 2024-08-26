import unittest
from sendcloud_email.email import SendCloud, CommonMail
from sendcloud_email.mailBody import MailBody, Filter, TrackingFilter, Settings, UnsubscribeSettings, FilterSettings, \
    XSMTPAPI
from sendcloud_email.mailReceiver import MailReceiver
from sendcloud_email.templateMail import TemplateMail
from sendcloud_email.textContent import TextContent


class TestSendCloud(unittest.TestCase):

    def setUp(self):
        self.api_user = '*'
        self.api_key = '*'
        self.send_cloud = SendCloud(self.api_user, self.api_key)
        self.receiver = MailReceiver(
            to="6815549542@qq.com;",
            use_address_list=False
        )
        self.mail_body = MailBody(
            from_email="SendCloud@SendCloud.com",
            subject="Email from SendCloud SDK",
            content_summary="Summary of the email content",
            from_name="SendCloud",
            reply_to="noreply@sendcloud.com",
            headers={"X-Custom-Header": "Value"},
            resp_email_id=False,
            use_notification=True
        )
        self.text_content = TextContent(html="<p>This is an HTML email.</p>")
        self.template_invoke_name = "test_template_active"

        self.to_emails = [f"user{i+1}@example.com" for i in range(2)]
        self.names = [f"Name{i+1:03d}" for i in range(2)]
        self.moneys = [f"{i+1:03d}99" for i in range(2)]

        self.sub_values = {
            "%name%": self.names,
            "%amount%": self.moneys
        }

        self.settings = Settings(unsubscribe=UnsubscribeSettings(page_id=[1, 2]))

        self.subscription_tracking = TrackingFilter(settings=FilterSettings(enable="1"))
        self.open_tracking = TrackingFilter(settings=FilterSettings(enable="1"))
        self.click_tracking = TrackingFilter(settings=FilterSettings(enable="1"))

        self.filters = Filter(
            subscription_tracking=self.subscription_tracking,
            open_tracking=self.open_tracking,
            click_tracking=self.click_tracking
        )

        self.xsmtpapi = XSMTPAPI(
            to=self.to_emails,
            sub=self.sub_values,
            filters=self.filters,
            settings=self.settings
        )

    # 测试发送普通邮件的功能
    def test_send_common_email(self):
        mail = CommonMail(receiver=self.receiver, body=self.mail_body, content=self.text_content)
        result = self.send_cloud.send_common_email(mail)
        print(result.message)

    def test_send_template_email(self):
        mail = TemplateMail(receiver=self.receiver, body=self.mail_body, template_invoke_name=self.template_invoke_name)
        result = self.send_cloud.send_template_email(mail)
        print(result.message)

    def test_send_common_email_with_vars(self):
        mail = CommonMail(receiver=self.receiver, body=self.mail_body, content=self.text_content)
        mail.body.xsmtpapi = self.xsmtpapi
        result = self.send_cloud.send_common_email(mail)
        print(result.message)


if __name__ == '__main__':
    unittest.main()
