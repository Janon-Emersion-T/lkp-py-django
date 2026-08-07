import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape


logger = logging.getLogger(__name__)


class QuoteEnquiryEmailService:
    @staticmethod
    def _customer_subject(enquiry):
        return (
            f"We received your quote request "
            f"— {enquiry.reference_code}"
        )

    @staticmethod
    def _internal_subject(enquiry):
        return (
            f"New quote request: "
            f"{enquiry.reference_code} — "
            f"{enquiry.project_title}"
        )

    @staticmethod
    def _customer_text(enquiry):
        name = enquiry.name or "there"

        return f"""Hello {name},

Thank you for contacting LKProfessionals.

We have received your quote request and our team will review the details you provided.

Reference: {enquiry.reference_code}
Service: {enquiry.project_title or "Not specified"}

We will contact you using your preferred contact method as soon as possible.

If you need to add anything to your request, reply to this email or contact us at {settings.LKP_CONTACT_EMAIL}.

Regards,
LKProfessionals
Empowering Businesses Through Reliable IT Solutions
"""

    @staticmethod
    def _customer_html(enquiry):
        name = escape(
            enquiry.name or "there"
        )

        reference = escape(
            enquiry.reference_code
        )

        service = escape(
            enquiry.project_title
            or "Not specified"
        )

        contact_email = escape(
            settings.LKP_CONTACT_EMAIL
        )

        return f"""
<!doctype html>
<html lang="en">
<body style="
  margin:0;
  padding:0;
  background:#f4f6f9;
  font-family:Arial,Helvetica,sans-serif;
  color:#17263c;
">
  <table
    role="presentation"
    width="100%"
    cellspacing="0"
    cellpadding="0"
    style="background:#f4f6f9;padding:32px 16px;"
  >
    <tr>
      <td align="center">
        <table
          role="presentation"
          width="100%"
          cellspacing="0"
          cellpadding="0"
          style="
            max-width:620px;
            background:#ffffff;
            border:1px solid #dfe5ed;
            border-radius:12px;
            overflow:hidden;
          "
        >
          <tr>
            <td style="
              padding:26px 30px;
              background:#0b2f8f;
              color:#f4f1e8;
            ">
              <div style="
                font-size:12px;
                font-weight:700;
                letter-spacing:1.4px;
                text-transform:uppercase;
                opacity:.76;
              ">
                LKProfessionals
              </div>

              <h1 style="
                margin:8px 0 0;
                font-size:25px;
                line-height:1.25;
                font-weight:600;
              ">
                We received your quote request
              </h1>
            </td>
          </tr>

          <tr>
            <td style="
              padding:30px;
              font-size:15px;
              line-height:1.7;
            ">
              <p style="margin:0 0 18px;">
                Hello {name},
              </p>

              <p style="margin:0 0 18px;">
                Thank you for contacting
                <strong>LKProfessionals</strong>.
                We have received your project enquiry
                and will review the requirements you
                provided.
              </p>

              <table
                role="presentation"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                  margin:24px 0;
                  background:#f7f9fc;
                  border:1px solid #e2e7ee;
                  border-radius:8px;
                "
              >
                <tr>
                  <td style="padding:16px 18px;">
                    <div style="
                      color:#6f7b8d;
                      font-size:12px;
                      margin-bottom:4px;
                    ">
                      Reference
                    </div>

                    <strong>
                      {reference}
                    </strong>
                  </td>
                </tr>

                <tr>
                  <td style="
                    padding:0 18px 16px;
                  ">
                    <div style="
                      color:#6f7b8d;
                      font-size:12px;
                      margin-bottom:4px;
                    ">
                      Service required
                    </div>

                    <strong>
                      {service}
                    </strong>
                  </td>
                </tr>
              </table>

              <p style="margin:0 0 18px;">
                Our team will contact you using your
                preferred contact method as soon as
                possible.
              </p>

              <p style="margin:0;">
                If you need to add anything to your
                request, simply reply to this email or
                contact us at
                <a
                  href="mailto:{contact_email}"
                  style="color:#0b2f8f;"
                >
                  {contact_email}
                </a>.
              </p>
            </td>
          </tr>

          <tr>
            <td style="
              padding:20px 30px;
              background:#f7f9fc;
              border-top:1px solid #e2e7ee;
              color:#687589;
              font-size:12px;
              line-height:1.6;
            ">
              LKProfessionals<br>
              Empowering Businesses Through Reliable IT Solutions.
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    @staticmethod
    def _internal_text(enquiry):
        metadata = enquiry.metadata or {}

        return f"""A new quote request has been submitted.

Reference: {enquiry.reference_code}
Name: {enquiry.name}
Company: {enquiry.company_name or "-"}
Service: {enquiry.project_title or "-"}
Email: {enquiry.email}
WhatsApp: {enquiry.phone or "-"}
Country: {enquiry.country or "-"}
Preferred contact: {metadata.get("preferred_contact_method") or "-"}
Best time to contact: {metadata.get("best_time_to_contact") or "-"}
Form source: {metadata.get("source_surface") or "-"}
Source URL: {enquiry.source_url or "-"}

Project description:
{enquiry.project_description}

This enquiry is available in the LKProfessionals dashboard.
"""

    @staticmethod
    def _internal_html(enquiry):
        metadata = enquiry.metadata or {}

        fields = [
            (
                "Reference",
                enquiry.reference_code,
            ),
            (
                "Name",
                enquiry.name,
            ),
            (
                "Company",
                enquiry.company_name or "-",
            ),
            (
                "Service",
                enquiry.project_title or "-",
            ),
            (
                "Email",
                enquiry.email or "-",
            ),
            (
                "WhatsApp",
                enquiry.phone or "-",
            ),
            (
                "Country",
                enquiry.country or "-",
            ),
            (
                "Preferred contact",
                metadata.get(
                    "preferred_contact_method",
                )
                or "-",
            ),
            (
                "Best time to contact",
                metadata.get(
                    "best_time_to_contact",
                )
                or "-",
            ),
            (
                "Form source",
                metadata.get(
                    "source_surface",
                )
                or "-",
            ),
            (
                "Source URL",
                enquiry.source_url or "-",
            ),
        ]

        rows = "".join(
            f"""
            <tr>
              <td style="
                width:34%;
                padding:9px 12px;
                border-bottom:1px solid #e5e9ef;
                color:#6a7688;
                font-size:13px;
                vertical-align:top;
              ">
                {escape(label)}
              </td>

              <td style="
                padding:9px 12px;
                border-bottom:1px solid #e5e9ef;
                color:#17263c;
                font-size:13px;
                font-weight:600;
                vertical-align:top;
              ">
                {escape(str(value))}
              </td>
            </tr>
            """
            for label, value in fields
        )

        description = escape(
            enquiry.project_description
        ).replace(
            "\n",
            "<br>",
        )

        return f"""
<!doctype html>
<html lang="en">
<body style="
  margin:0;
  padding:0;
  background:#f4f6f9;
  font-family:Arial,Helvetica,sans-serif;
  color:#17263c;
">
  <table
    role="presentation"
    width="100%"
    cellspacing="0"
    cellpadding="0"
    style="background:#f4f6f9;padding:30px 16px;"
  >
    <tr>
      <td align="center">
        <table
          role="presentation"
          width="100%"
          cellspacing="0"
          cellpadding="0"
          style="
            max-width:680px;
            background:#ffffff;
            border:1px solid #dfe5ed;
            border-radius:12px;
            overflow:hidden;
          "
        >
          <tr>
            <td style="
              padding:24px 28px;
              background:#0b2f8f;
              color:#f4f1e8;
            ">
              <div style="
                font-size:11px;
                font-weight:700;
                letter-spacing:1.3px;
                text-transform:uppercase;
                opacity:.75;
              ">
                New website enquiry
              </div>

              <h1 style="
                margin:7px 0 0;
                font-size:23px;
                font-weight:600;
              ">
                {escape(enquiry.reference_code)}
              </h1>
            </td>
          </tr>

          <tr>
            <td style="padding:24px 28px;">
              <table
                role="presentation"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                  border:1px solid #e5e9ef;
                  border-radius:8px;
                  overflow:hidden;
                  border-collapse:separate;
                  border-spacing:0;
                "
              >
                {rows}
              </table>

              <h2 style="
                margin:26px 0 10px;
                font-size:15px;
              ">
                Project description
              </h2>

              <div style="
                padding:16px;
                background:#f7f9fc;
                border:1px solid #e5e9ef;
                border-radius:8px;
                font-size:14px;
                line-height:1.65;
              ">
                {description}
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    @classmethod
    def send_customer_email(
        cls,
        enquiry,
    ):
        if not enquiry.email:
            return 0

        message = EmailMultiAlternatives(
            subject=cls._customer_subject(
                enquiry
            ),
            body=cls._customer_text(
                enquiry
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[
                enquiry.email,
            ],
            reply_to=[
                settings.LKP_CONTACT_EMAIL,
            ],
        )

        message.attach_alternative(
            cls._customer_html(
                enquiry
            ),
            "text/html",
        )

        return message.send(
            fail_silently=False,
        )

    @classmethod
    def send_internal_email(
        cls,
        enquiry,
    ):
        reply_to = []

        if enquiry.email:
            reply_to.append(
                enquiry.email
            )

        message = EmailMultiAlternatives(
            subject=cls._internal_subject(
                enquiry
            ),
            body=cls._internal_text(
                enquiry
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[
                settings.LKP_QUOTE_NOTIFICATION_EMAIL,
            ],
            reply_to=reply_to,
        )

        message.attach_alternative(
            cls._internal_html(
                enquiry
            ),
            "text/html",
        )

        return message.send(
            fail_silently=False,
        )

    @classmethod
    def send_quote_emails(
        cls,
        enquiry,
    ):
        results = {
            "customer": False,
            "internal": False,
        }

        try:
            results["customer"] = bool(
                cls.send_customer_email(
                    enquiry
                )
            )
        except Exception:
            logger.exception(
                "Failed to send quote acknowledgement "
                "for %s.",
                enquiry.reference_code,
            )

        try:
            results["internal"] = bool(
                cls.send_internal_email(
                    enquiry
                )
            )
        except Exception:
            logger.exception(
                "Failed to send internal quote "
                "notification for %s.",
                enquiry.reference_code,
            )

        return results
