class UserPrivilege:
    user_id = ''
    role = 0
    privileges =''
    all_privileges = {1:'Admin', 2:'User'}
    @classmethod
    def generate_user_role(cls, user_id):
        if user_id == 1:
            cls.user_id = user_id
            cls.role = 1
            cls.privileges = cls.all_privileges[cls.role]
        else:
            cls.user_id = user_id
            cls.role = 2
            cls.privileges = cls.all_privileges[cls.role]

    @classmethod
    def get_privileges(cls, user_id, role):
        cls.user_id = user_id
        cls.role = role
        cls.privileges = cls.all_privileges[cls.role]

    @classmethod
    def get_privilege_key(cls, privilege:str):
        position = cls.all_privileges.index(privilege)
        return cls.all_privileges[position]

    @classmethod
    def update_user_role(cls, user_id, role):
        try:
            cls.user_id = user_id
            cls.role = role
            cls.privileges = cls.all_privileges[cls.role]
        except:
            cls.user_id = user_id
            cls.role = 2
            cls.privileges = cls.all_privileges[cls.role]
