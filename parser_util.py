"""
Email Parser Utility for Phishing Email Detector
Handles parsing .eml files and extracting content
"""

import email
from email import policy
from email.parser import BytesParser, Parser

class EmailParser:
    """
    Class for parsing email files and extracting content
    """
    
    def __init__(self):
        """Initialize the email parser"""
        # Initialize parsers
        self.bytes_parser = BytesParser(policy=policy.default)
        self.str_parser = Parser(policy=policy.default)
    
    def parse_eml_file(self, file_path):
        """
        Parse an .eml file and extract the content
        
        Args:
            file_path (str): Path to the .eml file
            
        Returns:
            str: The extracted email content (subject + body)
        """
        try:
            # Read the file
            with open(file_path, 'rb') as fp:
                # Parse the email
                msg = self.bytes_parser.parse(fp)
                
                # Extract content
                return self._extract_content(msg)
                
        except Exception as e:
            raise Exception(f"Failed to parse email file: {str(e)}")
    
    def parse_raw_email(self, raw_email):
        """
        Parse raw email text
        
        Args:
            raw_email (str): Raw email content
            
        Returns:
            str: The extracted email content (subject + body)
        """
        try:
            # Parse the email
            msg = self.str_parser.parsestr(raw_email)
            
            # Extract content
            return self._extract_content(msg)
            
        except Exception as e:
            raise Exception(f"Failed to parse raw email: {str(e)}")
    
    def _extract_content(self, msg):
        """
        Extract content from parsed email
        
        Args:
            msg (email.message.Message): Parsed email message
            
        Returns:
            str: The extracted email content (subject + body)
        """
        # Get subject
        subject = msg.get('Subject', '')
        
        # Get body
        body = self._get_email_body(msg)
        
        # Combine subject and body
        content = f"Subject: {subject}\n\n{body}"
        
        return content
    
    def _get_email_body(self, msg):
        """
        Extract the body from an email message, handling multipart messages
        
        Args:
            msg (email.message.Message): Parsed email message
            
        Returns:
            str: The extracted email body
        """
        # Check if the message is multipart
        if msg.is_multipart():
            # Get all text parts
            text_parts = []
            for part in msg.walk():
                # Check if this part is text
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    # Get the payload
                    try:
                        payload = part.get_payload(decode=True).decode(errors='replace')
                        text_parts.append(payload)
                    except:
                        # If decoding fails, try to get the payload without decoding
                        payload = part.get_payload()
                        if isinstance(payload, str):
                            text_parts.append(payload)
            
            # Join all text parts
            return '\n'.join(text_parts)
        else:
            # If not multipart, just get the payload
            try:
                return msg.get_payload(decode=True).decode(errors='replace')
            except:
                # If decoding fails, try to get the payload without decoding
                payload = msg.get_payload()
                if isinstance(payload, str):
                    return payload
                return "Unable to decode email content"