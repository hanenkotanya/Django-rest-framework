from django.db import models



class Age(models.Model):
    AGE_CHOICES = (
        ('choises', 'choises'),
        ('1_4', 'Animators for 1-4 years'),
        ('5_9', 'Animators for 5-9 years'),
        ('10_14', 'Animators for 10-14 years')
    )
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default='choises')
    animators_for_years = models.ManyToManyField('personage.Personage', blank=True, related_name ='for_age')

    
    def __str__(self):
        
        return str(self.age)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    


