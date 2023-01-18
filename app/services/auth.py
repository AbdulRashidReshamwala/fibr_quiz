class AuthService:
    auth_provider = None

    def __init__(self, auth_provider) -> None:
        self.auth_provider = auth_provider

    def create_user(self, email, password):
        user = self.auth_provider.create_user(email=email, password=password)
        return user

    def create_jwt(self, user_id):
        return self.auth_provider.create_custom_token(user_id)

    def verify_jwt(self, jwt):
        user = self.auth_provider.verify_id_token(jwt)
        return user
