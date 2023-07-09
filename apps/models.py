from django.db import models
from django.contrib.auth.models import User # Import for user authentication

class Account(models.Model):
    # User Authentication's Instance (1-1 relationship)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional Fields
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)

    # Favorite Posts
    favorite_courses = models.ManyToManyField('Course', blank=True, related_name='favorite_by')
    def __str__(self):
        return self.user.username
    
class Course(models.Model):
    CREDIT_CHOICES = (
        (4, '4'),
        (2, '2'),
        (0, '0'),
    )

    FACULTY_CHOICES = (
        ('----', '----'),
        ('Faculty of Environment and Information Studies', 'Faculty of Environment and Information Studies'),
        ('Faculty of Policy Management', 'Faculty of Policy Management'),
        ('Faculty of Media and Governance', 'Faculty of Media and Governance'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    credit = models.IntegerField(choices=CREDIT_CHOICES, default=0)
    faculty = models.TextField(choices=FACULTY_CHOICES, default='----')
    professor = models.TextField()
    intro = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    SCORE_CHOICES = (
        (-5, '-5'),
        (-4, '-4'),
        (-3, '-3'),
        (-2, '-2'),
        (-1, '-1'),
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    name = models.TextField()
    body = models.TextField()
    score = models.IntegerField(choices=SCORE_CHOICES, default=0)
    posted_date = models.DateTimeField(auto_now_add=True)
    
    
