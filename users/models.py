# users/models.py
#from django.contrib.auth.models import AbstractUser
#from django.db import models

# Inherit from AbstractUser to keep all default fields (username, password, email, etc.)
# but allows you to add custom fields later without new migrations.
#class CustomUser(AbstractUser):
    # Add any custom fields here, or leave it empty for now
    # Example: bio = models.TextField(max_length=500, blank=True)
 #   pass
    
 #   def __str__(self):
   #     return self.username

# Note: You generally don't need to define a custom manager unless you want 
# to change how users are created (e.g., using email as the username field).
# For now, inheriting AbstractUser is enough.