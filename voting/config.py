import os

HOST_NAME = os.environ.get('HOST_NAME', 'https://votazioni.mensa.it/')
ADMIN_MAIL = os.environ.get('ADMIN_MAIL', 'marco.montanari@gmail.com')
EMAIL_BACKUP = os.environ.get('EMAIL_BACKUP', 'votazionimensaitalia@gmail.com')
EMAIL_BACKUP_NAME = os.environ.get('EMAIL_BACKUP_NAME', 'Backup Votazioni Mensa')