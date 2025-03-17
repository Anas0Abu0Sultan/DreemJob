from django.db import models
from django.contrib.auth.models import User


# class customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     card = models.IntegerField()
#     country = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="img/customer/", null=True)
#     # 1 customer many jobs --->  1 job 1 customer


#     def __str__(self):
#         return str(self.user.username)


class category(models.Model):
    name = models.CharField(max_length=30)


    def __str__(self):
        return self.name 


class freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_job = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100)
    image = models.ImageField(upload_to="img/freelancer/", null=True,default='img/blog/author.png')


    def __str__(self):
        return str(self.user.username)


class job(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=6000)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    salary = models.DecimalField(max_digits=7,decimal_places=2,default=0.0)
    category = models.ForeignKey(category, on_delete=models.CASCADE,related_name='job_category')
    created_by = models.ForeignKey(freelancer, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="img/post/", null=True)
    job_nature = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=50,default='remot')

    # 1 customer many jobs --->  1 job 1 customer


    def __str__(self):
        return self.title
    
from django.db.models import UniqueConstraint

class apply(models.Model):
    freelancer = models.ForeignKey(freelancer, on_delete=models.CASCADE, related_name="applications",null= True)  
    job = models.ForeignKey(job, on_delete=models.CASCADE, related_name="applications",null= True)  
    link = models.URLField(max_length=200)
    cv = models.FileField(upload_to="service/cv/", null=True)
    coverletter = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('freelancer', 'job')

    def __str__(self):
        return f"{self.freelancer.user.username} - {self.job.title}"
