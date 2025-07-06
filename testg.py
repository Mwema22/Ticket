import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('codewithmwema22@gmail.com', 'abcdefghijklmnop')  # App Password here
    print("✅ Login successful")
    server.quit()
except Exception as e:
    print("❌ Login failed:", e)
