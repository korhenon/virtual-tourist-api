from typing import Optional

import jwt

from data.environment import EnvironmentDataSource


class JWTDataSource:
    @staticmethod
    def encode(email: str) -> str:
        return jwt.encode({"email": email}, EnvironmentDataSource.get_jwt_secret(), algorithm="HS256")

    @staticmethod
    def decode(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, EnvironmentDataSource.get_jwt_secret(), algorithms=["HS256"])
            return payload["email"]
        except jwt.DecodeError:
            return None
