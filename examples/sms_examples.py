#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sendcloud_sms.codeSms import CodeSms
from sendcloud_sms.sms import SendCloudSms
from sendcloud_sms.templateSms import TemplateSms
from sendcloud_sms.voiceSms import VoiceSms

# Initialize the SendCloud SMS client with your SMS service provider credentials
send_cloud_sms = SendCloudSms("YOUR_SMS_USER", "YOUR_SMS_KEY")


def send_template_sms():
    # Create a TemplateSms object with the necessary parameters
    template_sms = TemplateSms(
        template_id=40513,  # Replace with your template ID
        phone="13800138000",  # Replace with the recipient's phone number
        vars_dict={"code": "1234"},  # Variables to be replaced in the template
        tag={"tag1": "tag1"}  # Additional tags for the SMS
    )
    # Send the template SMS and print the result message
    result = send_cloud_sms.send_template_sms(template_sms)
    print(result.message)


def send_voice_sms():
    # Create a VoiceSms object with the necessary parameters
    voice_sms = VoiceSms(
        phone="13800138000",  # Replace with the recipient's phone number
        code="123456",  # The code to be delivered via voice SMS
        tag={"tag1": "tag1"}  # Additional tags for the SMS
    )
    # Send the voice SMS and print the result message
    result = send_cloud_sms.send_voice_sms(voice_sms)
    print(result.message)


def send_code_sms():
    # Create a CodeSms object with the necessary parameters
    code_sms = CodeSms(
        phone="13800138000",  # Replace with the recipient's phone number
        sign_name="YourSignName",  # Replace with your sign name
        code="123456",  # The code to be sent as SMS
        tag={"tag1": "tag1"}  # Additional tags for the SMS
    )
    # Send the code SMS and print the result message
    result = send_cloud_sms.send_code_sms(code_sms)
    print(result.message)


if __name__ == "__main__":
    send_template_sms()
    send_voice_sms()
    send_code_sms()
