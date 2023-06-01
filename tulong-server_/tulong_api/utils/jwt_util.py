import jwt


def generate_token(payload, secret, expiry=None):
    """
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: 生成jwt
    """
    # _payload = {'exp': expiry}
    # _payload.update(payload)

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def verify_token(token, secret):
    """
    校验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """

    # try:
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    # except jwt.PyJWTError:
        # payload = None

    return payload
