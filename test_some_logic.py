from django.utils.text import slugify



class SlugModel:
    def __init__(self, name):
        self.name = name
        self.slug = None

        
    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug
    
    

test = SlugModel('Hello World')
print('before save: ', test.slug)
test.save()
print('after save: ', test.slug)