import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import socket
import requests
import threading
import smtplib
import string
import secrets
import webbrowser
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlparse, urljoin
from config import (GOOGLE_SAFE_BROWSING_API_KEY, SAFE_BROWSING_API_URL, 
                   CLIENT_ID, CLIENT_VERSION, THREAT_TYPES, 
                   PLATFORM_TYPE, THREAT_ENTRY_TYPE, API_TIMEOUT)

# Email Configuration - UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
SENDER_EMAIL = "sup321980@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "ebrc gqao dqdp wize"    # Your Gmail app password
RECEIVER_EMAIL = "sup321980@gmail.com"  # Same as sender email (admin receives codes)

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Admin Configuration
ADMIN_PASSWORD = "admin123"  # Default admin password for check status feature


class MaliciousWebsiteBlocker:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.hosts_file = self.get_hosts_file_path()
        
    def get_hosts_file_path(self):
        """Get the appropriate hosts file path for the operating system"""
        if os.name == 'nt':  # Windows
            return r'C:\Windows\System32\drivers\etc\hosts'
        else:  # Unix-like systems
            return '/etc/hosts'
    
    def setup_ui(self):
        """Set up the main UI layout"""
        self.root.title("Website Blocker")
        self.root.geometry("750x700")
        self.root.configure(bg='#f8f9fa')
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Create main container with subtle shadow effect
        main_frame = tk.Frame(self.root, bg='#f8f9fa', padx=25, pady=25)
        main_frame.pack(fill='both', expand=True)
        
        # Header Section
        self.create_header(main_frame)
        
        # Spacer
        tk.Frame(main_frame, bg='#f8f9fa', height=20).pack()
        
        # Check Malicious Status Section
        self.create_check_section(main_frame)
        
        # Spacer
        tk.Frame(main_frame, bg='#f8f9fa', height=20).pack()
        
        # Block and Unblock Sections Container (side by side)
        self.create_block_unblock_sections(main_frame)
        
        # Bottom spacer
        tk.Frame(main_frame, bg='#f8f9fa', height=10).pack()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_header(self, parent):
        """Create the header section with logo and title"""
        header_frame = tk.Frame(parent, bg='#f8f9fa')
        header_frame.pack(fill='x')
        
        # Logo and Title Container
        title_container = tk.Frame(header_frame, bg='#f8f9fa')
        title_container.pack(pady=(0, 20))
        
        # Logo/Icon - Modern shield design
        logo_canvas = tk.Canvas(title_container, width=50, height=50, bg='#f8f9fa', highlightthickness=0)
        logo_canvas.pack(side='left', padx=(0, 15))
        
        # Draw shield logo
        logo_canvas.create_oval(10, 10, 40, 40, fill='#4f46e5', outline='#4f46e5', width=2)
        logo_canvas.create_oval(15, 15, 35, 35, fill='white', outline='white')
        logo_canvas.create_text(25, 25, text='🛡', font=('Arial', 16), fill='#4f46e5')
        
        # Main Title
        title_label = tk.Label(
            title_container,
            text="Website Blocker",
            font=('Segoe UI', 20, 'bold'),
            bg='#f8f9fa',
            fg='#1f2937'
        )
        title_label.pack(side='left', anchor='w')
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Protect your system from malicious websites",
            font=('Segoe UI', 10),
            bg='#f8f9fa',
            fg='#6b7280'
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Project Info Button
        info_button = tk.Button(
            header_frame,
            text="Project Info",
            font=('Segoe UI', 9),
            bg='#4f46e5',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.open_project_info_html
        )
        info_button.pack()
        self.style_modern_button(info_button, '#4f46e5', '#3730a3')
    
    def create_check_section(self, parent):
        """Create the check malicious status section"""
        # Section container with subtle background
        check_container = tk.Frame(parent, bg='white', relief='solid', bd=1)
        check_container.pack(fill='x', pady=(0, 10))
        
        check_frame = tk.Frame(check_container, bg='white', padx=20, pady=20)
        check_frame.pack(fill='x')
        
        # Section Title with icon
        title_frame = tk.Frame(check_frame, bg='white')
        title_frame.pack(fill='x', pady=(0, 15))
        
        check_title = tk.Label(
            title_frame,
            text="🔍 Check Malicious Status",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#7c3aed'
        )
        check_title.pack(anchor='w')
        
        # Description label
        desc_label = tk.Label(
            title_frame,
            text="Check if a website is safe using Google Safe Browsing API",
            font=('Segoe UI', 9),
            bg='white',
            fg='#6b7280'
        )
        desc_label.pack(anchor='w', pady=(5, 0))
        
        # URL Input Field with modern styling
        self.check_url_entry = tk.Entry(
            check_frame,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            width=35,
            fg='#374151',
            insertbackground='#4f46e5'
        )
        self.check_url_entry.pack(pady=(0, 15), ipady=8)
        self.check_url_entry.insert(0, "Enter website URL to check")
        self.check_url_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(self.check_url_entry, "Enter website URL to check"))
        self.check_url_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(self.check_url_entry, "Enter website URL to check"))
        self.check_url_entry.configure(fg='#9ca3af')
        
        # Action Buttons Frame
        check_buttons_frame = tk.Frame(check_frame, bg='white')
        check_buttons_frame.pack()
        
        # Upload File Button
        upload_check_button = tk.Button(
            check_buttons_frame,
            text="Upload file to check",
            font=('Segoe UI', 9),
            bg='#f59e0b',
            fg='white',
            relief='flat',
            padx=15,
            pady=10,
            cursor='hand2',
            command=self.bulk_check_from_file
        )
        upload_check_button.pack(side='left', padx=(0, 10))
        self.style_modern_button(upload_check_button, '#f59e0b', '#d97706')
        
        # Check Button
        check_button = tk.Button(
            check_buttons_frame,
            text="Check Status",
            font=('Segoe UI', 9, 'bold'),
            bg='#7c3aed',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.handle_check_malicious_status
        )
        check_button.pack(side='left')
        self.style_modern_button(check_button, '#7c3aed', '#6d28d9')
    
    def request_admin_password(self):
        """Request admin password from user"""
        try:
            user_input = simpledialog.askstring(
                "Administrator Authentication",
                "Enter admin password to access Check Status feature:",
                parent=self.root,
                show='*'  # Hide password input
            )
            return user_input
        except Exception:
            return None
    
    def handle_check_malicious_status(self):
        """Handle the check malicious status button click with admin password verification"""
        url = self.check_url_entry.get().strip()
        if not url or url == "Enter website URL to check":
            messagebox.showwarning("Warning", "Please enter a website URL.")
            return
        
        # Request admin password
        admin_password = self.request_admin_password()
        
        # Check if user canceled or entered nothing
        if admin_password is None or admin_password.strip() == "":
            messagebox.showinfo("Cancelled", "Operation cancelled by user")
            return
        
        # Verify admin password
        if admin_password.strip() == ADMIN_PASSWORD:
            # Password is correct, proceed with check
            self.check_malicious_status(url)
        else:
            # Password is incorrect
            messagebox.showerror("Access Denied", "Incorrect admin password")
    
    def create_block_unblock_sections(self, parent):
        """Create Block and Unblock sections side by side"""
        # Container frame for both sections
        sections_container = tk.Frame(parent, bg='#f8f9fa')
        sections_container.pack(fill='x')
        
        # Left side - Block section
        left_frame = tk.Frame(sections_container, bg='#f8f9fa')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right side - Unblock section
        right_frame = tk.Frame(sections_container, bg='#f8f9fa')
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Create the sections
        self.create_block_section(left_frame)
        self.create_unblock_section(right_frame)
        
    def create_block_section(self, parent):
        """Create the block websites section"""
        # Section container with subtle background
        block_container = tk.Frame(parent, bg='white', relief='solid', bd=1)
        block_container.pack(fill='x', pady=(0, 10))
        
        block_frame = tk.Frame(block_container, bg='white', padx=20, pady=20)
        block_frame.pack(fill='x')
        
        # Section Title with icon
        title_frame = tk.Frame(block_frame, bg='white')
        title_frame.pack(fill='x', pady=(0, 15))
        
        block_title = tk.Label(
            title_frame,
            text="🚫 Block Websites",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#dc2626'
        )
        block_title.pack(anchor='w')
        
        # URL Input Field with modern styling
        self.block_url_entry = tk.Entry(
            block_frame,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            width=35,
            fg='#374151',
            insertbackground='#4f46e5'
        )
        self.block_url_entry.pack(pady=(0, 15), ipady=8)
        self.block_url_entry.insert(0, "Enter website URL to block")
        self.block_url_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(self.block_url_entry, "Enter website URL to block"))
        self.block_url_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(self.block_url_entry, "Enter website URL to block"))
        self.block_url_entry.configure(fg='#9ca3af')
        
        # Action Buttons Frame
        block_buttons_frame = tk.Frame(block_frame, bg='white')
        block_buttons_frame.pack()
        
        # Upload File Button
        upload_block_button = tk.Button(
            block_buttons_frame,
            text="Upload file to block",
            font=('Segoe UI', 9),
            bg='#f59e0b',
            fg='white',
            relief='flat',
            padx=15,
            pady=10,
            cursor='hand2',
            command=self.bulk_block_from_file
        )
        upload_block_button.pack(side='left', padx=(0, 10))
        self.style_modern_button(upload_block_button, '#f59e0b', '#d97706')
        
        # Block Button
        block_button = tk.Button(
            block_buttons_frame,
            text="Block",
            font=('Segoe UI', 9, 'bold'),
            bg='#dc2626',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.block_single_website
        )
        block_button.pack(side='left')
        self.style_modern_button(block_button, '#dc2626', '#b91c1c')
        
    def create_unblock_section(self, parent):
        """Create the unblock websites section"""
        # Section container with subtle background
        unblock_container = tk.Frame(parent, bg='white', relief='solid', bd=1)
        unblock_container.pack(fill='x')
        
        unblock_frame = tk.Frame(unblock_container, bg='white', padx=20, pady=20)
        unblock_frame.pack(fill='x')
        
        # Section Title with icon
        title_frame = tk.Frame(unblock_frame, bg='white')
        title_frame.pack(fill='x', pady=(0, 15))
        
        unblock_title = tk.Label(
            title_frame,
            text="✅ Unblock Websites",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#059669'
        )
        unblock_title.pack(anchor='w')
        
        # URL Input Field with modern styling
        self.unblock_url_entry = tk.Entry(
            unblock_frame,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            width=35,
            fg='#374151',
            insertbackground='#4f46e5'
        )
        self.unblock_url_entry.pack(pady=(0, 15), ipady=8)
        self.unblock_url_entry.insert(0, "Enter website URL to unblock")
        self.unblock_url_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(self.unblock_url_entry, "Enter website URL to unblock"))
        self.unblock_url_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(self.unblock_url_entry, "Enter website URL to unblock"))
        self.unblock_url_entry.configure(fg='#9ca3af')
        
        # Action Buttons Frame
        unblock_buttons_frame = tk.Frame(unblock_frame, bg='white')
        unblock_buttons_frame.pack()
        
        # Upload File Button
        upload_unblock_button = tk.Button(
            unblock_buttons_frame,
            text="Upload file to unblock",
            font=('Segoe UI', 9),
            bg='#f59e0b',
            fg='white',
            relief='flat',
            padx=15,
            pady=10,
            cursor='hand2',
            command=self.bulk_unblock_from_file
        )
        upload_unblock_button.pack(side='left', padx=(0, 10))
        self.style_modern_button(upload_unblock_button, '#f59e0b', '#d97706')
        
        # Unblock Button
        unblock_button = tk.Button(
            unblock_buttons_frame,
            text="Unblock",
            font=('Segoe UI', 9, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.unblock_single_website
        )
        unblock_button.pack(side='left')
        self.style_modern_button(unblock_button, '#059669', '#047857')
    
    def style_button(self, button):
        """Apply rounded button styling"""
        button.configure(relief='flat', bd=0)
    
    def style_modern_button(self, button, bg_color, hover_color):
        """Apply modern button styling with hover effects"""
        button.configure(relief='flat', bd=0)
        
        def on_enter(e):
            button.configure(bg=hover_color)
        
        def on_leave(e):
            button.configure(bg=bg_color)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
    def clear_placeholder(self, entry, placeholder):
        """Clear placeholder text when entry is focused"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(fg='#374151')
    
    def restore_placeholder(self, entry, placeholder):
        """Restore placeholder text when entry loses focus and is empty"""
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(fg='#9ca3af')
    
    def create_project_info_html(self):
        """Create HTML file with project information"""
        html_content = '''

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Information - Block Malicious Websites</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #000000;
            background-color: #f8f9fa;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 0%;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, rgb(255, 255, 255) 0%, rgb(247, 247, 247) 100%);
            color: rgb(0, 0, 0);
            padding: 40px 30px;
            position: relative;
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .header-text {
            flex: 1;
        }

        .header h1 {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .profile-picture {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: 20px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            border: 4px solid white;
            position: relative;
            overflow: hidden;
        }

        .profile-picture img {
            width: 80%;
            height: 80%;
            object-fit: contain;
            border-radius: 50%;
            display: block;
            margin: auto;
        }

        .introduction {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            backdrop-filter: blur(10px);
        }

        .introduction p {
            font-size: 1.1em;
            line-height: 1.8;
        }

        .bold {
            font-weight: bold;
            color: rgb(2, 2, 2);
        }

        .content {
            padding: 40px 30px;
        }

        .section {
            margin-bottom: 40px;
        }

        .section h2 {
            color: #000000;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #0b0f11;
        }

        .table-container {
            overflow-x: auto;
            border-radius: 0px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        th {
            background-color: #5e3834;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.1em;
        }

        td {
            padding: 15px;
            border-bottom: 1px solid #ecf0f1;
            font-size: 1em;
        }

        tr:hover {
            background-color: #f8f9fa;
            transition: background-color 0.3s ease;
        }

        .status-completed {
            background-color: #d4edda;
            color: #155724;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
        }

        .footer {
            background: #5e3834;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }

        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                text-align: center;
            }

            .profile-picture {
                margin: 20px auto 0;
            }

            .header h1 {
                font-size: 2em;
            }

            .content {
                padding: 20px;
            }

            th,
            td {
                padding: 10px;
                font-size: 0.9em;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <div class="header-text">
                    <h1>Project Information</h1>
                    <div class="introduction">
                        <p>This project was developed by <span class="bold">Vinjamuri Teja, Jaya Lakshmi Vuppala,
                                V.Naveen Kumar</span> as part of a <span class="bold">Cyber
                                Security Internship</span>. This project is designed to <span class="bold">Safeguard users and organizations from <span class="bold">Cyber Threats</span> by <span class="bold">Blocking
                                        Malicious Websites</span> effectively.</p>

                    </div>
                </div>
                <div class="profile-picture"><img src="https://suprajatechnologies.com/images/logo.png"></div>
            </div>
        </div>

        <div class="content">
            <div class="section">
                <h2>Project Details</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Project Details</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Project Name</strong></td>
                                <td><b>Block Malicious Websites</b></td>
                            </tr>
                            <tr>
                                <td><strong>Project Description</strong></td>
                                <td><p>Implementing <span class="bold">Website Access Control Policy</span> on Devices to Prevent <span
                                        class="bold">Malicious Website Activities</span>.</p>
</td>
                            </tr>
                            <tr>
                                <td><strong>Project Start Date</strong></td>
                                <td>21-July-2025</td>
                            </tr>
                            <tr>
                                <td><strong>Project End Date</strong></td>
                                <td>11-August-2025</td>
                            </tr>
                            <tr>
                                <td><strong>Project Status</strong></td>
                                <td><span class="status-completed">Completed</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="section">
                <h2>Developer Details</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Employee ID</th>
                                <th>Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Jaya Lakshmi Vuppala</td>
                                <td>ST#IS#7554</td>
                                <td>jayav0679@gmail.com</td>
                            </tr>
                            <tr>
                                <td>Vinjamuri Teja</td>
                                <td>ST#IS#7562</td>
                                <td>teja75920@gmail.com</td>
                            </tr>
                            <tr>
                                <td>V.Naveen Kumar</td>
                                <td>ST#IS#7564</td>
                                <td>praveennaveen243@gmail.com</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="section">
                <h2>Company Details</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Company</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Company Name</strong></td>
                                <td>Supraja Technologies</td>
                            </tr>
                            <tr>
                                <td><strong>Email Address</strong></td>
                                <td>contact@suprajatechnologies.com</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>&copy; 2025 Supraja Technologies - Cyber Security Internship Project</p>
        </div>
    </div>
</body>

</html>
        
        '''
        
        html_path = os.path.join(os.path.dirname(__file__), 'project_info.html')
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return html_path
        except Exception as e:
            messagebox.showerror("Error", f"Could not create documentation file: {str(e)}")
            return None
    
    def open_project_info_html(self):
        """Open project information HTML file in browser"""
        try:
            html_path = self.create_project_info_html()
            if html_path:
                webbrowser.open(f'file://{html_path}')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open documentation: {str(e)}")
    
    def generate_verification_code(self, length=8):
        """Generate a cryptographically secure random verification code"""
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def send_verification_email(self, verification_code):
        """Send verification code to the admin email address"""
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = SENDER_EMAIL
            message["To"] = RECEIVER_EMAIL
            message["Subject"] = "Website Action Verification Code"
            
            # Email body
            body = f"Your verification code is: {verification_code}"
            message.attach(MIMEText(body, "plain"))
            
            # Connect to Gmail SMTP server
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # Enable TLS encryption
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            # Send email
            text = message.as_string()
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
            server.quit()
            
            return True, "Verification email sent successfully"
            
        except Exception as e:
            return False, f"Failed to send verification email: {str(e)}"
    
    def request_verification_code(self):
        """Request verification code from user via popup dialog"""
        try:
            user_input = simpledialog.askstring(
                "Email Verification",
                f"Enter the verification code sent to {RECEIVER_EMAIL}:",
                parent=self.root
            )
            return user_input
        except Exception:
            return None
    
    def verify_and_execute(self, action_function, *args):
        """Verify email code and execute the requested action"""
        try:
            # Generate verification code
            verification_code = self.generate_verification_code()
            
            # Send email with verification code
            email_success, email_message = self.send_verification_email(verification_code)
            if not email_success:
                messagebox.showerror("Error", email_message)
                return
            
            # Request verification code from user
            user_code = self.request_verification_code()
            
            # Check if user canceled or entered nothing
            if user_code is None or user_code.strip() == "":
                messagebox.showinfo("Cancelled", "Operation cancelled by user")
                return
            
            # Verify the code
            if user_code.strip() == verification_code:
                # Code is correct, execute the action
                success, message = action_function(*args)
                self.show_result(success, message)
            else:
                # Code is incorrect
                messagebox.showerror("Error", "Incorrect verification code")
                
        except Exception as e:
            messagebox.showerror("Error", f"Verification failed: {str(e)}")
    
    def normalize_url(self, url):
        """Normalize URL by removing protocol and www prefix"""
        if not url:
            return ""
        
        # Remove http:// or https://
        if url.startswith(('http://', 'https://')):
            parsed = urlparse(url)
            url = parsed.netloc
        
        # Remove www. prefix
        if url.startswith('www.'):
            url = url[4:]
            
        return url.strip().lower()
    
    def format_url_for_api(self, url):
        """Format URL for Google Safe Browsing API"""
        if not url:
            return ""
        
        # Add http:// if no protocol is specified
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        return url.strip()
    
    def check_safe_browsing_api(self, url):
        """Check if website is malicious using Google Safe Browsing API v4"""
        try:
            # Check if API key is configured
            if GOOGLE_SAFE_BROWSING_API_KEY == "YOUR_API_KEY_HERE":
                return False, "Google Safe Browsing API key not configured. Please update config.py"
            
            # Format URL for API
            formatted_url = self.format_url_for_api(url)
            if not formatted_url:
                return False, "Invalid URL format"
            
            # Prepare API request
            api_url = f"{SAFE_BROWSING_API_URL}?key={GOOGLE_SAFE_BROWSING_API_KEY}"
            
            # Create request payload
            payload = {
                "client": {
                    "clientId": CLIENT_ID,
                    "clientVersion": CLIENT_VERSION
                },
                "threatInfo": {
                    "threatTypes": THREAT_TYPES,
                    "platformTypes": [PLATFORM_TYPE],
                    "threatEntryTypes": [THREAT_ENTRY_TYPE],
                    "threatEntries": [
                        {"url": formatted_url}
                    ]
                }
            }
            
            # Make API request
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=API_TIMEOUT
            )
            
            # Check response status
            if response.status_code == 200:
                result = response.json()
                
                # Check if matches found (malicious)
                if "matches" in result and result["matches"]:
                    threat_types = [match["threatType"] for match in result["matches"]]
                    return True, f"Malicious website detected! Threat types: {', '.join(threat_types)}"
                else:
                    # No matches found (safe)
                    return False, "The website is safe."
            
            elif response.status_code == 400:
                return False, "Invalid API request. Please check the URL format."
            elif response.status_code == 401:
                return False, "Invalid API key. Update your key in config.py"
            elif response.status_code == 429:
                return False, "Daily API limit reached. Try again later."
            else:
                return False, f"API request failed with status code: {response.status_code}"
            
        except requests.exceptions.Timeout:
            return False, "Error connecting to Safe Browsing API. Request timed out."
        except requests.exceptions.ConnectionError:
            return False, "Error connecting to Safe Browsing API. Please check your internet connection."
        except requests.exceptions.RequestException as e:
            return False, f"Error connecting to Safe Browsing API: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def check_malicious_status(self, url):
        """Check malicious status and handle user interaction"""
        if not url or url == "Enter website URL to check":
            messagebox.showwarning("Warning", "Please enter a website URL.")
            return
        
        # Show loading message
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Checking...")
        loading_window.geometry("300x100")
        loading_window.resizable(False, False)
        loading_window.configure(bg='white')
        
        # Center the loading window
        loading_window.transient(self.root)
        loading_window.grab_set()
        
        # Add loading message
        loading_label = tk.Label(
            loading_window,
            text="Checking website safety...\nPlease wait...",
            font=('Segoe UI', 10),
            bg='white',
            fg='#374151'
        )
        loading_label.pack(expand=True)
        
        def check_in_thread():
            try:
                # Check with Safe Browsing API
                is_malicious, message = self.check_safe_browsing_api(url)
                
                # Close loading window
                self.root.after(0, loading_window.destroy)
                
                if is_malicious:
                    # Website is malicious, ask user if they want to block it
                    result = messagebox.askyesno(
                        "Malicious Website Detected!",
                        f"{message}\n\nDo you want to block this website?",
                        icon='warning'
                    )
                    
                    if result:  # User clicked Yes
                        # Trigger website blocking process
                        self.root.after(0, lambda: self.verify_and_block(url))
                    # If No, do nothing
                else:
                    # Website is safe or there was an error
                    if "safe" in message.lower():
                        messagebox.showinfo("Safe Website", message, icon='info')
                    else:
                        messagebox.showerror("Error", message)
                        
            except Exception as e:
                # Close loading window and show error
                self.root.after(0, loading_window.destroy)
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to check website: {str(e)}"))
        
        # Start checking in background thread
        threading.Thread(target=check_in_thread, daemon=True).start()
    
    def is_malicious_website(self, url):
        """Check if a website is malicious using VirusTotal API"""
        try:
            # This is a placeholder - you would need a real API key
            # For demonstration, we'll do a basic check
            normalized_url = self.normalize_url(url)
            
            # Basic validation
            if not normalized_url or '.' not in normalized_url:
                return False, "Invalid URL format"
            
            # Try to resolve the domain
            try:
                socket.gethostbyname(normalized_url)
            except socket.gaierror:
                return False, "Domain does not exist"
            
            # For now, return True to allow blocking
            # In a real implementation, you would check against threat intelligence APIs
            return True, "Website can be blocked"
            
        except Exception as e:
            return False, f"Error checking website: {str(e)}"
    
    def block_website(self, url):
        """Block a single website by adding it to hosts file"""
        try:
            normalized_url = self.normalize_url(url)
            if not normalized_url:
                return False, "Invalid URL"
            
            # Check if already blocked
            if self.is_website_blocked(normalized_url):
                return False, f"{normalized_url} is already blocked"
            
            # Add to hosts file
            with open(self.hosts_file, 'a', encoding='utf-8') as f:
                f.write(f"\n127.0.0.1 {normalized_url}")
                f.write(f"\n127.0.0.1 www.{normalized_url}")
            
            return True, f"Successfully blocked {normalized_url}"
            
        except PermissionError:
            return False, "Permission denied. Run as administrator."
        except Exception as e:
            return False, f"Error blocking website: {str(e)}"
    
    def unblock_website(self, url):
        """Unblock a single website by removing it from hosts file"""
        try:
            normalized_url = self.normalize_url(url)
            if not normalized_url:
                return False, "Invalid URL"
            
            # Read current hosts file
            with open(self.hosts_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Filter out lines containing the URL
            filtered_lines = []
            removed = False
            for line in lines:
                if normalized_url not in line.lower() or not line.strip().startswith('127.0.0.1'):
                    filtered_lines.append(line)
                else:
                    removed = True
            
            if not removed:
                return False, f"{normalized_url} was not blocked"
            
            # Write back to hosts file
            with open(self.hosts_file, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)
            
            return True, f"Successfully unblocked {normalized_url}"
            
        except PermissionError:
            return False, "Permission denied. Run as administrator."
        except Exception as e:
            return False, f"Error unblocking website: {str(e)}"
    
    def is_website_blocked(self, url):
        """Check if a website is currently blocked"""
        try:
            normalized_url = self.normalize_url(url)
            with open(self.hosts_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                return f"127.0.0.1 {normalized_url}" in content
        except:
            return False
    
    def verify_and_block(self, url):
        """Verify and block a single website"""
        def verification_thread():
            self.root.after(0, lambda: self.verify_and_execute(self.block_website, url))
        
        threading.Thread(target=verification_thread, daemon=True).start()
    
    def verify_and_unblock(self, url):
        """Verify and unblock a single website"""
        def verification_thread():
            self.root.after(0, lambda: self.verify_and_execute(self.unblock_website, url))
        
        threading.Thread(target=verification_thread, daemon=True).start()
    
    def block_single_website(self):
        """Handle blocking a single website with verification"""
        url = self.block_url_entry.get().strip()
        if not url or url == "Enter website URL to block":
            messagebox.showwarning("Warning", "Please enter a URL to block")
            return
        
        self.verify_and_block(url)
    
    def unblock_single_website(self):
        """Handle unblocking a single website with verification"""
        url = self.unblock_url_entry.get().strip()
        if not url or url == "Enter website URL to unblock":
            messagebox.showwarning("Warning", "Please enter a URL to unblock")
            return
        
        self.verify_and_unblock(url)
    
    def bulk_block_from_file(self):
        """Handle bulk blocking from file with email verification"""
        file_path = filedialog.askopenfilename(
            title="Select file with URLs to block",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Verify with email before processing file
        self.verify_and_execute(self.process_bulk_block_file, file_path)
    
    def process_bulk_block_file(self, file_path):
        """Process bulk blocking file after verification"""
        def bulk_block_thread():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                blocked_count = 0
                failed_count = 0
                results = []
                
                for url in urls:
                    if url and not url.startswith('#'):  # Skip comments
                        success, message = self.block_website(url)
                        if success:
                            blocked_count += 1
                        else:
                            failed_count += 1
                            results.append(f"Failed to block {url}: {message}")
                
                result_message = f"Blocked: {blocked_count}, Failed: {failed_count}"
                if results:
                    result_message += f"\n\nErrors:\n" + "\n".join(results[:5])
                    if len(results) > 5:
                        result_message += f"\n... and {len(results) - 5} more errors"
                
                self.root.after(0, lambda: messagebox.showinfo("Bulk Block Results", result_message))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process file: {str(e)}"))
        
        threading.Thread(target=bulk_block_thread, daemon=True).start()
        return True, "File processing initiated"
    
    def bulk_unblock_from_file(self):
        """Handle bulk unblocking from file with email verification"""
        file_path = filedialog.askopenfilename(
            title="Select file with URLs to unblock",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Verify with email before processing file
        self.verify_and_execute(self.process_bulk_unblock_file, file_path)
    
    def process_bulk_unblock_file(self, file_path):
        """Process bulk unblocking file after verification"""
        def bulk_unblock_thread():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                unblocked_count = 0
                failed_count = 0
                results = []
                
                for url in urls:
                    if url and not url.startswith('#'):  # Skip comments
                        success, message = self.unblock_website(url)
                        if success:
                            unblocked_count += 1
                        else:
                            failed_count += 1
                            results.append(f"Failed to unblock {url}: {message}")
                
                result_message = f"Unblocked: {unblocked_count}, Failed: {failed_count}"
                if results:
                    result_message += f"\n\nErrors:\n" + "\n".join(results[:5])
                    if len(results) > 5:
                        result_message += f"\n... and {len(results) - 5} more errors"
                
                self.root.after(0, lambda: messagebox.showinfo("Bulk Unblock Results", result_message))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process file: {str(e)}"))
        
        threading.Thread(target=bulk_unblock_thread, daemon=True).start()
        return True, "File processing initiated"
    
    def bulk_check_from_file(self):
        """Handle bulk checking from file with admin password verification"""
        # Request admin password first
        admin_password = self.request_admin_password()
        
        # Check if user canceled or entered nothing
        if admin_password is None or admin_password.strip() == "":
            messagebox.showinfo("Cancelled", "Operation cancelled by user")
            return
        
        # Verify admin password
        if admin_password.strip() != ADMIN_PASSWORD:
            messagebox.showerror("Access Denied", "Incorrect admin password")
            return
        
        # Password is correct, proceed with file selection
        file_path = filedialog.askopenfilename(
            title="Select file with URLs to check",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Process the file
        self.process_bulk_check_file(file_path)
    
    def process_bulk_check_file(self, file_path):
        """Process bulk checking file"""
        def bulk_check_thread():
            try:
                # Show progress window
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Checking URLs...")
                progress_window.geometry("400x150")
                progress_window.resizable(False, False)
                progress_window.configure(bg='white')
                progress_window.transient(self.root)
                progress_window.grab_set()
                
                # Progress label
                progress_label = tk.Label(
                    progress_window,
                    text="Checking websites for malicious content...\nPlease wait...",
                    font=('Segoe UI', 10),
                    bg='white',
                    fg='#374151'
                )
                progress_label.pack(expand=True, pady=20)
                
                # Read URLs from file
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                safe_urls = []
                malicious_urls = []
                error_urls = []
                
                total_urls = len([url for url in urls if url and not url.startswith('#')])
                processed = 0
                
                for url in urls:
                    if url and not url.startswith('#'):  # Skip comments
                        processed += 1
                        # Update progress
                        self.root.after(0, lambda p=processed, t=total_urls: 
                                      progress_label.config(text=f"Checking websites...\nProgress: {p}/{t}"))
                        
                        is_malicious, message = self.check_safe_browsing_api(url)
                        
                        if "safe" in message.lower():
                            safe_urls.append(url)
                        elif is_malicious:
                            malicious_urls.append((url, message))
                        else:
                            error_urls.append((url, message))
                
                # Close progress window
                self.root.after(0, progress_window.destroy)
                
                # Create detailed results window
                self.root.after(0, lambda: self.show_bulk_check_results(safe_urls, malicious_urls, error_urls))
                
            except Exception as e:
                self.root.after(0, progress_window.destroy)
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process file: {str(e)}"))
        
        threading.Thread(target=bulk_check_thread, daemon=True).start()
    
    def show_bulk_check_results(self, safe_urls, malicious_urls, error_urls):
        """Show detailed results of bulk check in a new window"""
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("Bulk Check Results")
        results_window.geometry("700x600")
        results_window.configure(bg='#f8f9fa')
        results_window.transient(self.root)
        
        # Main frame
        main_frame = tk.Frame(results_window, bg='#f8f9fa', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Website Safety Check Results",
            font=('Segoe UI', 16, 'bold'),
            bg='#f8f9fa',
            fg='#1f2937'
        )
        title_label.pack(pady=(0, 20))
        
        # Summary frame
        summary_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1, padx=15, pady=15)
        summary_frame.pack(fill='x', pady=(0, 20))
        
        summary_text = f"""📊 Summary:
        
✅ Safe Websites: {len(safe_urls)}
🚫 Malicious Websites: {len(malicious_urls)}
⚠️ Errors/Unable to Check: {len(error_urls)}
        
🔍 Total Checked: {len(safe_urls) + len(malicious_urls) + len(error_urls)}"""
        
        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=('Segoe UI', 11),
            bg='white',
            fg='#374151',
            justify='left'
        )
        summary_label.pack(anchor='w')
        
        # Create notebook for tabs
        from tkinter import ttk
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 10))
        
        # Safe URLs tab
        if safe_urls:
            safe_frame = tk.Frame(notebook, bg='white')
            notebook.add(safe_frame, text=f"Safe URLs ({len(safe_urls)})")
            
            safe_text = tk.Text(safe_frame, font=('Consolas', 10), wrap='word', padx=10, pady=10)
            safe_scrollbar = tk.Scrollbar(safe_frame, orient='vertical', command=safe_text.yview)
            safe_text.configure(yscrollcommand=safe_scrollbar.set)
            
            safe_text.pack(side='left', fill='both', expand=True)
            safe_scrollbar.pack(side='right', fill='y')
            
            safe_content = "\n".join([f"✅ {url}" for url in safe_urls])
            safe_text.insert('1.0', safe_content)
            safe_text.config(state='disabled')
        
        # Malicious URLs tab
        if malicious_urls:
            mal_frame = tk.Frame(notebook, bg='white')
            notebook.add(mal_frame, text=f"Malicious URLs ({len(malicious_urls)})")
            
            mal_text = tk.Text(mal_frame, font=('Consolas', 10), wrap='word', padx=10, pady=10)
            mal_scrollbar = tk.Scrollbar(mal_frame, orient='vertical', command=mal_text.yview)
            mal_text.configure(yscrollcommand=mal_scrollbar.set)
            
            mal_text.pack(side='left', fill='both', expand=True)
            mal_scrollbar.pack(side='right', fill='y')
            
            mal_content = "\n\n".join([f"🚫 {url}\n   Threat: {message}" for url, message in malicious_urls])
            mal_text.insert('1.0', mal_content)
            mal_text.config(state='disabled')
        
        # Error URLs tab
        if error_urls:
            error_frame = tk.Frame(notebook, bg='white')
            notebook.add(error_frame, text=f"Errors ({len(error_urls)})")
            
            error_text = tk.Text(error_frame, font=('Consolas', 10), wrap='word', padx=10, pady=10)
            error_scrollbar = tk.Scrollbar(error_frame, orient='vertical', command=error_text.yview)
            error_text.configure(yscrollcommand=error_scrollbar.set)
            
            error_text.pack(side='left', fill='both', expand=True)
            error_scrollbar.pack(side='right', fill='y')
            
            error_content = "\n\n".join([f"⚠️ {url}\n   Error: {message}" for url, message in error_urls])
            error_text.insert('1.0', error_content)
            error_text.config(state='disabled')
        
        # Action buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f8f9fa')
        buttons_frame.pack(fill='x', pady=(10, 0))
        
        # Block all malicious button
        if malicious_urls:
            block_all_button = tk.Button(
                buttons_frame,
                text=f"Block All Malicious URLs ({len(malicious_urls)})",
                font=('Segoe UI', 9, 'bold'),
                bg='#dc2626',
                fg='white',
                relief='flat',
                padx=20,
                pady=10,
                cursor='hand2',
                command=lambda: self.bulk_block_malicious_urls([url for url, _ in malicious_urls])
            )
            block_all_button.pack(side='left', padx=(0, 10))
            self.style_modern_button(block_all_button, '#dc2626', '#b91c1c')
        
        # Close button
        close_button = tk.Button(
            buttons_frame,
            text="Close",
            font=('Segoe UI', 9),
            bg='#6b7280',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=results_window.destroy
        )
        close_button.pack(side='right')
        self.style_modern_button(close_button, '#6b7280', '#4b5563')
    
    def bulk_block_malicious_urls(self, urls):
        """Block all malicious URLs found during bulk check"""
        def block_thread():
            try:
                blocked_count = 0
                failed_count = 0
                results = []
                
                for url in urls:
                    success, message = self.block_website(url)
                    if success:
                        blocked_count += 1
                    else:
                        failed_count += 1
                        results.append(f"Failed to block {url}: {message}")
                
                result_message = f"Blocked: {blocked_count}, Failed: {failed_count}"
                if results:
                    result_message += f"\n\nErrors:\n" + "\n".join(results[:5])
                    if len(results) > 5:
                        result_message += f"\n... and {len(results) - 5} more errors"
                
                self.root.after(0, lambda: messagebox.showinfo("Bulk Block Results", result_message))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to block websites: {str(e)}"))
        
        threading.Thread(target=block_thread, daemon=True).start()
    
    def show_result(self, success, message):
        """Show operation result to user"""
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)


def main():
    root = tk.Tk()
    app = MaliciousWebsiteBlocker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
