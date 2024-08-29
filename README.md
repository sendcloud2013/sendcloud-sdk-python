# SendCloud Python SDK

## Overview

The SendCloud Python SDK offers an intuitive interface for integrating SendCloud's email and SMS services into your Python applications, supporting Python versions 3.8 and above. It simplifies the process of sending various types of messages and ensures a seamless communication experience.

## Key Features

- **Email SDK**: Capable of sending standard emails and emails using predefined templates.
- **SMS SDK**: Facilitates sending template-based SMS messages, voice SMS, and verification codes.

1. ## Getting Started

   ### Downloading the SDK

   1. **Clone the Repository**: Download the SDK from the [SendCloud Python SDK GitHub repository](https://github.com/sendcloud2013/sendcloud-sdk-python).

      ```
      git clone https://github.com/sendcloud2013/sendcloud-sdk-python.git
      ```

   2. **Setup**: Navigate into the downloaded SDK directory and set up your environment.

   ### Email SDK

   1. **Initialization**: Initialize the SendCloud email client with your API credentials.

      ```
      python
      from sendcloud_email.email import SendCloud
      
      client = SendCloud(api_key="API_KEY", api_secret="API_SECRET")
      ```

   2. **Usage Examples**: Explore usage examples in the `examples/email_examples.py` or the documentation.

   ### SMS SDK

   1. **Initialization**: Initialize the SendCloud SMS client with your SMS service provider credentials.

      ```
      python
      from sendcloud_sms.sms import SendCloudSms
      
      client = SendCloudSms(sms_user="SMS_USER", sms_key="SMS_KEY")
      ```

   2. **Usage Examples**: Review usage examples provided in the `examples/sms_examples.py` file.

## Documentation

- Comprehensive documentation and usage examples are available in the [SendCloud Python SDK Documentation](https://www.sendcloud.net/doc/).

## Support

For any inquiries or issues, reach out to SendCloud's support team or engage with the community on [SendCloud's GitHub](https://github.com/sendcloud2013).

## Contribution

We appreciate your choice of SendCloud as your communication platform. Contributions to the SDK are welcome. We are eager to assist you in successfully integrating our Python SDKs.