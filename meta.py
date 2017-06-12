class contact:
    def __init__(self,name=None,mobile=None,home=None,office=None,email=None,id_=None):
        self.__name=name
        self.__mobile=mobile
        self.__home=home
        self.__office=office
        self.__email=email
        self.id_=id_
    @property
    def get(self):
        return {'name': self.__name,'mobile':self.__mobile,'home':self.__home,\
                'office':self.__office,'email':self.__email}
    def update_name(self,value):
        self.__name=value
    def update_mobile(self,value):
        self.__mobile=value
    def update_home(self,value):
        self.__home=value
    def update_office(self,value):
        self.__office=value
    def update_email(self,value):
        self.__email=value
    def __lt__(self,other):
        return self.__name.lower() < other.__name.lower()
    def __gt__(self,other):
        return self.__name.lower() > other.__name.lower()
    #def __eq__(self,other):
     #   return self.__name == other.__name
    
    def __str__(self):
        return self.__name or self.__mobile or self.__email or self.__home or self.__office
    
