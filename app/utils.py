from passlib.context import CryptContext
from pydantic import SecretStr

## assigns the type of hashing that will be done with the passwords of the users
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: SecretStr):
    ## hash the password
    return pwd_context.hash(password.get_secret_value())

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    